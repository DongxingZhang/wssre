# coding : UTF-8

import datetime

import const
import funcset
import get_report
import get_stock_list

if __name__ == '__main__':
    top_rec = None
    top_rec_org = None
    top_rec_details = None
    latest_result = None
    stock_list = get_stock_list.get_existing_stock_list()
    get_report.get_report()
    funcset.help()
    while True:
        print('>>', end='')
        m = input().strip().lower().split(" ")
        if m[0] == "help" or m[0] == "h":
            funcset.help()
        elif m[0] == "savetocsv" or m[0] == "save":
            if len(m) != 2:
                funcset.output("rec only 1 parameter.")
                continue
            s = m[1].strip()
            if latest_result == None:
                funcset.output("latest result is None")
            else:
                funcset.write_listlist_csv(s, "w", latest_result)
                funcset.output("latest_result was written to " + s)
        elif m[0] == "getstock" or m[0] == "gs":
            funcset.output("==================STOCK LIST===============================")
            funcset.output("Stock list is being updated.")
            sl = get_stock_list.get_stock_list()
            funcset.output("Stock list update is completed.")
            funcset.output("===========================================================")
        elif m[0] == "top" or m[0] == "t":
            funcset.output("=====================TOP(" + str(const.TOP_REC) + ")===============================")
            if len(m) != 1 and len(m) != 3:
                funcset.output("top only accept zero or 2 parameters.")
                continue
            elif len(m) == 1:
                [top_rec, top_rec_org, top_rec_details] = funcset.top_recommend()
                funcset.output("End Date: " + datetime.datetime.now().strftime('%Y%m%d') + "    Working Days: 3")
            elif len(m) == 3:
                [top_rec, top_rec_org, top_rec_details] = funcset.top_recommend(m[1], int(m[2]))
                funcset.output("End Date: " + m[1] + "    Working Days:" + str(m[2]))
            funcset.output("")
            n = 0
            top_rec.insert(0, ["No.", "StockID", "StockName", "RecCount"])
            for r in top_rec:
                funcset.output("%-4s\t%-8s\t%-10s\t%-4s\t" % (n, r[0], r[1], str(r[2])))
                n += 1
            funcset.output("")
            funcset.output("===========================================================")
            latest_result = top_rec
        elif m[0] == "r" or m[0] == "rec" or m[0] == "recommend":
            funcset.output("=====================REC===================================")
            if len(m) != 2:
                funcset.output("rec only accept 1 parameter.")
                continue
            s = m[1].strip()
            if top_rec_org is None:
                [top_rec, top_rec_org, top_rec_details] = funcset.top_recommend()
            if s not in top_rec_org.keys():
                funcset.output(s + " is not recommended.")
                continue
            funcset.output("Stock ID:" + s + "  Stock Name:" + stock_list[s])
            funcset.output("")
            funcset.output("%-4s\t%-8s\t%-10s\t" % ("No.", "RecDate", "RecOrg"))
            n = 1
            for v in top_rec_org[s]:
                funcset.output("%-4s\t%-8s\t%-10s\t" % (n, v[0], v[1]))
                n += 1
            funcset.output("")
            funcset.output("===========================================================")
            latest_result = top_rec_org[s]
        elif m[0] == "rd" or m[0] == "recd":
            funcset.output("=====================REC DETAIL============================")
            if len(m) != 2:
                funcset.output("rec only 1 parameter.")
                continue
            s = m[1].strip()
            if top_rec_org is None:
                [top_rec, top_rec_org, top_rec_details] = funcset.top_recommend()
            if s not in top_rec_details.keys():
                funcset.output(s + " is not recommended.")
                continue
            funcset.output("Stock ID:" + s + "  Stock Name:" + stock_list[s])
            funcset.output("")
            for v in top_rec_details[s]:
                funcset.output("-----------------------------------------------------------")
                funcset.output(v[0])
                funcset.output(v[1])
                funcset.output("-----------------------------------------------------------")
            funcset.output("")
            funcset.output("===========================================================")
            latest_result = top_rec_details[s]
        elif m[0] == "stock" or m[0] == "s":
            if len(m) != 2 and len(m) != 1:
                funcset.output("stock only 0 or 1 parameter.")
                continue
            sl = []
            rec = {}
            if len(m) == 2:
                sl = m[1].split(",")
                sl = [s.strip() for s in sl]
            elif len(m) == 1 and top_rec is not None:
                sl = [v[0] for v in top_rec]
                rec = {v[0]: v[2] for v in top_rec}
            funcset.output("=====================STOCK INFO ===========================")
            sr = funcset.show_stock_details(sl)
            sr.insert(0, ["StockID", "StockName", "RecCount", "PE", "PB", "Change(3D)", "Change(5D)", "Change(10D)",
                          "Change(3W)", "Change(5W)", "Change(10W)", "Change(3M)",
                          "Change(6M)",
                          "Change(12M)"])
            for temp in sr:
                funcset.output("%-8s\t%-8s\t%-8s\t%-8s\t%-8s\t%-8s\t%-8s\t%-8s\t %-8s\t%-8s\t%-8s\t%-8s\t%-8s\t%-8s" % (
                    str(temp[0]), str(temp[1]), str(rec[temp[0]]), str(temp[2]), str(temp[3]), str(temp[4]),
                    str(temp[5]), str(temp[6]),
                    str(temp[7]), str(temp[8]), str(temp[9]), str(temp[10]),
                    str(temp[11]),
                    str(temp[12])))
            funcset.output("===========================================================")
            latest_result = sr
        elif m[0] == "kdj" or m[0] == "macd":
            funcset.output("=====================KDJ&MACD==============================")
            if len(m) != 2:
                funcset.output("rec only 1 parameter.")
                continue
            s = m[1].strip()
            km = funcset.get_kdjmacd(s)
            date_list = km[0]
            kdj_list = km[1]
            macd_list = km[2]
            stock_length = len(date_list)
            for type in km:
                funcset.output("-----------------------------------------------------------")
                funcset.output("%-8s\t%-10s\t%-10s" % ("DATE", "KDJ CROSS(" + type + ")", "MACD CROSS(" + type + ")"))
                for i in range(stock_length):
                    if kdj_list[i] == "金叉" or macd_list[i] == "金叉":
                        funcset.output("%-8s\t%-10s\t%-10s" % (date_list[i], kdj_list[i], macd_list[i]))
                funcset.output("-----------------------------------------------------------")
            funcset.output("===========================================================")
        elif m[0] == "show":
            funcset.output("=====================TUSHARE STOCK DATA====================")
            if len(m) != 2:
                funcset.output("rec only 1 parameter.")
                continue
            s = m[1].strip()
            latest_result = funcset.show_tushare(s)
            funcset.output("===========================================================")
        elif m[0] == "settoprec":
            if len(m) != 2:
                funcset.output("settoprec only 1 parameter.")
                continue
            const.TOP_REC = int(m[1].strip())
        elif m[0] == "last":
            print(latest_result)
        elif m[0] == "quit" or m[0] == "q" or m[0] == "exit" or m[0] == "e":
            break
        else:
            funcset.output("invalid command " + m[0] + ".")
