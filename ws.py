# coding : UTF-8

import argparse

import const
import funcset
import get_report
import get_stock_list
import wssrdb

if __name__ == '__main__':
    stock_dict = get_stock_list.get_existing_stock_list()
    org_dict = get_stock_list.get_existing_org_list()
    get_report.get_report(stock_dict, org_dict)
    parser = argparse.ArgumentParser(description='Web Spider Stock Recommendation Tool')
    parser.add_argument('--function', type=str, default=None)
    args = parser.parse_args()
    if args.function is None:
        top_rec = None
        date_range = None
        latest_result = None
        funcset.help()
        while True:
            print('>>', end='')
            m = input().strip().lower().split(" ")
            try:
                if m[0] == "help" or m[0] == "h":
                    funcset.help()
                elif m[0] == "savetocsv" or m[0] == "save":
                    if len(m) != 2:
                        funcset.output("save  [文件路径]: 保存最后的结果到csv文件。")
                        continue
                    s = m[1].strip()
                    if latest_result == None:
                        funcset.output("最后结果为空。")
                    else:
                        funcset.write_listlist_csv(s, "w", latest_result)
                        funcset.output("最后结果被保存到文件" + s)
                elif m[0] == "getstock" or m[0] == "gs":
                    funcset.output("==================股票列表==================================")
                    funcset.output("股票列表更新中......")
                    sl = get_stock_list.get_stock_list()
                    funcset.output("股票列表更新完成," + str(len(sl)) + "条记录生成。")
                    funcset.output("===========================================================")
                elif m[0] == "top" or m[0] == "t":
                    funcset.output(
                        "=====================TOP(" + str(const.TOP_REC) + ")===============================")
                    if len(m) != 1 and len(m) != 3:
                        funcset.output("top [结束时期，如20180305] [工作日天数，如3]: 查找从[结束日期]")
                        funcset.output("     开始往前给定的工作日时间内推荐次数最多的股票列表")
                        continue
                    elif len(m) == 1:
                        [top_rec, date_range] = funcset.top_recommend(stock_dict, org_dict)
                        funcset.output(
                            "开始日期: " + date_range[0].strftime('%Y-%m-%d') + "    结束日期: " + date_range[1].strftime(
                                '%Y-%m-%d') + "    工作日: 3")
                    elif len(m) == 3:
                        [top_rec, date_range] = funcset.top_recommend(stock_dict, org_dict, m[1], int(m[2]))
                        funcset.output(
                            "开始日期: " + date_range[0].strftime('%Y-%m-%d') + "    结束日期: " + date_range[1].strftime(
                                '%Y-%m-%d') + "    工作日:" + str(m[2]))
                    funcset.output("")
                    n = 1
                    funcset.output("%-4s\t%-8s\t%-10s\t%-4s\t" % ("编号", "股票编号", "股票名称", "次数"))
                    for r in top_rec:
                        funcset.output("%-4s\t%-8s\t%-10s\t%-4s\t" % (n, r[0], r[1], str(r[2])))
                        n += 1
                    funcset.output("")
                    funcset.output("===========================================================")
                    latest_result = top_rec
                elif m[0] == "r" or m[0] == "rec" or m[0] == "recommend":
                    funcset.output("=====================REC===================================")
                    if len(m) != 2:
                        funcset.output("rec [股票编号]:获取这个股票的相关推荐信息")
                        continue
                    s = m[1].strip()
                    if top_rec is None:
                        [top_rec, date_range] = funcset.top_recommend(stock_dict, org_dict)
                    rec_list = wssrdb.top_recommend_stock_org(s, org_dict, date_range[0], date_range[1])
                    funcset.output("股票编号:" + s + "  股票名称:" + stock_dict[s])
                    funcset.output("")
                    funcset.output("%-4s\t%-8s\t%-10s\t" % ("编号", "日期", "机构"))
                    n = 1
                    for v in rec_list:
                        funcset.output("%-4s\t%-8s\t%-10s\t" % (n, v[0], v[1]))
                        n += 1
                    funcset.output("")
                    funcset.output("===========================================================")
                elif m[0] == "rd" or m[0] == "recd":
                    funcset.output("=====================推荐信息==============================")
                    if len(m) != 2:
                        funcset.output("rd  [股票代码，如000001]:获取股票推荐信息和网页。")
                        continue
                    s = m[1].strip()
                    if top_rec is None:
                        [top_rec, date_range] = funcset.top_recommend(stock_dict, org_dict)
                    recd_list = wssrdb.top_recommend_stock_info(s, org_dict, date_range[0], date_range[1])
                    funcset.output("股票编号:" + s + "  股票名称:" + stock_dict[s])
                    funcset.output("")
                    for v in recd_list:
                        funcset.output("-----------------------------------------------------------")
                        funcset.output("日期:" + str(v[0]) + ",机构:" + str(v[1]))
                        funcset.output(v[2])
                        funcset.output("网址:" + v[3])
                        funcset.output("-----------------------------------------------------------")
                    funcset.output("")
                    funcset.output("===========================================================")
                elif m[0] == "stock" or m[0] == "s":
                    if len(m) != 2 and len(m) != 1:
                        funcset.output("stock [股票列表]:获取[股票列表]指标信息。")
                        funcset.output("     [股票列表]: 如0000001,0000002,0000003。")
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
                    sr = funcset.show_stock_details(sl, stock_dict)
                    funcset.output(
                        "%-8s\t%-8s\t%-8s\t%-8s\t%-8s\t%-8s\t%-8s\t%-8s\t %-8s\t%-8s\t%-8s\t%-8s\t%-8s\t%-8s" % (
                            "股票编号", "股票名称", "次数", "市净率", "市盈率", "涨跌(3天)", "涨跌(5天)", "涨跌(10天)",
                            "涨跌(3周)", "涨跌(5周)", "涨跌(10周)", "涨跌(3月)", "涨跌(6月)", "涨跌(12月)"
                        ))
                    for temp in sr:
                        rc = "-"
                        if temp[0] in rec.keys():
                            rc = rec[temp[0]]
                        funcset.output(
                            "%-8s\t%-8s\t%-8s\t%-8s\t%-8s\t%-8s\t%-8s\t%-8s\t %-8s\t%-8s\t%-8s\t%-8s\t%-8s\t%-8s" % (
                                str(temp[0]), str(temp[1]), rc, str(temp[2]), str(temp[3]), str(temp[4]),
                                str(temp[5]), str(temp[6]), str(temp[7]), str(temp[8]), str(temp[9]), str(temp[10]),
                                str(temp[11]), str(temp[12])))
                    funcset.output("===========================================================")
                    latest_result = sr
                elif m[0] == "kdj" or m[0] == "macd":
                    funcset.output("=====================KDJ&MACD==============================")
                    if len(m) != 2:
                        funcset.output("kdj/macd  [股票代码,如000001]: 获取MACD/KDJ金叉信息")
                        continue
                    s = m[1].strip()
                    km = funcset.get_kdjmacd(s)
                    if len(km) == 0:
                        funcset.output("很遗憾，没有关于" + s + "的信息。")
                        continue
                    for type in km:
                        date_list = km[type][0]
                        kdj_list = km[type][1]
                        macd_list = km[type][2]
                        stock_length = len(date_list)
                        funcset.output("-----------------------------------------------------------")
                        funcset.output(
                            "%-8s\t%-8s\t%-8s" % ("日期", "KDJ金叉(" + type + ")", "MACD金叉(" + type + ")"))
                        for i in range(stock_length):
                            if kdj_list[i] == "金叉" or macd_list[i] == "金叉":
                                funcset.output("%-8s\t%-8s\t%-8s" % (date_list[i], kdj_list[i], macd_list[i]))
                        funcset.output("-----------------------------------------------------------")
                    funcset.output("===========================================================")
                elif m[0] == "show":
                    funcset.output("=====================TUSHARE 数据==========================")
                    if len(m) != 2:
                        funcset.output("show [股票代码,如000001]: 打印来自tushare的k线数据")
                        continue
                    s = m[1].strip()
                    funcset.show_tushare(s)
                    funcset.output("===========================================================")
                elif m[0] == "trend" or m[0] == "tr":
                    if len(m) != 2:
                        funcset.output("trend [股票代码,如000001]: 输出股票的推荐趋势")
                        continue
                    s = m[1].strip()
                    funcset.show_trend(s)
                elif m[0] == "settoprec":
                    if len(m) != 2 and len(m) != 1:
                        funcset.output("settoprec  [top推荐股票数量]: 设置top推荐股票数量")
                        continue
                    if len(m) == 2:
                        const.TOP_REC = int(m[1].strip())
                    print("当前为" + str(const.TOP_REC))
                elif m[0] == "last":
                    for r in latest_result:
                        funcset.output(r)
                elif m[0] == "quit" or m[0] == "q" or m[0] == "exit" or m[0] == "e":
                    break
                else:
                    funcset.output("无效命令 " + m[0] + ".")
            except Exception as e:
                funcset.output(e)
