# coding : UTF-8

import const
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
                [top_rec, top_rec_org, top_rec_details] = funcset.top_recommend()
            elif len(m) == 3:
                [top_rec, top_rec_org, top_rec_details] = funcset.top_recommend(m[1], int(m[2]))
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
                [top_rec, top_rec_org, top_rec_details] = funcset.top_recommend()
            if s not in top_rec_details.keys():
                funcset.output(s + " is not recommended.")
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
            funcset.output("%-8s\t%-8s\t%-8s\t%-8s\t%-8s\t%-8s\t%-8s\t%-8s\t %-8s\t%-8s\t%-8s\t%-8s\t%-8s\t%-8s" % (
                "股票编码", "股票名称", "推荐次数", "市盈率", "市净率", "涨(3天)", "涨(5天)", "涨(10天)", "涨(3周)", "涨(5周)", "涨(10周)", "涨(3月)",
                "涨(6月)",
                "涨(12月)"))
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
        elif m[0] == "settoprec":
            if len(m) != 2:
                funcset.output("settoprec only 1 parameter.")
                continue
            const.TOP_REC = int(m[1].strip())
        elif m[0] == "quit" or m[0] == "q" or m[0] == "exit" or m[0] == "e":
            break
        else:
            funcset.output("invalid command.")
