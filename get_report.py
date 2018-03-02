# coding : UTF-8

import datetime

import const
import funcset
import get_report_51pdf
import get_report_51pdf_buy
import get_report_sina_finance
import get_stock_list


def generate_report(start_date, end_date):
    a = {}
    stock_list = get_stock_list.get_existing_stock_list()

    a1 = get_report_51pdf.generate_report(start_date, end_date, stock_list)
    a = funcset.merge_report_records(a, a1)

    a2 = get_report_51pdf_buy.generate_report(start_date, end_date, stock_list)
    a = funcset.merge_report_records(a, a2)

    a3 = get_report_sina_finance.generate_report(start_date, end_date, stock_list)
    a = funcset.merge_report_records(a, a3)

    return a


def get_report():
    last_day = funcset.read_lastday()
    today = datetime.datetime.now()
    records = generate_report(last_day, today)
    for temp_date, sr in records.items():
        funcset.write_listlist_csv(const.RECORDS_CSV.replace("DATEYYMMDD", temp_date), 'w', [r.get_array() for r in sr])
    # funcset.write_lastday(today + datetime.timedelta(days=-1))
