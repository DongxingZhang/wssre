# coding : UTF-8

import csv
import os

from bs4 import BeautifulSoup

import const
import funcset
from ws_base import WS, STOCK


# funcset.log(sys.getfilesystemencoding())

def get_stock(html_text, start_date, end_date):
    final = []
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
                final.append(temp)
    funcset.write_listlist_csv(const.STOCK_LIST_CSV, 'w', final)
    return final


def get_stock_list():
    ws = WS('http://quote.eastmoney.com/stock_list.html', get_stock, encoding="GBK")
    stock_list = ws.get_data()


def check_stock_exists_in_paragraph(stock_dict, para, title, file_path):
    l = len(para)
    sr = []
    rec = ['推荐', '增持', '买入', '关注', '增长', '受益', '突破', '领先', '突出', '优势', '上涨', '加速']
    para_array = para.split("。")
    para_array1 = []
    for p in para_array:
        p_array = p.split(".")
        if len(p_array) > 0:
            para_array.remove(p)
            para_array1 = para_array1 + p_array
    para_array = para_array + para_array1
    para_array.append("推荐" + title)

    for p in para_array:
        for r in rec:
            if p.find(r) > -1:
                sr = sr + check_stock_exists_in_string(stock_dict, p, file_path)

    sr = list({}.fromkeys(sr).keys())
    return sr


def get_existing_stock_list():
    stock = {}
    if not os.path.exists(const.STOCK_LIST_CSV):
        get_stock_list()
    with open(const.STOCK_LIST_CSV, 'r', errors='ignore', newline='') as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            if row[0] not in stock.keys() and check_valid_stock_num(row[0]):
                stock[row[0]] = row[1]
        f.close()
    return stock


def get_existing_org_list():
    org_list = {}
    with open(const.ORG_LIST_CSV, 'r', errors='ignore', newline='') as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            if len(row) == 2:
                org_list[row[0]] = row[1]
        f.close()
    return org_list


def check_valid_stock_num(stocknum):
    return stocknum.find("60") == 0 or stocknum.find("30") == 0 or stocknum.find("00") == 0


def check_stock_exists_in_string(stock_dict, string, file_path):
    s = []
    for k, v in stock_dict.items():
        if string.find(k) > -1 or string.find(v) > -1:
            s.append(STOCK(["", "", k, v, string, file_path, "", ""]))
    return s


def check_valid_org_num(org_list, string):
    for id, org in org_list.items():
        if string.find(org) > -1 or org.find(string) > -1:
            return org
    return None


if __name__ == '__main__':
    get_stock_list()
