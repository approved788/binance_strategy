import websocket, json, pprint, talib, numpy
import Config, pprint, time
from binance.client import Client
from binance.enums import *
import pandas as pd
import getdata as gt

#   Need defaults to load basic data
MA_PERIOD = 400
TRADE_SYMBOL = 'BTCUSDT'

hist_data = gt.get_hist_indicator(MA_PERIOD)
in_position = False
side = ''
with open('static/data.json') as json_file:
    data = json.load(json_file)
previous_boot_data = data['sys_config'][-1]
last_params = [
    previous_boot_data['ma_period'],
    previous_boot_data['ma_up'],
    previous_boot_data['ma_dn'],
    previous_boot_data['risk']
]
client = Client(Config.API_KEY, Config.API_SECRET)
client.API_URL = Config.API_URL

def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    #   Prepare and send trade order.
    #   Return boolean value for in_trade variable,
    #   to control trade status.
    
    try:
        print("Sending order")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
        pprint.pprint(order)

        #   Return trade status
        if order['status'] == 'FILLED':
            return True
        if order['status'] in ['EXPIRED', 'CANCELED']:
            return False

    except Exception as e:
        print("Exception occured: {}".format(e))
        return False
  
def on_open(ws):
    #   Send message when connection established
    print('Connection established')

def on_close(ws):
    #   Send message on closed connection
    print(' Connection terminated')

def on_message(ws, message):
    #   Receive prices from web socket,
    #   operate it and send trade order
    global closes, in_position, hist_data, previous_boot_data, side
    
    json_message = json.loads(message)
    bar = json_message['k']
    is_close = bar['x']
    close = bar['c']

    #   Start operate if received close bar value
    if is_close:
        print(' ')
        print(' ')
        print('_________________________________')
        print("Candle last close bid price is {}".format(close))
        print(' ')
        hist_data['close'].append(float(close))

        #   Read settings from file, which chained with front-end.
        with open('static/data.json') as json_file:
            data = json.load(json_file)
        front_data = data['sys_config'][-1]
        front_last_ma_period = int(front_data['ma_period'])
        front_last_ma_up = float(front_data['ma_up'])
        front_last_ma_dn = float(front_data['ma_dn'])
        front_last_risk = float(front_data['risk'])

        last_front_list=[]
        for front_last in front_data.values():
            last_front_list.append(front_last)
        
        #   Say if settings was changed
        if last_front_list != previous_boot_data:
            print('-----ATTENTION-----')
            print('System received new configuration, new settings will be applied.')
            print('---------------------')
            print(' ')
            previous_boot_data = last_front_list

        #   Check lenght for indicator to operate futher
        if len(hist_data['close']) >= front_last_ma_period:
            np_arr = numpy.array(hist_data['close'][-front_last_ma_period:])
            sma = talib.SMA(np_arr, front_last_ma_period)
            print("SMA for given period gathered !")
            print(' ')
            
            last_sma = sma[-1]
            last_up = sma[-1] + front_last_ma_up
            last_dn = sma[-1] - front_last_ma_dn
            print("Last SMA value:{}, UP:{}, DN:{}".format(last_sma, last_up, last_dn))
            print('_________________________________')
            print(' ')

            #   Terminate position if price trigger ma
            if in_position:
                
                if side == 'SELL':
                    if close <= last_sma:
                        try:
                            make_order = order(SIDE_BUY, front_last_risk, TRADE_SYMBOL)
                            time.sleep(2)
                            if make_order:
                                in_position=False
                                side=''
                                print('----------------')
                                print('Sell position closed')
                                print('----------------')
                        except Exception:
                            print('----------------')
                            print('Oops, lack of liquidity lo close !')
                            print('----------------')

                if side == 'BUY':
                    if close >= last_sma:
                        try:
                            make_order = order(SIDE_SELL, front_last_risk, TRADE_SYMBOL)
                            if make_order:
                                in_position=False
                                side=''
                                print('----------------')
                                print('Buy position closed')
                                print('----------------')
                        except Exception:
                            print('----------------')
                            print('Oops, lack of liquidity lo close !')
                            print('----------------')

            #   Open new Sell
            if hist_data['close'][-1] > last_up:
                if in_position:
                    print('.................................')
                    print(' ')
                    print("Got position, can`t open new one")
                    print(' ')
                    print('.................................')
                
                if not in_position:
                    try:
                        make_order = order(SIDE_SELL, front_last_risk, TRADE_SYMBOL)
                        if make_order:
                            in_position = True
                            side = 'SELL'
                            print('.................................')
                            print(' ')
                            print("Sell position opened !")
                            print(' ')
                            print('.................................')
                        if not make_order:
                            print('.................................')
                            print(' ')
                            print("There is no liquididty on test server to execute order!")
                            print(' ')
                            print('.................................')
                    except Exception:
                        print('.................................')
                        print(' ')
                        print("Something go wrong!")
                        print(' ')
                        print('.................................')
            
            #   Open new Buy
            if hist_data['close'][-1] < last_dn:
                if in_position:
                    print('.................................')
                    print("Got position, can`t open new one")
                
                if not in_position:
                    try:
                        make_order = order(SIDE_BUY, front_last_risk, TRADE_SYMBOL)
                        if make_order:
                            in_position = True
                            side = 'BUY'
                            print('.................................')
                            print(' ')
                            print("Buy position opened !")
                            print(' ')
                            print('.................................')
                        if not make_order:
                            print('.................................')
                            print(' ')
                            print("There is no liquididty on test server to execute order!")
                            print(' ')
                            print('.................................')
                    except Exception:
                        print('.................................')
                        print(' ')
                        print("Something go wrong!")
                        print(' ')
                        print('.................................')

ws = websocket.WebSocketApp(Config.API_SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()