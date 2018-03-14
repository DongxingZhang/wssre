# coding : UTF-8

import datetime

import funcset
import get_report_51pdf
import get_report_51pdf_buy
import get_report_sina_finance
import wssrdb


def generate_report(start_date, end_date, stock_dict, org_dict):
    total_count = 0
    wssrdb.delete_stock_records(start_date, end_date)
    total_count += get_report_51pdf.generate_report(start_date, end_date, stock_dict, org_dict)
    total_count += get_report_51pdf_buy.generate_report(start_date, end_date, stock_dict, org_dict)
    total_count += get_report_sina_finance.generate_report(start_date, end_date, stock_dict, org_dict)
    return total_count

def get_report(stock_dict, org_dict):
    last_day = funcset.read_lastday()
    today = datetime.datetime.now()
    if today.year != last_day.year or today.month != last_day.month or today.day != last_day.day:
        funcset.output("数据初始化中......")
        total_count = generate_report(last_day, today, stock_dict, org_dict)
        funcset.write_lastday(today)
        funcset.output("数据初始化完毕。共读取" + str(total_count) + "条记录。")
