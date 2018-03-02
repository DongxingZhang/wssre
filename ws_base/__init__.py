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
    def __init__(self, stock_num, stock_name, stock_rec_count, stock_rec_org):
        self.stock_num = stock_num
        self.stock_name = stock_name
        self.stock_rec_count = stock_rec_count
        self.stock_rec_org = stock_rec_org

    def get_stock_num(self):
        return self.stock_num

    def get_stock_name(self):
        return self.stock_name

    def get_rec_count(self):
        return self.stock_rec_count

    def add_rec_count(self, stock_rec_count):
        self.stock_rec_count = int(self.stock_rec_count) + int(stock_rec_count)

    def get_rec_org(self):
        return self.stock_rec_org

    def set_rec_count(self, stock_rec_count):
        self.stock_rec_count = stock_rec_count

    def set_rec_org(self, stock_rec_org):
        self.stock_rec_org = stock_rec_org

    def add_rec_org(self, stock_rec_org):
        self.stock_rec_org = self.stock_rec_org + stock_rec_org

    def get_string(self):
        return self.get_stock_num() + "," + self.get_stock_name() + "," + str(self.get_rec_count()) + ",\"" + ",".join(
            self.get_rec_org()) + "\""


class STOCK:
    def __init__(self, date, organization, stocknum, stockname, reason, reason_file, sfrom="", type=""):
        self.date = date
        self.organization = organization
        self.stocknum = stocknum
        self.stockname = stockname
        self.reason = reason
        self.reason_file = reason_file
        self.sfrom = sfrom
        self.type = type

    def get_date(self):
        return self.date

    def get_organization(self):
        return self.organization

    def get_stocknum(self):
        return self.stocknum

    def get_stockname(self):
        return self.stockname

    def get_reason(self):
        return self.reason

    def get_reason_file(self):
        return self.reason_file

    def get_from(self):
        return self.sfrom

    def get_type(self):
        return self.type

    def set_date(self, temp_date):
        self.date = temp_date

    def set_organization(self, temp_organization):
        self.organization = temp_organization

    def set_stocknum(self, temp_stocknum):
        self.stocknum = temp_stocknum

    def set_stockname(self, temp_stockname):
        self.stockname = temp_stockname

    def set_reason(self, temp_reason):
        self.reason = temp_reason

    def set_reason_file(self, temp_reason_file):
        self.reason_file = temp_reason_file

    def set_from(self, temp_from):
        self.sfrom = temp_from

    def set_type(self, temp_type):
        self.type = temp_type

    def get_string(self):
        return self.get_date() + "," + self.get_organization() + "," + self.get_stocknum() + "," + self.get_stockname() + "," + self.get_reason() + "," + self.get_reason_file() + "," + self.get_from() + "," + self.get_type()

    def get_array(self):
        return (self.get_date(), self.get_organization(), self.get_stocknum(), self.get_stockname(), self.get_reason(),
                self.get_reason_file(),
                self.get_from(), self.get_type())


class WS:
    def __init__(self, url, get_data_func, stock_list=None, start_date=datetime.datetime.now(),
                 end_date=datetime.datetime.now(), encoding="utf-8"):
        self.url = url
        self.get_data_func = get_data_func
        self.get_content(encoding)
        self.start_date = start_date
        self.end_date = end_date
        self.stock_list = stock_list

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
        return self.get_data_func(self.html, self.start_date, self.end_date, self.stock_list)
