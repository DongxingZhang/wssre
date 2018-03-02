# stock_data is the dataframe from tushare
def getStockMacd(self, stock_data, macd_l=26, macd_s=12, macd_m=9):
    stock_data['ma_s'] = stock_data['close'].ewm(span=macd_s).mean().tolist()
    stock_data['ma_l'] = stock_data['close'].ewm(span=macd_l).mean().tolist()
    stock_data['diff'] = (stock_data['ma_s'] - stock_data['ma_l']).tolist()
    stock_data['dea'] = stock_data['diff'].ewm(span=macd_m).mean().tolist()
    stock_data['macd'] = ((stock_data['diff'] - stock_data['dea']) * 2).tolist()
    return stock_data


def getStockKDJ(self, stock_data, n=9, n1=3, n2=3):
    stock_length = len(stock_data)
    rsv_list = [0.0 for i in range(stock_length)]
    k_list = [0.0 for i in range(stock_length)]
    d_list = [0.0 for i in range(stock_length)]
    j_list = [0.0 for i in range(stock_length)]
    high_list = stock_data['high'].rolling(window=n, center=False).max().tolist()
    low_list = stock_data['low'].rolling(window=n, center=False).min().tolist()
    # complement the 0:n-1 value due to the rolling max/min method will get these values to nan
    for i in range(1, min(n, stock_length)):
        high_list[i - 1] = max(stock_data['high'][0:i])
        low_list[i - 1] = min(stock_data['low'][0:i])

    rsv_list[0] = (stock_data['close'][0] - low_list[0]) / (high_list[0] - low_list[0]) * 100.0
    k_list[0] = rsv_list[0]
    d_list[0] = rsv_list[0]
    j_list[0] = rsv_list[0]

    for i in range(1, stock_length):
        rsv_list[i] = (stock_data['close'][i] - low_list[i]) / (high_list[i] - low_list[i]) * 100.0
        k_list[i] = (k_list[i - 1] * (n1 - 1) + rsv_list[i]) / n1
        d_list[i] = (d_list[i - 1] * (n2 - 1) + k_list[i]) / n2
        j_list[i] = k_list[i] * 3.0 - d_list[i] * 2.0
    stock_data['k'] = k_list
    stock_data['d'] = d_list
    stock_data['j'] = j_list

    return stock_data
