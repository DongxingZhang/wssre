# coding : UTF-8

from bs4 import BeautifulSoup

import funcset
import ws_base


def get_data_func(html_text, start_date, end_date):
    final = {}
    try:
        bs = BeautifulSoup(html_text, "html.parser")
        body = bs.body
        div = body.find('div', {'class': 'col-2 fr'})
        ul = div.find_all("ul")
        if len(ul) >= 3:
            li = ul[2].find_all("li")
            if len(li) >= 4:
                final["turnover"] = li[0].find_all("span")[1].text
                final["swing"] = li[2].find_all("span")[1].text
                final["pb"] = li[1].find_all("span")[1].text
                final["pe"] = li[3].find_all("span")[1].text
    except BaseException as e:
        final["turnover"] = ""
        final["swing"] = ""
        final["pb"] = ""
        final["pe"] = ""
    return final


def get_stock_basic(stock_num):
    if stock_num.find("00") == 0 or stock_num.find("30") == 0:
        stock_num = 'sz' + stock_num
    elif stock_num.find("60") == 0:
        stock_num = 'sh' + stock_num
    url = "http://gu.qq.com/" + stock_num + "/gp"
    funcset.log("reading " + url)
    ws = ws_base.WS(url, get_data_func, None, None, "utf-8")
    return ws.get_data()
