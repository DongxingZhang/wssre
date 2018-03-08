# coding : UTF-8

import datetime

from bs4 import BeautifulSoup

import funcset
import get_stock_list


def get_51pdf(url, html_text, start_date, end_date, stock_list):
    final = {}
    stop = False
    try:
        bs = BeautifulSoup(html_text, "html.parser")  # 创建BeautifulSoup对象
        body = bs.body  # 获取body部分
        data = body.find('div', {'class': 'morelist'})  # 找到class为morelist的div
        table = data.find('table')  # 获取tbody部分
        tr = table.find_all("tr")
        org_list = get_stock_list.get_existing_org_list()
        if len(tr) == 0:
            return [final, True]
        for item in tr:
            td = item.find_all("td")
            if len(td) != 4:
                continue
            aa = td[1].find("a")
            if True:
                temp_date = td[2].text.strip()
                temp_date = temp_date[0:4] + "-" + temp_date[4:6] + "-" + temp_date[6:8]
                aarray = aa.text.strip().split("-", 1)
                if len(aarray) == 1:
                    funcset.log("something wrong on: " + aa.text)
                    continue
                temp_organization = aarray[0].strip()
                temp_organization = get_stock_list.check_valid_org_num(org_list, temp_organization)
                if temp_organization is None:
                    temp_organization = aarray[0].strip()
                    funcset.log("unsupported organization: " + temp_organization)
                sa = get_stock_list.check_stock_exists_in_string(stock_list, aarray[1].strip(), url)
                if len(sa) == 0:
                    continue
                report_date = datetime.datetime.strptime(temp_date, "%Y-%m-%d")
                stop = report_date < start_date
                if report_date >= start_date and report_date <= end_date:
                    if temp_date not in final.keys():
                        final[temp_date] = []
                    for s in sa:
                        s.set_organization(temp_organization)
                        s.set_date(temp_date)
                        s.set_from("51pdf")
                        final[temp_date].append(s)
    except Exception as e:
        funcset.log(url + "崩溃了")
        funcset.log(e)
    return [final, stop]


def generate_report(start_date, end_date, stock_list):
    return funcset.generate_report_1("http://www.51pdf.com.cn/report_gg_pPAGENUMBER/", get_51pdf, "utf-8", stock_list,
                                     start_date, end_date)
