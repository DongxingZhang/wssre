# coding : UTF-8

import csv
import datetime
import logging
import os
import traceback

import tushare as ts

import const
import ws_base


def log(msg):
    print("wssr: " + msg)


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


def getMacdBrandistock(stock_data):
    try:
        stock_data = getStockMacd(stock_data)
        if stock_data['diff'].tolist()[0] > stock_data['dea'].tolist()[0] and stock_data['diff'].tolist()[1] < \
                stock_data['dea'].tolist()[1]:
            return "金叉"
        else:
            return "-"
    except:
        return "-"


def getStockKDJ(stock_data, n=9, n1=3, n2=3):
    stock_length = len(stock_data)
    rsv_list = [0.0 for i in range(stock_length)]
    k_list = [0.0 for i in range(stock_length)]
    d_list = [0.0 for i in range(stock_length)]
    j_list = [0.0 for i in range(stock_length)]
    high_list = stock_data['high'].rolling(window=n, center=False).max().tolist()
    low_list = stock_data['low'].rolling(window=n, center=False).min().tolist()
    # complement the 0:n-1 value due to the rolling max/min method will get these values to nan
    for i in range(1, min(n, stock_length)):
        high_list[i - 1] = max(stock_data['high'][0:i])
        low_list[i - 1] = min(stock_data['low'][0:i])

    rsv_list[0] = (stock_data['close'][0] - low_list[0]) / (high_list[0] - low_list[0]) * 100.0
    k_list[0] = rsv_list[0]
    d_list[0] = rsv_list[0]
    j_list[0] = rsv_list[0]

    for i in range(1, stock_length):
        rsv_list[i] = (stock_data['close'][i] - low_list[i]) / (high_list[i] - low_list[i]) * 100.0
        k_list[i] = (k_list[i - 1] * (n1 - 1) + rsv_list[i]) / n1
        d_list[i] = (d_list[i - 1] * (n2 - 1) + k_list[i]) / n2
        j_list[i] = k_list[i] * 3.0 - d_list[i] * 2.0
    stock_data['k'] = k_list
    stock_data['d'] = d_list
    stock_data['j'] = j_list
    return stock_data


def getKDJBrandistock(stock_data):
    try:
        stock_data = getStockKDJ(stock_data)
        if stock_data['j'].tolist()[0] > stock_data['k'].tolist()[0] and stock_data['j'].tolist()[0] > \
                stock_data['d'].tolist()[0] and stock_data['j'].tolist()[1] < stock_data['k'].tolist()[1] and \
                stock_data['j'].tolist()[1] < stock_data['d'].tolist()[1]:
            return "金叉"
        else:
            return "-"
    except:
        return "-"


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
                stock_rec = ws_base.STOCK_REC(sr[0], sr[1], sr[2], sr[3].split(","))
                report_all[sr[0]] = stock_rec
            else:
                report_all[sr[0]].add_rec_count(sr[2])
                report_all[sr[0]].add_rec_org(sr[3].split(","))
    return report_all


def get_history_data_and_quota(stock_num, k_index, time_list):
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
            quota[str(d)] = str(format((end - start) / start, '.2%')) + "  " + str(d)
    if k_index is None or len(k_index) == 0:
        quota["kdj"] = str(getKDJBrandistock(k_index))
        quota["macd"] = str(getMacdBrandistock(k_index))
    else:
        quota["kdj"] = "-"
        quota["macd"] = "-"
    return quota


def get_day_history_data_and_quota(stock_num, day_list, last_day):
    day_k = None
    i = 0
    while i <= 5 and day_k is None:
        try:
            i = i + 1
            start_day = last_day + datetime.timedelta(days=-100)
            day_k = ts.get_k_data(stock_num, start=start_day.strftime('%Y-%m-%d'), end=last_day.strftime('%Y-%m-%d'))
        except BaseException as e:
            log(e)
            if day_k is None:
                log("get_day_history_data_and_quota retry......" + str(i))
    return get_history_data_and_quota(stock_num, day_k, day_list)


def get_week_history_data_and_quota(stock_num, week_list, last_day):
    week_k = None
    i = 0
    while i <= 5 and week_k is None:
        try:
            i = i + 1
            start_day = last_day + datetime.timedelta(days=-100)
            week_k = ts.get_k_data(stock_num, ktype='W', start=start_day.strftime('%Y-%m-%d'),
                                   end=last_day.strftime('%Y-%m-%d'))
        except BaseException as e:
            log(e)
            if week_k is None:
                log("get_week_history_data_and_quota retry......" + str(i))
    return get_history_data_and_quota(stock_num, week_k, week_list)


def get_month_history_data_and_quota(stock_num, month_list, last_day):
    month_k = None
    i = 0
    while i <= 5 and month_k is None:
        try:
            i = i + 1
            start_day = last_day + datetime.timedelta(days=-100)
            month_k = ts.get_k_data(stock_num, ktype='M', start=start_day.strftime('%Y-%m-%d'),
                                    end=last_day.strftime('%Y-%m-%d'))
        except BaseException as e:
            log(e)
            if month_k is None:
                log("get_month_history_data_and_quota retry......" + str(i))
    return get_history_data_and_quota(stock_num, month_k, month_list)
