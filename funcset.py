# coding : UTF-8

import csv
import datetime
import os

import pylab as pl
import tushare as ts

import const
import get_report_basic
import ws_base
import wssrdb


def log(msg):
    write_str_to_file(const.LOG_FILE, "WSSR(" + str(datetime.datetime.now()) + "): " + str(msg) + "\n", "a")


def output(msg, end='\r'):
    print(msg, end)


def write_str_to_file(file_name, contents, mode="w"):
    f = open(file_name, mode)
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
        return [[], [], []]
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
    return [date_list, kdj_list, macd_list]


def write_listlist_csv(filename, mode, listlist):
    with open(filename, mode, errors='ignore', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(listlist)
        f.close()
        log(filename + "写入完毕!")


def read_listlist_csv(filename):
    listlist = []
    with open(filename, 'r', errors='ignore', newline='') as f:
        f_csv = csv.reader(f)
        listlist = [row for row in f_csv]
        f.close()
    return listlist


def generate_report_1(url, get_data_func, encoding, start_date, end_date, stock_dict, org_dict):
    stop = False
    pageno = 1
    total_count = 0
    while not stop:
        newurl = url.replace("PAGENUMBER", str(pageno))
        ws = ws_base.WS(newurl, get_data_func, start_date, end_date, stock_dict, org_dict, encoding)
        [get_report, stop] = ws.get_data()
        log("读取URL:" + newurl + " with " + encoding + "(" + str(
            len(get_report)) + ")")
        pageno += 1
        total_count += len(get_report)
    return total_count


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
                log("获取历史......" + str(i))
    return func([k_index, k_list])


def get_working_days(start, end):
    wd = 0
    while start < end:
        start = start + datetime.timedelta(days=1)
        if start.weekday() not in [5, 6]:
            wd += 1
    return wd


def help():
    output("=============================================================================================")
    output("help :打印帮助。")
    output("getstock:获取A股票列表")
    output("top [结束时期，如20180305] [工作日天数，如3]: 查找从[结束日期]开始往前[工作日天数]时间内推荐次数最多")
    output("    的股票 ")
    output("stock [股票列表]:获取[股票列表]指标信息。")
    output("     [股票列表]: 如0000001,0000002,0000003。")
    output("trend [股票代码,如000001] [结束时期，如20180305] [工作日天数，如5] [时间段，月为20，周为5，日为1]:")
    output("     输出股票在一段时间内的推荐趋势")
    output("rec [股票编号]:获取这个股票的相关推荐信息")
    output("rd  [股票代码，如000001]:获取股票推荐信息和网页。")
    output("kdj/macd  [股票代码,如000001]: 获取MACD/KDJ金叉信息")
    output("show [股票代码,如000001]: 打印来自tushare的k线数据")
    output("save  [文件路径]: 保存最后的结果到csv文件。")
    output("settoprec  [top推荐股票数量]: 设置top推荐股票数量")
    output("==========================================================================================")


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


def top_recommend(stock_dict, org_dict,
                  end_date=(datetime.datetime.now() + datetime.timedelta(days=-1)).strftime('%Y%m%d'), workingdays=5):
    end_date = datetime.datetime.strptime(end_date, '%Y%m%d')
    start_date = end_date
    while get_working_days(start_date, end_date) < workingdays:
        start_date = start_date + datetime.timedelta(days=-1)
    return wssrdb.top_recommend(stock_dict, start_date, end_date, const.TOP_REC)


def show_stock_details(stock_num_list, stock_list):
    sr = []
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
    return sr


def get_kdjmacd(s):
    results = {}
    results["日"] = get_history_data_and_quota(s, "D", getKDJMacdBrandistock, k_list="日")
    results["周"] = get_history_data_and_quota(s, "W", getKDJMacdBrandistock, k_list="周")
    results["月"] = get_history_data_and_quota(s, "M", getKDJMacdBrandistock, k_list="月")
    return results


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
                log("tushare数据获取中......" + str(i))
    output(k_index)


def show_trend(stock_id, stock_name,
               end_date=(datetime.datetime.now() + datetime.timedelta(days=-1)).strftime('%Y%m%d'), working_days=200,
               step=10):
    end_date = datetime.datetime.strptime(end_date, '%Y%m%d')
    start_date = end_date
    while get_working_days(start_date, end_date) < working_days:
        start_date = start_date + datetime.timedelta(days=-1)
    start_date = start_date + datetime.timedelta(days=-(step - 1))
    k_dict = {}
    k_index = ts.get_k_data(stock_id, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
    for i in range(0, len(k_index)):
        k_dict[list(k_index['date'])[i]] = list(k_index['close'])[i]
    trend_dict = wssrdb.get_trend(stock_id, start_date, end_date)
    date_list = sorted(list(k_dict.keys()) + [item for item in trend_dict.keys() if item not in k_dict.keys()])
    k_list = []
    trend_list = []
    for r in date_list:
        if r in k_dict.keys():
            k_list.append(k_dict[r])
        elif len(k_list) > 0:
            k_list.append(k_list[-1])
        else:
            k_list.append(0.0)
        if r in trend_dict.keys():
            trend_list.append(trend_dict[r])
        else:
            trend_list.append(0)
    #####################################################
    if step > 1:  # 大于1天
        date_list_2 = []
        k_list_2 = []
        trend_list_2 = []
        k_avg = 0.0
        trend_sum = 0
        for i in range(0, len(date_list)):
            if (i + 1) % step > 0:
                k_avg += k_list[i]
                trend_sum += trend_list[i]
            else:
                date_list_2.append(date_list[i])
                k_list_2.append(k_avg / step)
                trend_list_2.append(trend_sum)
                k_avg = 0.0
                trend_sum = 0
        date_list = date_list_2
        k_list = k_list_2
        trend_list = trend_list_2
    #####################################################
    date_list = [d.replace("-", "\n") for d in date_list]
    fig, pl1 = pl.subplots()
    pl1.plot(date_list, k_list, label=u"收盘价", color="blue", linewidth=2.5)
    pl1.set_ylabel(u"收盘价", fontsize=18, color="blue")
    for label in pl1.get_yticklabels():
        label.set_color("blue")
    pl2 = pl1.twinx()
    pl2.plot(date_list, trend_list, label=u"研报推荐", color="red", linewidth=2.5)
    pl2.set_ylabel(u"研报推荐", fontsize=18, color="red")
    for label in pl2.get_yticklabels():
        label.set_color("red")
    pl2.set_xlabel(u'时间', fontsize=18, color="black")
    pl.title(stock_name + "[" + stock_id + "]")
    pl.legend()
    pl.show()
