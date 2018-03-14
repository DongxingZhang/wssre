# coding : UTF-8

from bs4 import BeautifulSoup

import funcset
import wssrdb
from ws_base import WS, STOCK_RECORD


def get_stock(url, html_text, start_date, end_date, stock_list):
    final = {}
    try:
        bs = BeautifulSoup(html_text, "html.parser")  # 创建BeautifulSoup对象
        body = bs.body  # 获取body部分
        data = body.find('div', {'id': 'quotesearch'})  # 找到id为quotesearch的div
        ul = data.find_all('ul')  # 获取ul部分
        for site in ul:
            li = site.find_all('li')  # 获取所有的li
            for stock in li:
                a = stock.find_all("a")
                for valid_item in a:
                    temp = []
                    vi = valid_item.string.split("(")
                    if len(vi) == 2:
                        temp.append(vi[1].replace(")", "").strip())
                        temp.append(vi[0].strip())
                    final[temp[0]] = temp[1]
        wssrdb.cleanup_stock()
        wssrdb.insert_stock(final)
    except Exception as e:
        funcset.log("Error happened " + str(e))
    return final


def get_stock_list():
    ws = WS('http://quote.eastmoney.com/stock_list.html', get_stock, None, None, None, encoding="GBK")
    stock_list = ws.get_data()
    return stock_list


def get_existing_stock_list():
    stock_list = wssrdb.get_stock()
    if len(stock_list) < 100:
        stock_list = get_stock_list()
    return stock_list


def get_existing_org_list():
    return wssrdb.get_org()


def merge_stock_records(stock_record1, stock_record2):
    sr = stock_record1.copy()
    for sr2 in stock_record2:
        found = False
        for sr1 in stock_record1:
            if sr1.get_date() == sr2.get_date() and sr1.get_stockid() == sr2.get_stockid() and \
                    sr1.get_orgid() == sr2.get_orgid() and sr1.get_reason() == sr2.get_reason() and \
                    sr1.get_url() == sr2.get_url():
                found = True
                break
        if not found:
            sr.append(sr2)
    return sr


def check_stock_exists_in_paragraph(stock_dict, para, title, file_path):
    l = len(para)
    sr = []
    rec = ['推荐', '增持', '买入', '关注', '增长', '受益', '突破', '领先', '突出', '优势', '上涨', '加速', '加快']
    para_array = para.split("。")
    para_array1 = []
    for p in para_array:
        p_array = p.split(".")
        if len(p_array) > 0:
            para_array.remove(p)
            para_array1 = para_array1 + p_array
    para_array = para_array + para_array1
    para_array.append("推荐:" + title)

    for p in para_array:
        for r in rec:
            if p.find(r) > -1:
                sr = merge_stock_records(sr, check_stock_exists_in_string(stock_dict, p, file_path))
    return sr

def check_stock_exists_in_string(stock_dict, string, url):
    s = []
    for k, v in stock_dict.items():
        if string.find(k) > -1 or string.find(v) > -1:
            if len(string) > 5000:
                string = string[0:5000]
            s.append(STOCK_RECORD(["", k, 0, string, url, ""]))
    return s


def check_valid_org_num(org_dict, string):
    for id, org in org_dict.items():
        if string.find(org) > -1 or org.find(string) > -1:
            return id
    return None

if __name__ == '__main__':
    get_stock_list()
