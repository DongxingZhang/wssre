# coding : UTF-8

import datetime

from bs4 import BeautifulSoup

import funcset
import get_stock_list
import ws_base
import wssrdb


def get_sina_finance_page(url, html_text, start_date, end_date, stock_dict, org_dict):
    sa = []
    cont = ""
    h1 = ""
    try:
        bs = BeautifulSoup(html_text, "html.parser")
        body = bs.body
        blk_02 = body.find('div', {'class': 'blk_02'})
        data = blk_02.find('div', {'class': 'blk_container'})
        pa = data.find('p')
        title = body.find('div', {'class': 'content'})
        h1 = title.find("h1")
        cont = pa.text.replace(u'\xa0', u' ').strip()
        sa = get_stock_list.check_stock_exists_in_paragraph(stock_dict, cont, h1.text.strip(), url)
    except Exception as e:
        funcset.log(url + "崩溃了")
        funcset.log(e)
    return sa


def get_sina_finance(url, html_text, start_date, end_date, stock_dict, org_dict):
    final = []
    stop = False
    bs = BeautifulSoup(html_text, "html.parser")
    body = bs.body
    table = body.find('table', {'class': 'tb_01'})
    tr = table.find_all("tr")
    if len(tr) == 3:
        return [final, True]
    try:
        for item in tr:
            td = item.find_all("td")
            if len(td) != 6:
                continue
            temp_date = td[3].text
            report_date = datetime.datetime.strptime(temp_date, "%Y-%m-%d")
            stop = report_date < start_date
            if report_date < start_date or report_date > end_date:
                break
            aa = item.find_all("a")
            ws = ws_base.WS(aa[0]['href'], get_sina_finance_page, start_date, end_date, stock_dict, org_dict,
                            encoding="GBK")
            report = ws.get_data()
            funcset.log("读取URL:" + aa[0]['href'] + "(" + str(len(report)) + ")")
            organization = td[4].text.strip()
            orgid = get_stock_list.check_valid_org_num(org_dict, organization)
            if orgid is None:
                funcset.log("Add new org: " + organization)
                wssrdb.insert_org(organization)
                orgid = wssrdb.get_orgid(organization)
                org_dict[orgid] = organization  # add new org into the org_dict
            for r in report:
                r.set_date(temp_date.strip())
                r.set_orgid(orgid)
                r.set_source("sina finance")
                final.append(r)
        wssrdb.insert_stock_records(final)
    except Exception as e:
        funcset.log(url + "崩溃了")
        funcset.log(e)
    return [final, stop]


def generate_report(start_date, end_date, stock_dict, org_dict):
    return funcset.generate_report_1(
        "http://vip.stock.finance.sina.com.cn/q/go.php/vReport_List/kind/lastest/index.phtml?p=PAGENUMBER/",
        get_sina_finance, "GBK", start_date, end_date, stock_dict, org_dict)
