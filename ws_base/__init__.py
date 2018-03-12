# coding : UTF-8

import datetime
import http.client
import random
import socket
import time
from multiprocessing import Process

import requests


class PROCESS(Process):
    def __init__(self, name, process, para_arr):
        super().__init__()
        self.running = True
        self.name = name
        self.process = process
        self.para_arr = para_arr

    def run(self):
        print("run %s with %s process start " % (self.name, ".".join([str(a) for a in self.para_arr])))
        self.process(self.para_arr)
        self.running = False
        print("run %s with %s process end   " % (self.name, ".".join([str(a) for a in self.para_arr])))

    def get_running(self):
        return self.running


class STOCK_REC:
    def __init__(self, stock_num, stock_name):
        self.stock_num = stock_num
        self.stock_name = stock_name
        self.stock_rec_count = 0
        self.stock_rec = []

    def get_stocknum(self):
        return self.stock_num

    def get_stockname(self):
        return self.stock_name

    def get_rec_count(self):
        return self.stock_rec_count

    def get_rec(self):
        return self.stock_rec

    def set_rec_count(self, stock_rec_count):
        self.stock_rec_count = stock_rec_count

    def add_rec(self, stock_rec_date, stock_rec_org):
        found = False
        for s in self.stock_rec:
            if s[0] == stock_rec_date and (s[1].find(stock_rec_org) >= 0 or stock_rec_org.find(s[1]) >= 0):
                found = True
                break
        if not found:
            self.stock_rec.append(tuple([stock_rec_date, stock_rec_org]))
            self.stock_rec_count = len(self.stock_rec)

    def get_string(self):
        return self.get_stocknum() + "," + self.get_stockname() + "," + str(self.get_rec_count())


class STOCK_RECORD:
    def __init__(self, list):
        self.date = list[0]
        self.stockid = list[1]
        self.orgid = list[2]
        self.reason = list[3]
        self.url = list[4]
        self.source = list[5]

    def get_date(self):
        return self.date

    def get_stockid(self):
        return self.stockid

    def get_orgid(self):
        return self.orgid

    def get_reason(self):
        return self.reason

    def get_url(self):
        return self.url

    def get_source(self):
        return self.source

    def set_date(self, temp_date):
        self.date = temp_date

    def set_orgid(self, orgid):
        self.orgid = orgid

    def set_stockid(self, stockid):
        self.stockid = stockid

    def set_reason(self, reason):
        self.reason = reason

    def set_url(self, url):
        self.url = url

    def set_source(self, source):
        self.source = source

    def get_string(self):
        return self.get_date() + "," + self.get_stockid() + "," + self.get_orgid() + "," + self.get_reason() + "," + self.get_url() + "," + self.get_source()

    def get_array(self):
        return (self.get_date(), self.get_stockid(), self.get_orgid(), self.get_reason(), self.get_reason(),
                self.get_url(), self.get_source())


class WS:
    def __init__(self, url, get_data_func, start_date=datetime.datetime.now(),
                 end_date=datetime.datetime.now(), stock_dict=None, org_dict=None, encoding="utf-8"):
        self.url = url
        self.get_data_func = get_data_func
        self.get_content(encoding)
        self.start_date = start_date
        self.end_date = end_date
        self.stock_dict = stock_dict
        self.org_dict = org_dict

    def get_content(self, encoding, data=None):
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml, text/javascript;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.235'
        }
        timeout = random.choice(range(480, 1080))
        while True:
            try:
                rep = requests.get(self.url, headers=header, timeout=timeout)
                rep.encoding = encoding
                # req = urllib.request.Request(self.url, data, header)
                # response = urllib.request.urlopen(req, timeout=timeout)
                # html1 = response.read().decode('UTF-8', errors='ignore')
                # response.close()
                break
            # except urllib.request.HTTPError as e:
            #         print( '1:', e)
            #         time.sleep(random.choice(range(5, 10)))
            #
            # except urllib.request.URLError as e:
            #     print( '2:', e)
            #     time.sleep(random.choice(range(5, 10)))
            except socket.timeout as e:
                print('3:', e)
                time.sleep(random.choice(range(8, 15)))

            except socket.error as e:
                print('4:', e)
                time.sleep(random.choice(range(20, 60)))

            except http.client.BadStatusLine as e:
                print('5:', e)
                time.sleep(random.choice(range(30, 80)))

            except http.client.IncompleteRead as e:
                print('6:', e)
                time.sleep(random.choice(range(5, 15)))

            except BaseException as e:
                print('7:', e)
                time.sleep(random.choice(range(5, 15)))

        self.html = rep.text

    def get_data(self):
        return self.get_data_func(self.url, self.html, self.start_date, self.end_date, self.stock_dict, self.org_dict)
