# coding : utf-8

import datetime

import const
import funcset
import get_report_basic
import ws_base

global results


def get_stock_recommand_lastndays(last_day, ndays):
    sr = []
    title = [u"编号", u"名称", u"推荐次数", u"市净率", u"市盈率"]
    title = title + [u"涨(" + str(d) + u"天)" for d in const.DAY_LIST] + ["KDJ金叉", "MACD金叉"]
    title = title + [u"涨(" + str(w) + u"周)" for w in const.WEEK_LIST] + ["KDJ金叉", "MACD金叉"]
    title = title + [u"涨(" + str(m) + u"月)" for m in const.MONTH_LIST] + ["KDJ金叉", "MACD金叉"]
    title.append(u"推荐机构（推荐日期）")
    days_ago = last_day
    total_working_days = 0
    while total_working_days < ndays:
        days_ago = days_ago + datetime.timedelta(days=-1)
        if days_ago.weekday() not in [5, 6]:
            total_working_days = total_working_days + 1
    funcset.log("collecting the data from " + days_ago.strftime('%Y-%m-%d') + " to " + last_day.strftime('%Y-%m-%d'))
    report_all = funcset.load_all_existing_report(days_ago, last_day)
    for r in report_all.values():
        if int(r.get_rec_count()) > 1:
            temp = []
            temp.append(r.get_stock_num())
            temp.append(r.get_stock_name())
            temp.append(int(r.get_rec_count()))
            basic = get_report_basic.get_stock_basic(r.get_stock_num())
            temp.append(basic["pb"])
            temp.append(basic["pe"])
            # basic_summary = get_report_basic_summary.get_stock_basic_summary(r.get_stock_num())
            # financial_overview = "\t\t\t," + "\t,".join(list(list(basic_summary.values())[0].keys())) + "\n"
            # for item, v in basic_summary.items():
            #    financial_overview = financial_overview + item + "\t\t\t," + "\t,".join(v.values()) + "\n"
            # temp.append(financial_overview)
            temp = temp + list(
                funcset.get_day_history_data_and_quota(r.get_stock_num(), last_day).values())
            temp = temp + list(
                funcset.get_week_history_data_and_quota(r.get_stock_num(), last_day).values())
            temp = temp + list(
                funcset.get_month_history_data_and_quota(r.get_stock_num(), last_day).values())
            temp.append(",".join(r.get_rec_org()))
            sr.append(tuple(temp))
    sr = sorted(sr, key=lambda stock: stock[2], reverse=True)
    sr.insert(0, title)
    return sr


def get_statistics():
    p1 = ws_base.PROCESS('get_statistics_by_period_3', get_statistics_func, [3])
    p2 = ws_base.PROCESS('get_statistics_by_period_5', get_statistics_func, [5])
    p3 = ws_base.PROCESS('get_statistics_by_period_10', get_statistics_func, [10])
    p4 = ws_base.PROCESS('get_statistics_by_period_20', get_statistics_func, [20])
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    while p1.get_running() or p2.get_running() or p3.get_running() or p4.get_running():
        pass


def get_statistics_func(para_arr):
    get_statistics_by_period(para_arr[0])
    return


def get_statistics_by_period(ndays):
    funcset.log("get_statistics_by_period start " + str(ndays))
    last_day_report = funcset.read_lastday()
    last_day = funcset.read_lastday(const.LAST_DAY_CSV_DD.replace("DD", str(ndays)))
    while last_day <= last_day_report:
        file_name_postfix = last_day.strftime('%Y-%m-%d')
        dayOfWeek = last_day.weekday()
        if dayOfWeek in [5, 6]:
            funcset.log("weekend, no analysis data.")
            continue
        funcset.write_listlist_csv(
            const.STA_REC_LAST_DAYS_CSV.replace("DATEYYMMDD", file_name_postfix).replace("DD", str(ndays)), "w",
            get_stock_recommand_lastndays(last_day, ndays))
        funcset.write_lastday(last_day, const.LAST_DAY_CSV_DD.replace("DD", str(ndays)))
        last_day += datetime.timedelta(days=1)
    funcset.log("get_statistics_by_period end " + str(ndays))
    return
