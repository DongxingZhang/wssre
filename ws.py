# coding : UTF-8

import funcset
import get_report
import get_stock_list

if __name__ == '__main__':
    stock_list = get_stock_list.get_existing_stock_list()
    funcset.output("Data initialization is running.")
    get_report.get_report()
    funcset.output("Data initialization is completed.")
    funcset.help()
    top_rec = None
    top_rec_org = None
    top_rec_details = None
    latest_result = None
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
            latest_result = sl
        elif m[0] == "top" or m[0] == "t":
            funcset.output("=====================TOP===================================")
            if len(m) != 1 and len(m) != 3:
                funcset.output("top only accept zero or 2 parameters.")
                continue
            elif len(m) == 1:
                [top_rec, top_rec_org, top_rec_details] = funcset.top_recommand()
            elif len(m) == 3:
                [top_rec, top_rec_org, top_rec_details] = funcset.top_recommand(m[1], int(m[2]))
            funcset.output("===========================================================")
            latest_result = top_rec
        elif m[0] == "r" or m[0] == "rec" or m[0] == "recommand":
            funcset.output("=====================REC===================================")
            if len(m) != 2:
                funcset.output("rec only 1 parameter.")
                continue
            s = m[1].strip()
            if top_rec_org is None:
                [top_rec, top_rec_org, top_rec_details] = funcset.top_recommand()
            if s not in top_rec_org.keys():
                funcset.output(s + " is not recommanded.")
                continue
            funcset.output("股票代码:" + s + "  股票名称:" + stock_list[s])
            funcset.output("")
            funcset.output("%-4s\t%-8s\t%-10s\t" % (u"编号", u"推荐时间", u"推荐机构"))
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
                [top_rec, top_rec_org, top_rec_details] = funcset.top_recommand()
            if s not in top_rec_details.keys():
                funcset.output(s + " is not recommanded.")
                continue
            funcset.output("股票代码:" + s + "  股票名称:" + stock_list[s])
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
            sl = m[1].split(",")
            sl = [s.strip() for s in sl]
            funcset.output("=====================STOCK INFO ===========================")
            sr = funcset.show_stock_details(sl)
            funcset.output("===========================================================")
            latest_result = sr
        elif m[0] == "kdj" or m[0] == "macd":
            funcset.output("=====================KDJ MACD==============================")
            if len(m) != 2:
                funcset.output("rec only 1 parameter.")
                continue
            s = m[1].strip()
            latest_result = funcset.get_kdjmacd(s)
            funcset.output("===========================================================")
        elif m[0] == "show":
            funcset.output("=====================TUSHARE STOCK DATA====================")
            if len(m) != 2:
                funcset.output("rec only 1 parameter.")
                continue
            s = m[1].strip()
            latest_result = funcset.show_tushare(s)
            funcset.output("===========================================================")
        elif m[0] == "quit" or m[0] == "q" or m[0] == "exit" or m[0] == "e":
            break
        else:
            funcset.output("invalid command.")
