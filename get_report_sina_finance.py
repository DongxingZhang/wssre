# coding : UTF-8

import datetime

from bs4 import BeautifulSoup

import funcset
import get_stock_list
import ws_base


def get_sina_finance_page(url, html_text, start_date, end_date, stock_list):
    bs = BeautifulSoup(html_text, "html.parser")
    body = bs.body
    blk_02 = body.find('div', {'class': 'blk_02'})
    data = blk_02.find('div', {'class': 'blk_container'})
    pa = data.find('p')
    title = body.find('div', {'class': 'content'})
    h1 = title.find("h1")
    cont = pa.text.replace(u'\xa0', u' ').strip()
    creab = body.find('div', {'class': 'creab'})
    span = creab.find_all("span")
    # data = str(data).replace("\xa0", "")
    # save_path = const.WEBCACHE_DIR + os.sep + span[len(span) - 1].text.strip()[::-1][0:10][::-1].replace("-", "")
    # file_path = funcset.get_webcache_hash_file_name(data, span[
    #                                                                                                                    len(
    #                                                                                                                        span) - 1].text.strip()[
    #                                                                                                                ::-1][
    #                                                       0:10][
    #                                                       ::-1].replace(
    #     "-", ""))
    # if not os.path.exists(save_path):
    #     os.mkdir(save_path)
    # funcset.write_str_to_file(file_path, data)
    sa = get_stock_list.check_stock_exists_in_paragraph(stock_list, cont, h1.text.strip(), url)
    return sa


def get_sina_finance(url, html_text, start_date, end_date, stock_list):
    final = {}
    stop = False
    bs = BeautifulSoup(html_text, "html.parser")
    body = bs.body
    table = body.find('table', {'class': 'tb_01'})
    tr = table.find_all("tr")
    org_list = get_stock_list.get_existing_org_list()
    if len(tr) == 3:
        return [final, True]
    for item in tr:
        # try:
        if True:
            aa = item.find_all("a")
            td = item.find_all("td")
            if len(td) != 6:
                continue
            temp_org = td[4].text.strip()
            temp_org = get_stock_list.check_valid_org_num(org_list, temp_org)
            if temp_org is None:
                temp_org = td[4].text.strip()
                funcset.log("unsupported organization: " + temp_org.strip())
            # funcset.log(temp_org)
            temp_date = td[3].text
            report_date = datetime.datetime.strptime(temp_date, "%Y-%m-%d")
            stop = report_date < start_date
            if report_date < start_date or report_date > end_date:
                break
            temp_reason = td[1].text.strip()
            funcset.log("reading url path: " + aa[0]['href'])
            ws = ws_base.WS(aa[0]['href'], get_sina_finance_page, stock_list, start_date, end_date, encoding="GBK")
            report = ws.get_data()
            if temp_date not in final.keys():
                final[temp_date] = []
            for r in report:
                r.set_date(temp_date.strip())
                r.set_organization(temp_org.strip())
                # r.set_reason(temp_reason.strip())
                r.set_from("sina")
                final[temp_date].append(r)
    return [final, stop]


def generate_report(start_date, end_date, stock_list):
    return funcset.generate_report_1(
        "http://vip.stock.finance.sina.com.cn/q/go.php/vReport_List/kind/lastest/index.phtml?p=PAGENUMBER/",
        get_sina_finance, "GBK", stock_list, start_date, end_date)
