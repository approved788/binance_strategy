from binance.client import Client
from application import Config
# import Config
from datetime import datetime

class SystemClient:
    """Modified model of binance Client Model.
    Symbol is hardcoded due to task system rules,
    can be simply refactored.

    API Keys are hardcoded too, but can be simply refactored.
    """

    def __init__(self, sys_name):
        self.name = sys_name
        self.client = Client(Config.API_KEY, Config.API_SECRET)
        self.client.API_URL = Config.API_URL
    
    def get_balance(self):
        self.balance = self.client.get_account()['balances']
        return self.balance
    
    def get_trades(self):
        result_list = []
        self.trades = self.client.get_all_orders(symbol='BTCUSDT')

        for trade in self.trades:
            result_dict = {}
            result_dict['OrderID'] = trade['orderId']
            result_dict['OrderSymbol'] = trade['symbol']
            result_dict['OrderSide'] = trade['side']
            result_dict['ExecutionStatus'] = trade['status']
            result_dict['OriginalVolume'] = trade['origQty']
            result_dict['ExecutedVolume'] = trade['executedQty']
            result_dict['time'] = datetime.fromtimestamp(trade['time'] / 1000)

            result_list.append(result_dict)

        return result_list