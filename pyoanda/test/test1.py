import datetime
from pjslib.general import get_upper_folder_path
from pjslib.general import accepts
#from pjslib.logger import oanda_logger
#================================================
import requests
import pprint
import collections
import time
import sys
import os
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
            "units": "1",
            "instrument": "EUR_USD",
            "timeInForce": "FOK",
            "type": "MARKET",
            "positionFill": "DEFAULT",
        }
        }
        close_out_file = 'close_out_order.txt'
        folder = 'order'
        current_folder = get_upper_folder_path(1)
        self.close_out_file_path = os.path.join(current_folder, folder, close_out_file)

    def close_out(self):
        def get_trade_id(instrument):
            url = self.get_trade_id_url.format(self.account_id, instrument)
            response = requests.get(url, headers=self.headers)
            trade_id = dict(response.json())['trades'][0]["id"]
            return trade_id

        body = self.body
        instrument = 'USD_JPY'
        body['order']['instrument'] = instrument
        trade_id = get_trade_id(instrument)
        trade_id = '241'
        url = self.close_out_url.format(self.account_id, trade_id)
        response = requests.put(url, headers=self.headers, json = body)
        response_content = sorted(list(dict(response.json()).items()))
        status_code = response.status_code
        #
        print ("response_content: ", response_content)
        print ("status_code: ", status_code)


    def trade(self):
        time = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        body = self.body
        headers = self.headers
        url = self.order_url
        body['order']['instrument'] = 'USD_JPY'
        body['order']['units'] = '10'
        response = requests.post(url, headers=headers, json=body)
        response_content = response.json()
        last_transaction_id = response_content['lastTransactionID']
        print ("last_transaction_id: ", last_transaction_id)
        status_code = response.status_code
        print ("response_content: ", response_content)
        print ("status_code: ", status_code)

        # logging

    def get_all_positions(self):
        time = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        url = self.get_all_positions_url
        response = requests.get(url, headers = self.headers)
        positions_list = dict(response.json())['positions']
        pprint.pprint(positions_list)
        all_pos_list = []
        for positions_dict in positions_list:
            instrument = positions_dict['instrument']
            all_pos_list.append(instrument)

            # get the pos detail(buy/sell)
            long_units = int(positions_dict['long']['units'])
            short_units = int(positions_dict['short']['units'])
            if long_units == 0 and short_units <=0:
                buy_or_sell = 'sell'
            elif short_units == 0 and long_units >=0:
                buy_or_sell = 'buy'
            else:
                #oanda_logger.error("ERROR HAPPEND AT get_all_positions! long_unit, short unit")
                sys.exit(0)
            self.pos_detail_dict[instrument] = buy_or_sell

        #   archive positions
        date = datetime.datetime.today().strftime("%Y-%m-%d")
        folder_name = 'position_archive'
        date_file_name = date + '_positions.txt'
        date_file_path = os.path.join(folder_name, date_file_name)
        archive_time = datetime.datetime.today().strftime("%Y-%m-%d-%H-%M-%S")

        with open(date_file_path, 'w') as f:
            f.write("archive_time: {}\n".format(archive_time))
            for detail in positions_list:
                f.write(str(detail))
                f.write("\n")

    def close_out2(self,strategy='s2'):
        # get close out id
        close_out_id_list = []
        with open(self.close_out_file_path, 'r') as f:
            for line in f:
                if line == '\n':
                    continue
                line_list = line.strip().split(',')
                date = line_list[1]
                id = line_list[-1]
                date_temp = time.strptime(date, '%Y-%m-%d')
                date_obj = datetime.datetime(*date_temp[:3]).date()
                print ('date_obj ', date_obj)
                print ('date_today ', self.date_today)
                if self.date_today == date_obj:
                    close_out_id_list.append(id)

        if not close_out_id_list:
            print ("No close out forex for {}".format(date))

        for i, trade_id in enumerate(close_out_id_list):

            url = self.close_out_url.format(self.account_id, trade_id)
            response = requests.put(url, headers=self.headers)
            response_content = response.json()
            status_code = response.status_code
            print ("trade_id: ", trade_id)
            print ("response_content: ", response_content)
            print ("status_code: ", status_code)
            # ===============================================================================
            # delete the close_out_order line if close out is done succesfully
            # TODO change status_code
            new_file_list = []
            if status_code == 200:
                with open(self.close_out_file_path, 'r') as f:
                    for line in f:
                        line_list = line.strip().split(',')
                        f_trade_id = line_list[-1]
                        date = line_list[1]
                        date_temp = time.strptime(date, '%Y-%m-%d')
                        date_obj = datetime.datetime(*date_temp[:3]).date()
                        if f_trade_id == trade_id and self.date_today == date_obj:
                            continue
                        else:
                            new_file_list.append(line)

                with open(self.close_out_file_path, 'w') as f:
                    for new_line in new_file_list:
                        f.write(new_line)
                print ("Close out trade_id {} succesfully!".format(trade_id))
            else:
                print ("trade_id {} does not hold any position!".format(trade_id))
            # ===============================================================================





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
ot.close_out2()
#ot.trade()
ot.get_all_positions()
