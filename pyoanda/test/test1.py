import datetime
#================================================
import requests
import pprint
import collections
import sys
import json

class OandaTrading():
    def __init__(self):
        self.date_today = datetime.datetime.today().date()
        self.is_1_day_buy = True
        self.is_1_day_sell = True
        self.is_3_day_buy = False
        self.is_3_day_sell = False
        self.is_7_day_buy = False
        self.is_7_day_sell = False
        self.mode = '3_day'
        self.strategy1_file_path = 'strategy/strategy_1.json'

        self.pos_detail_dict = collections.defaultdict(lambda: '')
        self.isEnd = False
        # strategy_1 : buy or sell order and close_out dict
        # {date_object:{'close_out':['EUR_USD', ...]}}
        self.strategy_1_dict = collections.defaultdict(lambda: collections.defaultdict(lambda: []))
        self.domain = 'api-fxpractice.oanda.com'
        self.access_token = 'b53308ebd6ec5da20475f6e5481e3b7d-b17b9d81c15d6ec435cf875bcc41f4d9'
        self.account_id = '101-004-5027528-001'
        self.order_url = "https://" + self.domain + "/v3/accounts/{}/orders".format(self.account_id)
        self.close_out_url = "https://" + self.domain + "/v3/accounts/{}/trades/{}/close"
        self.get_all_positions_url = "https://" + self.domain + "/v3/accounts/{}/openPositions".format(self.account_id)
        self.get_trade_id_url = "https://" + self.domain + "/v3/accounts/{}/trades?instrument={}"
        self.headers = {
            "Content-Type": "application/json",
            'Authorization': 'Bearer ' + self.access_token,
        }
        self.body = {"order": {
            "units": "50",
            "instrument": "EUR_USD",
            "timeInForce": "FOK",
            "type": "MARKET",
            "positionFill": "DEFAULT"
        }
        }

    def close_out(self):
        def get_trade_id(instrument):
            url = self.get_trade_id_url.format(self.account_id, instrument)
            response = requests.get(url, headers=self.headers)
            trade_id = dict(response.json())['trades'][0]["id"]
            return trade_id

        instrument = 'EUR_USD'
        trade_id = get_trade_id(instrument)
        url = self.close_out_url.format(self.account_id, trade_id)
        body = {'units': '5'}
        response = requests.put(url, headers=self.headers, json = body)
        response_content = sorted(list(dict(response.json()).items()))
        status_code = response.status_code
        print ("response_content: ", response_content)
        print ("status_code: ", status_code)


    def trade(self):
        time = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        body = self.body
        headers = self.headers
        url = self.order_url
        body['order']['instrument'] = 'USD_JPY'

        response = requests.post(url, headers=headers, json=body)
        response_content = response.json()
        status_code = response.status_code
        print ("response_content: ", response_content)
        print ("status_code: ", status_code)

        # logging



#response_content:  [('lastTransactionID', '195'),
# ('orderCancelTransaction',
# {'time': '2017-05-20T12:23:10.888227692Z',
# 'type': 'ORDER_CANCEL', 'orderID': '194',
# 'userID': 5027528, 'reason': 'MARKET_HALTED',
# 'batchID': '194', 'requestID': '24286069936909317',
#  'id': '195', 'accountID': '101-004-5027528-001'}), ('orderCreateTransaction',
# {'type': 'MARKET_ORDER', 'positionFill': 'REDUCE_ONLY',
#  'time': '2017-05-20T12:23:10.888227692Z', 'timeInForce': 'FOK', 'instrument': 'EUR_USD', 'batchID': '194',
# 'tradeClose': {'tradeID': '88', 'units': '5'}, 'units': '5', 'userID': 5027528, 'reason': 'TRADE_CLOSE',
#  'requestID': '24286069936909317', 'id': '194', 'accountID': '101-004-5027528-001'}),
#  ('relatedTransactionIDs', ['194', '195'])]


# # trade
# response_content:  {'orderCreateTransaction': {'batchID': '204', 'positionFill': 'DEFAULT', 'id': '204', 'userID': 5027528, 'time': '2017-05-20T12:38:31.625793271Z', 'type': 'MARKET_ORDER', 'timeInForce': 'FOK', 'instrument': 'USD_JPY', 'units': '50', 'accountID': '101-004-5027528-001', 'reason': 'CLIENT_ORDER', 'requestID': '24286073800779523'}, 'lastTransactionID': '205', 'orderCancelTransaction': {'userID': 5027528, 'accountID': '101-004-5027528-001', 'id': '205', 'batchID': '204', 'reason': 'MARKET_HALTED', 'requestID': '24286073800779523', 'time': '2017-05-20T12:38:31.625793271Z', 'orderID': '204', 'type': 'ORDER_CANCEL'}, 'relatedTransactionIDs': ['204', '205']}
# status_code:  201



ot = OandaTrading()
ot.close_out()
ot.trade()