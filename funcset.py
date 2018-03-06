# coding : UTF-8

import csv
import datetime
import logging
import os
import traceback

import tushare as ts

import const
import get_report_basic
import get_stock_list
import ws_base


def log(msg):
    pass
    # print("wssr: " + msg)

def output(msg, end='\r'):
    print(msg, end)

def write_str_to_file(file_name, contents):
    f = open(file_name, 'w')
    f.write(contents)
    f.close()

def write_lastday(ld=None, csv=const.LAST_DAY_CSV):
    if ld is None:
        ld = datetime.datetime.now() + datetime.timedelta(days=-1)
    with open(csv, 'w', errors='ignore', newline='') as f:
        f.write(ld.strftime('%Y-%m-%d'))
        f.close()

def read_lastday(csv=const.LAST_DAY_CSV):
    if not os.path.exists(csv):
        twohundred_days_ago = datetime.datetime.now() + datetime.timedelta(days=-80)
        write_lastday(twohundred_days_ago)
    with open(csv, 'r', errors='ignore', newline='') as f:
        last_day = f.readline()
        f.close()
    return datetime.datetime.strptime(last_day, "%Y-%m-%d")

# stock_data is the dataframe from tushare
def getStockMacd(stock_data, macd_l=26, macd_s=12, macd_m=9):
    stock_data['ma_s'] = stock_data['close'].ewm(span=macd_s).mean().tolist()
    stock_data['ma_l'] = stock_data['close'].ewm(span=macd_l).mean().tolist()
    stock_data['diff'] = (stock_data['ma_s'] - stock_data['ma_l']).tolist()
    stock_data['dea'] = stock_data['diff'].ewm(span=macd_m).mean().tolist()
    stock_data['macd'] = ((stock_data['diff'] - stock_data['dea']) * 2).tolist()
    return stock_data

def getStockKDJ(stock_data, n=9, n1=3, n2=3):
    stock_length = len(stock_data)
    rsv_list = [0.0 for i in range(stock_length)]
    k_list = [0.0 for i in range(stock_length)]
    d_list = [0.0 for i in range(stock_length)]
    j_list = [0.0 for i in range(stock_length)]

    high_list = list(stock_data['high'])
    low_list = list(stock_data['low'])
    close_list = list(stock_data['close'])

    # complement the 0:n-1 value due to the rolling max/min method will get these values to nan
    for i in range(1, min(n, stock_length)):
        high_list[i - 1] = max(stock_data['high'][0:i])
        low_list[i - 1] = min(stock_data['low'][0:i])

    rsv_list[0] = (close_list[0] - low_list[0]) / (high_list[0] - low_list[0]) * 100.0
    k_list[0] = rsv_list[0]
    d_list[0] = rsv_list[0]
    j_list[0] = rsv_list[0]

    for i in range(1, stock_length):
        rsv_list[i] = (close_list[i] - low_list[i]) / (high_list[i] - low_list[i]) * 100.0
        k_list[i] = (k_list[i - 1] * (n1 - 1) + rsv_list[i]) / n1
        d_list[i] = (d_list[i - 1] * (n2 - 1) + k_list[i]) / n2
        j_list[i] = k_list[i] * 3.0 - d_list[i] * 2.0
    stock_data['k'] = k_list
    stock_data['d'] = d_list
    stock_data['j'] = j_list
    return stock_data


def getKDJMacdBrandistock(args):
    stock_data = args[0]
    type = args[1]
    stock_length = len(stock_data)
    if stock_length == 0:
        output("no data")
        return
    stock_data = getStockKDJ(getStockMacd(stock_data))
    diff_list = list(stock_data['diff'])
    dea_list = list(stock_data['dea'])
    date_list = list(stock_data['date'])
    k_list = list(stock_data['k'])
    d_list = list(stock_data['d'])
    j_list = list(stock_data['j'])
    macd_list = ["-" for i in range(stock_length)]
    kdj_list = ["-" for i in range(stock_length)]
    for i in range(1, stock_length - 1):
        if diff_list[i - 1] > dea_list[i - 1] and diff_list[i] < \
                dea_list[i]:
            macd_list[i] = "金叉"
        if j_list[i - 1] > k_list[i - 1] and j_list[i - 1] > \
                d_list[i - 1] and j_list[i] < k_list[i] and \
                j_list[i] < d_list[i]:
            kdj_list[i] = "金叉"
    output("-----------------------------------------------------------")
    output("%-8s\t%-10s\t%-10s" % (u"时间", u"KDJ金叉(" + type + ")", u"MACD金叉(" + type + ")"))
    for i in range(stock_length):
        if kdj_list[i] == "金叉" or macd_list[i] == "金叉":
            output("%-8s\t%-10s\t%-10s" % (date_list[i], kdj_list[i], macd_list[i]))
    output("-----------------------------------------------------------")

def write_listlist_csv(filename, mode, listlist):
    with open(filename, mode, errors='ignore', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(listlist)
        f.close()
        log(filename + " was generated!")

def read_listlist_csv(filename):
    listlist = []
    with open(filename, 'r', errors='ignore', newline='') as f:
        f_csv = csv.reader(f)
        listlist = [row for row in f_csv]
        f.close()
    return listlist

def merge_report_records(get_data_all, get_data):
    for temp_date, stock_array in get_data.items():
        for r in stock_array:
            if temp_date not in get_data_all.keys():
                get_data_all[temp_date] = []
            get_data_all[temp_date].append(r)
    return get_data_all

def generate_report_1(url, get_data_func, encoding, start_date, end_date, stock_list):
    get_report_all = {}
    i = 1
    stop = False
    try:
        while not stop:
            newurl = url.replace("PAGENUMBER", str(i))
            log("reading url path:" + newurl + " with " + encoding)
            ws = ws_base.WS(newurl, get_data_func, start_date, end_date, stock_list, encoding)
            [get_report, stop] = ws.get_data()
            get_report_all = merge_report_records(get_report_all, get_report)
            i = i + 1
    except BaseException as e:
        msg = traceback.format_exc()
        log(msg)
        logging.exception(e)
    return get_report_all

def load_all_existing_report(start_date, end_date):
    report_all = {}
    cur_day = start_date
    while cur_day <= end_date:
        # log(str(cur_day) + " " +  str(end_date))
        data_string = str(cur_day.year) + "-" + str(cur_day.month).zfill(2) + "-" + str(cur_day.day).zfill(2)
        file_name = const.REPORT_CSV.replace("DATEYYMMDD", data_string)
        cur_day = cur_day + datetime.timedelta(days=1)
        if not os.path.exists(file_name):
            log(file_name + " doesn't exist.")
            continue
        list_array = read_listlist_csv(file_name)
        for sr in list_array:
            if not sr[0] in report_all.keys():
                stock_rec = ws_base.STOCK_REC(sr[0], sr[1], sr[2])
                report_all[sr[0]] = stock_rec
            else:
                report_all[sr[0]].add_rec_count(sr[2])
                report_all[sr[0]].add_rec_org(sr[3].split(","))
    return report_all


def get_quota(args):
    k_index = args[0]
    time_list = args[1]
    quota = {}
    if k_index is None or len(k_index) == 0:
        k_close = []
        k_open = []
    else:
        k_close = list(k_index['close'])
        k_open = list(k_index['open'])
    end = 1
    start = 1
    for d in time_list:
        if len(k_close) == 0:
            quota[str(d)] = "-"
        else:
            end = k_close[0]
        if len(k_open) < d:
            quota[str(d)] = "-"
        else:
            start = k_open[d - 1]
        if len(k_close) > 0 and len(k_open) >= d:
            quota[str(d)] = str(format((end - start) / start, '.2%'))
    return quota


def get_history_data_and_quota(stock_num, ktype, func, last_day=datetime.datetime.now(), k_list=const.DAY_LIST):
    k_index = None
    i = 0
    while i <= 5 and k_index is None:
        try:
            i = i + 1
            start_day = last_day + datetime.timedelta(days=-400)
            k_index = ts.get_k_data(stock_num, ktype=ktype, start=start_day.strftime('%Y-%m-%d'),
                                    end=last_day.strftime('%Y-%m-%d'))
            k_index = k_index[::-1]
        except BaseException as e:
            log(e)
            if k_index is None:
                log("get_history_data_and_quota retrying......" + str(i))
    return func([k_index, k_list])

def get_webcache_hash_file_name(cont, datasting):
    hash_string = str(hex(int(hash(cont)))).replace("0x", "").replace("-", "")
    i = 1
    hash_string1 = hash_string
    while os.path.exists(const.WEBCACHE_CSV.replace("DATEYYMMDDHHMMDD",
                                                    hash_string1).replace(
        "DATEYYMMDD", datasting)):
        hash_string1 = hash_string + "-" + str(i)
        i += 1
    return const.WEBCACHE_CSV.replace("DATEYYMMDDHHMMDD",
                                      hash_string1).replace(
        "DATEYYMMDD", datasting)

def get_working_days(start, end):
    wd = 0
    while start < end:
        start = start + datetime.timedelta(days=1)
        if start.weekday() not in [5, 6]:
            wd += 1
    return wd

def help():
    output("===========================================================")
    output("help : print help menu")
    output("getstock: get latest stock list")
    output("top [end date] [working days] : find the the most frequently recomanded  stock list")
    output("    [end date]: end date (YYMMDD) like 20180101 ")
    output("    [working days]: the period of days before the end date")
    output("stock [stock list]: get infomation of the stocks in a stock list")
    output("    [stock list]: a list of several stocks like 0000001,0000002,0000003")
    output("rec [stock number]: get the recommand organization information of a stock")
    output("    [stock number]: a stock number such as 0000001")
    output("rd  [stock number]: get the recommand information of a stock")
    output("    [stock number]: a stock number such as 0000001")
    output("kdj/macd  [stock number]: get the KDJ/MACD index of a stock")
    output("    [stock number]: a stock number such as 0000001")
    output("show [stock number]: show the detail info of a stock")
    output("    [stock number]: a stock number such as 0000001")
    output("save  [file path]: save latest result to a csv file")
    output("    [file path]: a csv file path")
    output("settoprec  [top recommend count]: set max top recommend stock count")
    output("    [top recommend count]: the number for max top recommend stock count, default is 20.")
    output("===========================================================")

def list_add_uniqe_tuple(list, tuple):
    found = False
    for l in list:
        all_equal = True
        for i in range(len(tuple)):
            if l[i] != tuple[i]:
                all_equal = False
                break
        if all_equal == True:
            found = True
            break
    if found == False:
        list.append(tuple)
    return list


def top_recommend(end_date=datetime.datetime.now().strftime('%Y%m%d'), workingdays=3):
    current = datetime.datetime.strptime(end_date, '%Y%m%d')
    start_date = current
    stock_ref = {}
    rec_details = {}
    while get_working_days(start_date, current) < workingdays:
        csv_file = const.RECORDS_CSV.replace("DATEYYMMDD", start_date.strftime('%Y-%m-%d'))
        if os.path.exists(csv_file):
            log("parsing the csv " + csv_file)
            ll = read_listlist_csv(csv_file)
            for l in ll:
                s = ws_base.STOCK(l)
                if s.get_stocknum() not in stock_ref.keys():
                    stock_ref[s.get_stocknum()] = ws_base.STOCK_REC(s.get_stocknum(), s.get_stockname())
                stock_ref[s.get_stocknum()].add_rec(s.get_date(), s.get_organization())
                if s.get_stocknum() not in rec_details.keys():
                    rec_details[s.get_stocknum()] = [(s.get_reason().strip(), s.get_reason_file())]
                else:
                    rec_details[s.get_stocknum()] = list_add_uniqe_tuple(rec_details[s.get_stocknum()],
                                                                         (s.get_reason().strip(), s.get_reason_file()))
        start_date = start_date + datetime.timedelta(days=-1)
    final = []
    rec_org = {}
    for k, v in stock_ref.items():
        if v.get_rec_count() > 0:
            temp = []
            temp.append(v.get_stocknum())
            temp.append(v.get_stockname())
            temp.append(v.get_rec_count())
            final.append(tuple(temp))
            rec_org[k] = sorted(v.get_rec(), key=lambda rec: rec[0], reverse=True)
            if len(final) == const.TOP_REC:
                break
    final = sorted(final, key=lambda stock_rec: stock_rec[2], reverse=True)
    output("end date: " + end_date + "    working days:" + str(workingdays))
    output("")
    n = 1
    output("%-4s\t%-8s\t%-10s\t%-4s\t" % ("编号", "股票编码", "股票名称", "推荐次数"))
    for r in final:
        output("%-4s\t%-8s\t%-10s\t%-4s\t" % (n, r[0], r[1], str(r[2])))
        n += 1
    output("")
    return [final, rec_org, rec_details]

def show_stock_details(stock_num_list):
    sr = []
    stock_list = get_stock_list.get_existing_stock_list()
    for r in stock_num_list:
        temp = []
        temp.append(r)
        if r in stock_list.keys():
            temp.append(stock_list[r])
        else:
            temp.append("NA")
        basic = get_report_basic.get_stock_basic(r)
        temp.append(basic["pb"])
        temp.append(basic["pe"])
        temp = temp + list(get_history_data_and_quota(r, "D", get_quota).values())
        temp = temp + list(get_history_data_and_quota(r, "W", get_quota, k_list=const.WEEK_LIST).values())
        temp = temp + list(get_history_data_and_quota(r, "M", get_quota, k_list=const.MONTH_LIST).values())
        sr.append(tuple(temp))
    # sr.insert(0,
    #          ["股票编码", "股票名称", "市盈率", "市净率", "涨(3天)", "涨(5天)", "涨(10天)", "涨(3周)", "涨(5周)", "涨(10周)", "涨(3月)", "涨(6月)",
    #           "涨(12月)"])
    return sr


def get_kdjmacd(s):
    get_history_data_and_quota(s, "D", getKDJMacdBrandistock, k_list="日")
    get_history_data_and_quota(s, "W", getKDJMacdBrandistock, k_list="周")
    get_history_data_and_quota(s, "M", getKDJMacdBrandistock, k_list="月")


def show_tushare(s):
    k_index = None
    i = 0
    while i <= 5 and k_index is None:
        try:
            i = i + 1
            last_day = datetime.datetime.now()
            start_day = last_day + datetime.timedelta(days=-100)
            k_index = ts.get_k_data(s, start=start_day.strftime('%Y-%m-%d'),
                                    end=last_day.strftime('%Y-%m-%d'))
            k_index = k_index[::-1]
        except BaseException as e:
            log(e)
            if k_index is None:
                log("show_tushare retrying......" + str(i))
    output(k_index)
