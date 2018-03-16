import os

REPORT_DIR = 'report'
STOCK_DIR = 'stock'
TIMESTAP_DIR = 'timestamp'
RECORDS_DIR = 'records'
TMP_DIR = 'tmp'
DB_DIR = 'db'

WSSRDB = DB_DIR + os.sep + 'wssre.db'

STOCK_LIST_CSV = STOCK_DIR + os.sep + 'stock_list.csv'
ORG_LIST_CSV = STOCK_DIR + os.sep + 'org_list.csv'

REPORT_CSV = REPORT_DIR + os.sep + 'report-DATEYYMMDD.csv'
RECORDS_CSV = RECORDS_DIR + os.sep + 'reocrds-DATEYYMMDD.csv'

LAST_DAY_CSV = TIMESTAP_DIR + os.sep + 'last_day.csv'

DAY_LIST = [3, 5, 10]
WEEK_LIST = [3, 5, 10]
MONTH_LIST = [3, 6, 12]

TOP_REC = 30
LOG_FILE = TMP_DIR + os.sep + 'wssr.log'
# def write_lastday(ld=None):
#    if ld is None:
#        ld = datetime.datetime.now()
#    with open(const.LAST_DAY_CSV, 'w', errors='ignore', newline='') as f:
#        f.write(ld.strftime('%Y-%m-%d'))
#        f.close()

# def read_lastday():
#    if not os.path.exists(const.LAST_DAY_CSV):
# funcset.log("没有最后时间，写入三天前！")
#        three_days_ago = datetime.datetime.now() + datetime.timedelta(days=-3)
#        write_lastday(three_days_ago)
#    with open(const.LAST_DAY_CSV, 'r', errors='ignore', newline='') as f:
#        last_day = f.readline()
#        f.close()
#    return datetime.datetime.strptime(last_day, "%Y-%m-%d")
# last_day = read_lastday()
# days = (datetime.datetime.now() - last_day).days
# generate_report()
# for i in range(7):
# cur_day = datetime.datetime.now() + datetime.timedelta(days=i)
# cur_day = cur_day.strftime('%Y-%m-%d')
# write_lastday()

# start_date = datetime.datetime.strptime((datetime.datetime.now() + datetime.timedelta(days=-days)).strftime('%Y-%m-%d'), "%Y-%m-%d")
# end_date = datetime.datetime.now()
