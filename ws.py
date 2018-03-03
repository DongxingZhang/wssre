# coding : UTF-8

import funcset
import get_report

if __name__ == '__main__':
    funcset.log("Initializing data")
    get_report.get_report()
    funcset.log("Initialize data completed")

    while True:
        m = input().strip().lower().split(" ")
        print(m)
        if m[0] == "quit":
            break
        elif m[0] == "help":
            funcset.help()
        elif m[0] == "stock":
            funcset.show_stock_details([])
        elif m[0] == "ref":
            funcset.show_reference_details([])
        elif m[0] == "top":
            funcset.top_reference()
    # parser = argparse.ArgumentParser(description='manual to this script')
    # parser.add_argument('--function', type=str, default=None)
    # args = parser.parse_args()
    # func = "get_report"
    # if args.function is not None:
    #    func = args.function
    # funcset.log("function : " + func)
    # if func == "get_stock":
    #    get_stock_list.get_stock_list()
    # elif func == "get_report":
    # get_report.get_report()
    # get_statistics.get_statistics()
