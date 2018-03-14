# coding : UTF-8

import datetime

from bs4 import BeautifulSoup

import funcset
import get_stock_list
import wssrdb


def get_51pdf(url, html_text, start_date, end_date, stock_dict, org_dict):
    final = []
    stop = False
    try:
        bs = BeautifulSoup(html_text, "html.parser")
        body = bs.body
        data = body.find('div', {'class': 'morelist'})
        table = data.find('table')
        tr = table.find_all("tr")
        if len(tr) == 0:
            return True
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
                    org_dict[orgid] = organization
                report_date = datetime.datetime.strptime(temp_date, "%Y-%m-%d")
                stop = report_date < start_date
                if end_date >= report_date >= start_date:
                    for s in sa:
                        s.set_orgid(orgid)
                        s.set_date(temp_date)
                        s.set_source("51pdf stock")
                        final.append(s)
        wssrdb.insert_stock_records(final)
    except Exception as e:
        funcset.log(url + "崩溃了")
        funcset.log(e)
    return [final, stop]


def generate_report(start_date, end_date, stock_dict, org_dict):
    return funcset.generate_report_1("http://www.51pdf.cn/report_gg_pPAGENUMBER/", get_51pdf, "utf-8", start_date,
                                     end_date, stock_dict, org_dict)
