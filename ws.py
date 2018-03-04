# coding : UTF-8

import funcset
import get_report
import get_stock_list

if __name__ == '__main__':
    stock_list = get_stock_list.get_existing_stock_list()
    funcset.output("Initializing data")
    get_report.get_report()
    funcset.output("Initialize data completed")
    funcset.help()
    top_rec = None
    top_rec_org = None
    top_rec_details = None
    while True:
        print('>>', end='')
        m = input().strip().lower().split(" ")
        if m[0] == "help" or m[0] == "h":
            funcset.help()
        elif m[0] == "getstock" or m[0] == "gs":
            funcset.output("Stock list update.")
            get_stock_list.get_stock_list()
            funcset.output("Stock list update complete.")
        elif m[0] == "top" or m[0] == "t":
            funcset.output("=====================TOP==============================")
            if len(m) != 1 and len(m) != 3:
                funcset.log("top only accept zero or 2 parameters.")
            elif len(m) == 1:
                [top_rec, top_rec_org, top_rec_details] = funcset.top_recommand()
            elif len(m) == 3:
                [top_rec, top_rec_org, top_rec_details] = funcset.top_recommand(m[1], m[2])
            funcset.output("======================================================")
        elif m[0] == "r" or m[0] == "rec" or m[0] == "recommand":
            if len(m) != 2:
                funcset.log("rec only 1 parameter.")
            s = m[1].strip()
            funcset.output("=====================REC==============================")
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
            funcset.output("======================================================")
        elif m[0] == "rd" or m[0] == "recd":
            if len(m) != 2:
                funcset.log("rec only 1 parameter.")
            s = m[1].strip()
            funcset.output("=====================REC==============================")
            if top_rec_org is None:
                [top_rec, top_rec_org, top_rec_details] = funcset.top_recommand()
            if s not in top_rec_details.keys():
                funcset.output(s + " is not recommanded.")
                continue
            funcset.output("股票代码:" + s + "  股票名称:" + stock_list[s])
            funcset.output("")
            for v in top_rec_details[s]:
                funcset.output("------------------------------------------------------")
                funcset.output(v[0])
                funcset.output(v[1])
                funcset.output("------------------------------------------------------")
            funcset.output("")
            funcset.output("======================================================")
        elif m[0] == "stock" or m[0] == "s":
            sl = m[1].split(",")
            sl = [s.strip() for s in sl]
            funcset.output("=====================STOCK INFO ======================")
            funcset.show_stock_details(sl)
            funcset.output("======================================================")
        elif m[0] == "quit" or m[0] == "q" or m[0] == "exit" or m[0] == "e":
            break
        else:
            funcset.output("invalid command.")
