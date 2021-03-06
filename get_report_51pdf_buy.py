# coding : UTF-8

import datetime

from bs4 import BeautifulSoup

import funcset
import get_stock_list
import wssrdb


def get_51pdf_buy(url, html_text, start_date, end_date, stock_dict, org_dict):
    final = []
    stop = False
    try:
        bs = BeautifulSoup(html_text, "html.parser")
        body = bs.body
        data = body.find('div', {'class': 'morelist'})
        table = data.find('table')
        tr = table.find_all("tr")
        org_list = get_stock_list.get_existing_org_list()
        if len(tr) == 2:
            return [final, True]
        for item in tr:
            td = item.find_all("td")
            if len(td) != 4:
                continue
            aa = td[0].find("a")
            if True:
                temp_date = td[3].text.strip()
                temp_date = temp_date[0:4] + "-" + temp_date[4:6] + "-" + temp_date[6:8]
                aarray = aa.text.strip().split("-", 1)
                if len(aarray) == 1:
                    funcset.log("something wrong on: " + aa.text)
                    continue
                sa = get_stock_list.check_stock_exists_in_string(stock_dict, aarray[1].strip(),
                                                                 "http://www.51pdf.cn" + aa["href"])
                if len(sa) == 0:
                    continue
                organization = aarray[0].strip()
                orgid = get_stock_list.check_valid_org_num(org_dict, organization)
                if orgid is None:
                    funcset.log("Add new org: " + organization)
                    wssrdb.insert_org(organization)
                    orgid = wssrdb.get_orgid(organization)
                    org_dict[orgid] = organization  # add new org into the org_dict
                report_date = datetime.datetime.strptime(temp_date, "%Y-%m-%d")
                stop = report_date < start_date
                if end_date >= report_date >= start_date:
                    for s in sa:
                        s.set_orgid(orgid)
                        s.set_date(temp_date)
                        s.set_source("51pdf report")
                        final.append(s)
        wssrdb.insert_stock_records(final)
    except Exception as e:
        funcset.log(url + "崩溃了")
        funcset.log(e)
    return [final, stop]


def generate_report(start_date, end_date, stock_dict, org_dict):
    return funcset.generate_report_1("http://www.51pdf.cn/pj_1_4_PAGENUMBER/", get_51pdf_buy, "utf-8", start_date,
                                     end_date, stock_dict, org_dict)
