# coding : UTF-8

from bs4 import BeautifulSoup

import funcset
import ws_base


def get_data_func(url, html_text, start_date, end_date):
    final = {}
    bs = BeautifulSoup(html_text, "lxml")
    body = bs.body
    div = body.find('div', {'class': 'finance_overview'})
    div_tabs = div.find('div', {'class': 'tabs'})
    div_table = div.find('div', {'class': 'cont data_table L_data_table'})
    div_tabs_date = div_tabs.find_all("div")
    data_array = [div.text for div in div_tabs_date]
    tr_array = div_table.find_all("tr")

    gain_each_share_cn = tr_array[0].find("th").text
    netasset_each_share_cn = tr_array[1].find("th").text
    cashflow_each_share_cn = tr_array[2].find("th").text
    netasset_gain_rate_cn = tr_array[3].find("th").text
    undistributedprofit_each_share_cn = tr_array[4].find("th").text
    capitalfunding_each_share_cn = tr_array[5].find("th").text

    gain_each_share = [td.text for td in tr_array[0].find_all("td")]
    netasset_each_share = [td.text for td in tr_array[1].find_all("td")]
    cashflow_each_share = [td.text for td in tr_array[2].find_all("td")]
    netasset_gain_rate = [td.text for td in tr_array[3].find_all("td")]
    undistributedprofit_each_share = [td.text for td in tr_array[4].find_all("td")]
    capitalfunding_each_share = [td.text for td in tr_array[5].find_all("td")]

    ges = {}
    nes = {}
    ces = {}
    ngr = {}
    ues = {}
    cfes = {}
    for i in range(len(data_array)):
        ges[data_array[i]] = str(gain_each_share[i])
        nes[data_array[i]] = str(netasset_each_share[i])
        ces[data_array[i]] = str(cashflow_each_share[i])
        ngr[data_array[i]] = str(netasset_gain_rate[i])
        ues[data_array[i]] = str(undistributedprofit_each_share[i])
        cfes[data_array[i]] = str(capitalfunding_each_share[i])
    final[gain_each_share_cn] = ges
    final[netasset_each_share_cn] = nes
    final[cashflow_each_share_cn] = ces
    final[netasset_gain_rate_cn] = ngr
    final[undistributedprofit_each_share_cn] = ues
    final[capitalfunding_each_share_cn] = cfes
    return final


def get_stock_basic_summary(stock_num):
    if stock_num.find("00") == 0 or stock_num.find("30") == 0:
        stock_num = 'sz' + stock_num
    elif stock_num.find("60") == 0:
        stock_num = 'sh' + stock_num
    url = "http://finance.sina.com.cn/realstock/company/" + stock_num + "/nc.shtml"
    funcset.log("reading " + url)
    ws = ws_base.WS(url, get_data_func, None, None, None, "GBK")
    return ws.get_data()
