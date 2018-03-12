# coding : UTF-8

import datetime

import funcset
import get_report_51pdf
import get_stock_list


def generate_report(start_date, end_date):
    stock_dict = get_stock_list.get_existing_stock_list()
    org_dict = get_stock_list.get_existing_org_list()
    get_report_51pdf.generate_report(start_date, end_date, stock_dict, org_dict)

    # a2 = get_report_51pdf_buy.generate_report(start_date, end_date, stock_list)
    # a = funcset.merge_report_records(a, a2)

    # a3 = get_report_sina_finance.generate_report(start_date, end_date, stock_list)
    # a = funcset.merge_report_records(a, a3)

    return


def get_report():
    last_day = funcset.read_lastday()
    today = datetime.datetime.now()
    if today.year != last_day.year or today.month != last_day.month or today.day != last_day.day:
        funcset.output("数据初始化中......")
        records = generate_report(last_day, today)
        # funcset.write_lastday(today)
        funcset.output("数据初始化完毕。")
