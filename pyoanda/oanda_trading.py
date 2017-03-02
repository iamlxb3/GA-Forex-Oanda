# import from pjslib
from pjslib.general import get_upper_folder_path
from pjslib.general import accepts
from pjslib.logger import oanda_logger
import datetime
#================================================
import requests
import pprint



class OandaTrading():
    def __init__(self):
        self.isEnd = False
        self.domain = 'api-fxpractice.oanda.com'
        self.access_token = 'b53308ebd6ec5da20475f6e5481e3b7d-b17b9d81c15d6ec435cf875bcc41f4d9'
        self.account_id = '101-004-5027528-001'
        self.order_url = "https://" + self.domain + "/v3/accounts/{}/orders".format(self.account_id)
        self.close_out_url = "https://" + self.domain + "/v3/accounts/{}/trades/{}/close"
        self.get_all_positions_url = "https://" + self.domain + "/v3/accounts/{}/openPositions".format(self.account_id)
        self.get_trade_id_url =  "https://" + self.domain + "/v3/accounts/{}/trades?instrument={}"
        self.headers = {
        "Content-Type": "application/json",
        'Authorization' : 'Bearer ' + self.access_token,
              }
        self.body = {"order": {
            "units": "10",
            "instrument": "EUR_USD",
            "timeInForce": "FOK",
            "type": "MARKET",
            "positionFill": "DEFAULT"
        }
        }

    def update_data(self, start_time, end_time, mode = 'trading'):
        pass

    # ga_classifier_result_dict {'1_day':{'buy':['USD/JPY'], 'sell':['USD/JPY']},...}
    def get_day_buy_sell(self, ga_classifier_result_dict):
        #
        is_1_day_buy = True
        is_1_day_sell = True
        is_3_day_buy = True
        is_3_day_sell = True
        is_7_day_buy = False
        is_7_day_sell = False
        #
        buy_list = []
        sell_list = []
        # buy
        if is_1_day_buy:
            buy_list.append(ga_classifier_result_dict['1_day_buy'])
        if is_3_day_buy:
            buy_list.append(ga_classifier_result_dict['3_day_buy'])
        if is_7_day_buy:
            buy_list.append(ga_classifier_result_dict['7_day_buy'])
        for i, instrument_list in enumerate(buy_list):
            if i == 0:
                buy_set = set(instrument_list)
                continue
            else:
                buy_set = buy_set & set(instrument_list)
        # buy end

        # sell
        if is_1_day_sell:
            sell_list.append(ga_classifier_result_dict['1_day_sell'])
        if is_3_day_sell:
            sell_list.append(ga_classifier_result_dict['3_day_sell'])
        if is_7_day_sell:
            sell_list.append(ga_classifier_result_dict['7_day_sell'])
        for i, instrument_list in enumerate(sell_list):
            if i == 0:
                sell_set = set(instrument_list)
                continue
            else:
                sell_set = sell_set & set(instrument_list)
        # sell end

        day_buy = list(buy_set)
        day_sell = list(sell_set)

        return day_buy, day_sell

    def get_trade_instrument(self, day_buy, day_sell):
        trade_instruments_tuple = []
        for instrument in day_buy:
            trade_instruments_tuple.append(instrument, 'buy')

        for instrument in day_sell:
            trade_instruments_tuple.append(instrument, 'sell')

        time = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        oanda_logger.info("Trading decision: {}, Time: {}".format(trade_instruments_tuple, time))
        return trade_instruments_tuple

    def get_close_out_instrument(self, day_buy, day_sell):
        instruments = ['EUR_USD']
        return instruments

    def get_all_positions(self):
        time = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        url = self.get_all_positions_url
        response = requests.get(url, headers = self.headers)
        positions_list = dict(response.json())['positions']
        all_pos_list = []
        for positions_dict in positions_list:
            all_pos_list.append(positions_dict['instrument'])
        # logging
        oanda_logger.info("=============================All positions=============================")
        oanda_logger.info("Time: {}".format(time))
        oanda_logger.info("All_pos_list: {}".format(all_pos_list))
        oanda_logger.info("Pos details:\n {}".format(pprint.pformat(response.json())))
        oanda_logger.info("=============================All positions END==========================\n")
        return all_pos_list

    def close_out(self, trading_params, day_buy, day_sell):
        def get_trade_id(instrument):
            url = self.get_trade_id_url.format(self.account_id, instrument)
            response = requests.get(url, headers=self.headers)
            trade_id = dict(response.json())['trades'][0]["id"]
            return trade_id

        # ::: close_out
        time = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        instrument_in_pos = self.get_all_positions()
        print ("instrument_in_pos", instrument_in_pos)
        # ('EUR_USD', 'USD_JPY')
        close_out_instruments = self.get_close_out_instrument(day_buy, day_sell)
        close_out_instruments = set(close_out_instruments) & set(instrument_in_pos)
        if not close_out_instruments:
            # return logging
            oanda_logger.info("=============================No Close Out=============================")
            oanda_logger.info("Time: {}".format(time))
            oanda_logger.info("Day buy: {}".format(day_buy))
            oanda_logger.info("Day sell: {}".format(day_sell))
            oanda_logger.info("Hold position: {}".format(instrument_in_pos))
            oanda_logger.info("No close_out!")
            oanda_logger.info("=============================Return Trading END==========================\n")
            return

        for instrument in close_out_instruments:
            trade_id = get_trade_id(instrument)
            url = self.close_out_url.format(self.account_id, trade_id)
            response = requests.put(url, headers=self.headers)
            response_content = response.json()
            status_code = response.status_code

            # close_out logging
            oanda_logger.info("=============================Oanda Close Out=============================")
            oanda_logger.info("Close Out Time: {}".format(time))
            oanda_logger.info("Day buy: {}".format(day_buy))
            oanda_logger.info("Day sell: {}".format(day_sell))
            oanda_logger.info("Close Out instrument chosen: {}".format(instrument))
            oanda_logger.info("status_code: {}".format(status_code))
            oanda_logger.info("response_content:\n {}".format(pprint.pformat(response_content)))
            oanda_logger.info("=============================Oanda Trading END==========================\n")

    def trade(self, trading_params, day_buy, day_sell):
        time = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        # trade_instruments_tuple: (('EUR_USD', 'buy'), ('EUR_USD', 'sell')...)
        trade_instruments_tuple = self.get_trade_instrument(day_buy, day_sell)
        for trade_instrument, sell_or_buy in trade_instruments_tuple:

            if not trade_instrument:
                # return logging
                oanda_logger.info("=============================Return Trading=============================")
                oanda_logger.info("Trading Time: {}".format(time))
                oanda_logger.info("Day buy: {}".format(day_buy))
                oanda_logger.info("Day sell: {}".format(day_sell))
                oanda_logger.info("No instrument chosen")
                oanda_logger.info("=============================Return Trading END==========================\n")
                return

            body = self.body
            headers = self.headers
            url = self.order_url
            body['order']['instrument'] = trade_instrument

            # sell or buy
            if sell_or_buy == 'sell':
                body['order']['units'] = str(int(body['order']['units']) * -1)
            else:
                pass
            response = requests.post(url, headers=headers, json=body)
            response_content = response.json()
            status_code = response.status_code
            # logging
            oanda_logger.info("=============================Oanda Trading=============================")
            oanda_logger.info("Trading Time: {}".format(time))
            oanda_logger.info("Day buy: {}".format(day_buy))
            oanda_logger.info("Day sell: {}".format(day_sell))
            oanda_logger.info("Instrument chosen: {}".format(trade_instrument))
            oanda_logger.info("status_code: {}".format(status_code))
            oanda_logger.info("response_content:\n {}".format(pprint.pformat(response_content)))
            oanda_logger.info("=============================Oanda Trading END==========================\n")