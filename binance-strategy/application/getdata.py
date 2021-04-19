import pandas as pd
from binance.client import Client
import pprint, talib, Config

def get_hist_indicator(ma_period):
    """Get historical values of indicator on booting
    """
    my_mod = Client(Config.API_KEY, Config.API_SECRET)
    my_mod.API_URL = Config.API_URL
    candlesticks = my_mod.get_historical_klines("BTCUSDT", my_mod.KLINE_INTERVAL_5MINUTE, "1 Apr, 2021", "29 Apr, 2022")
    processed_candlesticks = []
    ndict = {
        'time':[],
        'close':[]
    }
    for data in candlesticks:
        ndict['time'].append(data[0] / 1000)
        ndict['close'].append(float(data[4]))

    df = pd.DataFrame(ndict)
    df.drop(df.tail(1).index,inplace=True)
    ndf = df.tail(ma_period).to_dict('list')

    return ndf