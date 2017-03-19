# import from pjslib
from pjslib.general import get_upper_folder_path
from pjslib.general import accepts
from pjslib.logger import oanda_logger
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
        #{date_object:{'close_out':['EUR_USD', ...]}}
        self.strategy_1_dict = collections.defaultdict(lambda: collections.defaultdict(lambda: []))
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

        
        
    def s1_get_day_buy_sell(self, ga_classifier_result_dict):
        #
        mode = self.mode
        date_today = self.date_today
        delta = datetime.timedelta(days=1) 
        #
        buy_list = []
        sell_list = []
        # buy
        if mode == '1_day':
            # buy
            buy_list.extend(ga_classifier_result_dict['1_day_buy'])
            # sell
            sell_list.extend(ga_classifier_result_dict['1_day_sell'])
        elif mode == '3_day':
            # buy
            buy_list.extend(ga_classifier_result_dict['3_day_buy'])
            # sell
            sell_list.extend(ga_classifier_result_dict['3_day_sell'])
        elif mode == '7_day':
            # buy
            buy_list.extend(ga_classifier_result_dict['7_day_buy'])
            # sell
            sell_list.extend(ga_classifier_result_dict['7_day_sell'])
        else:
            oanda_logger.error("s1_get_day_buy_sell mode {} is not valid".format(mode))
            sys.exit(0)
        # sell

        day_buy = list(set(buy_list) - set(sell_list))
        day_sell = list(set(sell_list) - set(buy_list))
        
        close_out_target = list(set(day_buy + day_sell))
        
        # get the close out target for buy and close
        for target in close_out_target:
            if mode == '1_day':
                close_out_date = date_today + datetime.timedelta(days=1)
            elif mode == '3_day':
                close_out_date = date_today + datetime.timedelta(days=3)
            elif mode == '7_day':
                close_out_date = date_today + datetime.timedelta(days=7)
            #{date_object:{'close_out':['EUR_USD', ...]}}
            
            # TODO holiday is not included
            # add 1 or 2 days if the date is at weekends
            weekend = set([5, 6]) 
            # 5 for saturday, 6 for sunday
            if close_out_date.weekday() == 5:
                close_out_date += datetime.timedelta(days=2)
            elif close_out_date.weekday() == 6:
                close_out_date += datetime.timedelta(days=1)
            else:
                pass
            self.strategy_1_dict[close_out_date]['close_out'].append(target)
            

        
        
        # write strategy_1_dict to local file, update the previous dict
        strategy1_file_path = self.strategy1_file_path
        
        try:
            with open(strategy1_file_path, 'r', encoding = 'utf-8') as f:
                strategy1_dict_json = json.load(f)
        except FileNotFoundError:
            strategy1_dict_json = None
            
            
            
        #if strategy1_dict is empty
        if not strategy1_dict_json:
            strategy1_dict_json = self.strategy_1_dict.copy()
        else:
            for key, value in self.strategy_1_dict.items():
                date_key = key.strftime("%Y-%m-%d")
                if strategy1_dict_json.get(date_key) == None:
                    strategy1_dict_json[date_key]['close_out'] = []
                strategy1_dict_json[date_key]['close_out'].extend(value['close_out'])
                
        with open (strategy1_file_path, 'w', encoding = 'utf-8') as f:
            json.dump(strategy1_dict_json, f, indent = 4)
        # ===================================================================
        
        oanda_logger.info("day_buy: {}".format(day_buy))
        oanda_logger.info("day_sell: {}".format(day_sell))
        return day_buy, day_sell
        
        
    # ga_classifier_result_dict {'1_day_buy':['USD/JPY']}
    def get_day_buy_sell(self, ga_classifier_result_dict):
        #
        is_1_day_buy = self.is_1_day_buy
        is_1_day_sell = self.is_1_day_sell
        is_3_day_buy = self.is_3_day_buy
        is_3_day_sell = self.is_3_day_sell
        is_7_day_buy = self.is_7_day_buy
        is_7_day_sell = self.is_7_day_sell
        #
        buy_list = []
        sell_list = []
        buy_set = set()
        sell_set = set()
        # buy
        if is_1_day_buy:
            buy_list.extend(ga_classifier_result_dict['1_day_buy'])
        if is_3_day_buy:
            buy_list.extend(ga_classifier_result_dict['3_day_buy'])
        if is_7_day_buy:
            buy_list.extend(ga_classifier_result_dict['7_day_buy'])
            

        for i, instrument_list in enumerate(buy_list):
            if i == 0:
                buy_set = set(instrument_list)
                continue
            else:
                buy_set = buy_set & set(instrument_list)
        # buy end

        # sell
        if is_1_day_sell:
            sell_list.extend(ga_classifier_result_dict['1_day_sell'])
        if is_3_day_sell:
            sell_list.extend(ga_classifier_result_dict['3_day_sell'])
        if is_7_day_sell:
            sell_list.extend(ga_classifier_result_dict['7_day_sell'])
        for i, instrument_list in enumerate(sell_list):
            if i == 0:
                sell_set = set(instrument_list)
                continue
            else:
                sell_set = sell_set & set(instrument_list)
        # sell end

        # if forex appear in both set, delete it
        buy_set_complete = buy_set.copy()
        sell_set_complete = sell_set.copy()
        buy_set -= sell_set_complete
        sell_set -= buy_set_complete
        day_buy = list(buy_set)
        day_sell = list(sell_set)
        oanda_logger.info("day_buy: {}".format(day_buy))
        oanda_logger.info("day_sell: {}".format(day_sell))
        return day_buy, day_sell

    def get_trade_instrument(self, day_buy, day_sell):
        trade_instruments_tuple = []
        for instrument in day_buy:
            trade_instruments_tuple.append((instrument, 'buy'))

        for instrument in day_sell:
            trade_instruments_tuple.append((instrument, 'sell'))

        time = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        oanda_logger.info("Trading decision: {}, Time: {}".format(trade_instruments_tuple, time))
        return trade_instruments_tuple

    def get_close_out_instrument(self, day_buy, day_sell, strategy = 's2'):
        print ("=============get_close_out_instrument===============")
        instruments = []
        if strategy == 's2':
            # close out the sell trade
            for instrument in day_buy:
                for instrument_pos, buy_or_sell in self.pos_detail_dict.items():
                    if instrument == instrument_pos and buy_or_sell == 'sell':
                        instruments.append(instrument_pos)
            # close out the buy trade
            for instrument in day_sell:
                for instrument_pos, buy_or_sell in self.pos_detail_dict.items():
                    oanda_logger.debug("instrument: {}, instrument_pos:{}， buy_or_sell:{}"
                                       .format(instrument, instrument_pos, buy_or_sell))
                    if instrument == instrument_pos and buy_or_sell == 'buy':
                        instruments.append(instrument_pos)
                        
        elif strategy == 's1':
            date_today_str = self.date_today.strftime("%Y-%m-%d")
            strategy1_file_path = self.strategy1_file_path
            with open (strategy1_file_path, 'r', encoding = 'utf-8') as f:
                strategy1_dict = json.load(f)
            if strategy1_dict.get(date_today_str):
                instruments = strategy1_dict[date_today_str]['close_out']
            else:
                instruments = []
        
        #instruments = ['EUR_USD']
        time = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        oanda_logger.info("Close_out instruments: {}, Time: {}".format(instruments, time))
        return instruments

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
            if short_units != 0 and long_units == 0:
                if short_units > 0:
                    buy_or_sell = 'buy'
                elif short_units < 0:
                    buy_or_sell = 'sell'
            elif long_units != 0 and short_units == 0:
                if long_units > 0:
                    buy_or_sell = 'buy'
                elif long_units < 0:
                    buy_or_sell = 'sell'
            else:
                oanda_logger.error("ERROR HAPPEND AT get_all_positions! long_unit, short unit")
                sys.exit(0)
            self.pos_detail_dict[instrument] = buy_or_sell

        # logging
        oanda_logger.info("=============================All positions=============================")
        oanda_logger.info("Time: {}".format(time))
        oanda_logger.info("All_pos_list: {}".format(all_pos_list))
        oanda_logger.info("Pos details:\n {}".format(pprint.pformat(response.json())))
        oanda_logger.info("Buy/Sell details:\n {}".format(pprint.pformat(dict(self.pos_detail_dict))))
        oanda_logger.info("=============================All positions END==========================\n")
        return all_pos_list

    def close_out(self, trading_params, day_buy, day_sell, strategy = 's2'):
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
        close_out_instruments = self.get_close_out_instrument(day_buy, day_sell, strategy = strategy)
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