# coding : UTF-8

import datetime
import os

from bs4 import BeautifulSoup

import const
import funcset
import get_stock_list


def get_51pdf(html_text, start_date, end_date, stock_list):
    final = {}
    stop = False
    # stock_list = get_stock_list.get_existing_stock_list()
    bs = BeautifulSoup(html_text, "html.parser")  # 创建BeautifulSoup对象
    body = bs.body  # 获取body部分
    data = body.find('div', {'class': 'morelist'})  # 找到class为morelist的div
    html_context = body.find('div', {'class': 'content_left'})
    html_context_date = ""
    file_path = ""
    table = data.find('table')  # 获取tbody部分
    tr = table.find_all("tr")
    org_list = get_stock_list.get_existing_org_list()
    if len(tr) == 0:
        return [final, True]
    if html_context is not None:
        td = tr[0].find_all("td")
        if len(td) == 4:
            html_context = str(html_context).replace("\xa0", "")
            save_path = const.WEBCACHE_DIR + os.sep + td[2].text.strip()
            file_path = funcset.get_webcache_hash_file_name(html_context, td[2].text.strip())
            if not os.path.exists(save_path):
                os.mkdir(save_path)
            funcset.write_str_to_file(file_path, html_context)
    for item in tr:
        td = item.find_all("td")
        if len(td) != 4:
            continue
        aa = td[1].find("a")
        if True:
            temp_date = td[2].text.strip()
            html_context_date = temp_date
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
            sa = get_stock_list.check_stock_exists_in_string(stock_list, aarray[1].strip(), file_path)
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
    return [final, stop]


def generate_report(start_date, end_date, stock_list):
    return funcset.generate_report_1("http://www.51pdf.com.cn/report_gg_pPAGENUMBER/", get_51pdf, "utf-8", stock_list,
                                     start_date, end_date)
