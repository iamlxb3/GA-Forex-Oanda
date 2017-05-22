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
import os
import copy
import json



class OandaTrading():
    def __init__(self):
        self.date_today = datetime.datetime.today().date()
        self.is_1_day_buy = False
        self.is_1_day_sell = False
        self.is_3_day_buy = True
        self.is_3_day_sell = True
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

        # close_out_file_path
        close_out_file = 'close_out_order.txt'
        folder = 'order'
        current_folder = get_upper_folder_path(1)
        self.close_out_file_path = os.path.join(current_folder, folder, close_out_file)


    def update_data(self, start_time, end_time, mode = 'trading'):
        pass


    def s1_get_close_out_date(self):
        # get place order date
        start_date = self.date_today
        mode = self.mode

        # get close order date
        if mode == '1_day':
            close_out_date = start_date + datetime.timedelta(days=1)
        elif mode == '3_day':
            close_out_date = start_date + datetime.timedelta(days=3)
        elif mode == '7_day':
            close_out_date = start_date + datetime.timedelta(days=7)

        end_date = copy.copy(close_out_date)

        # ===========================================================
        # count the saturday/sunday between place/close order date
        # ===========================================================
        while start_date != end_date + delta:
            if start_date.weekday() == 5 or start_date.weekday() == 6:
                close_out_date += delta
            start_date += delta

        if close_out_date.weekday() == 5:
            close_out_date = close_out_date + delta + delta
        elif close_out_date.weekday() == 6:
            close_out_date += delta
        # ===========================================================
        close_out_date = close_out_date.strftime("%Y-%m-%d")
        return close_out_date


    def s1_get_day_buy_sell(self, ga_classifier_result_dict):
        mode = self.mode
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


        buy_set = set(buy_list)

        # sell
        if is_1_day_sell:
            sell_list.extend(ga_classifier_result_dict['1_day_sell'])
        if is_3_day_sell:
            sell_list.extend(ga_classifier_result_dict['3_day_sell'])
        if is_7_day_sell:
            sell_list.extend(ga_classifier_result_dict['7_day_sell'])

        sell_set = set(sell_list)

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

    def get_close_out_instrument(self, day_buy, day_sell, strategy = 's1'):
        print ("=============get_close_out_instrument===============")
        instrument_list = []
        unit_list = []
        line_id_list = []
        # if strategy == 's2':
        #     # close out the sell trade
        #     for instrument in day_buy:
        #         for instrument_pos, buy_or_sell in self.pos_detail_dict.items():
        #             if instrument == instrument_pos and buy_or_sell == 'sell':
        #                 instruments.append(instrument_pos)
        #     # close out the buy trade
        #     for instrument in day_sell:
        #         for instrument_pos, buy_or_sell in self.pos_detail_dict.items():
        #             oanda_logger.debug("instrument: {}, instrument_pos:{}， buy_or_sell:{}"
        #                                .format(instrument, instrument_pos, buy_or_sell))
        #             if instrument == instrument_pos and buy_or_sell == 'buy':
        #                 instruments.append(instrument_pos)

        if strategy == 's1':
            today_str = self.date_today.strftime("%Y-%m-%d")
            with open(self.close_out_file_path, 'r') as f:
                for i, line in enumerate(f):
                    if line == '\n':
                        continue
                    line_list = line.split(',')
                    date_str = line_list[1]
                    if today_str != date_str:
                        continue
                    else:
                        instrument = line_list[0]
                        units = str(line_list[2])
                        instrument_list.append(instrument)
                        unit_list.append(units)
                        line_id_list.append(i)
            # date_today_str = self.date_today.strftime("%Y-%m-%d")
            # strategy1_file_path = self.strategy1_file_path
            # with open (strategy1_file_path, 'r', encoding = 'utf-8') as f:
            #     strategy1_dict = json.load(f)
            # if strategy1_dict.get(date_today_str):
            #     instruments = strategy1_dict[date_today_str]['close_out']
            # else:
            #     instruments = []

        #instruments = ['EUR_USD']
        time = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        oanda_logger.info("Close_out instruments: {}, units: {}, Time: {}".format(instrument_list, unit_list,  time))
        return instrument_list, unit_list, line_id_list

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
        #

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
        close_out_instruments, units_list, line_id_list = self.get_close_out_instrument(day_buy, day_sell, strategy = strategy)
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

        # get close out id
        close_out_id_list = []
        with open (self.close_out_file_path, 'r') as f:
            for line in f:
                if line == '\n':
                    continue
                line_list = line.strip().split(',')
                date = line_list[1]
                id =line_list[-1]
                date_temp = time.strptime(date, '%Y%m%d')
                date_obj = datetime.datetime(*date_temp[:3])
                if self.date_today == date_obj:
                    close_out_id_list.append(id)

        if not close_out_id_list:
            print ("No close out forex for {}".format())

        for i, trade_id in enumerate(close_out_id_list):

            url = self.close_out_url.format(self.account_id, trade_id)
            response = requests.put(url, headers=self.headers, json=body)
            response_content = response.json()
            status_code = response.status_code

            # ===============================================================================
            # delete the close_out_order line if close out is done succesfully
            # TODO change status_code
            if status_code == '200':
                delete_line_id = line_id_list[i]
                with open (self.close_out_file_path, 'r') as f:
                    file_lines = f.readlines()
                new_file_lines = [x for i,x in enumerate(file_lines) if i != delete_line_id]
                with open(self.close_out_file_path, 'w') as f:
                    for new_line in new_file_lines:
                        f.write(new_line)
                        f.write('\n')
            # ===============================================================================

            # close_out logging
            oanda_logger.info("=============================Oanda Close Out=============================")
            oanda_logger.info("Close Out Time: {}".format(time))
            oanda_logger.info("Close Out trade_id: {}".format(trade_id))
            oanda_logger.info("status_code: {}".format(status_code))
            oanda_logger.info("response_content:\n {}".format(pprint.pformat(response_content)))
            oanda_logger.info("=============================Oanda Trading END==========================\n")


    def close_out2(self,strategy='s2'):
        oanda_logger.info("=============================Oanda Close Out=============================")
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
                if self.date_today == date_obj:
                    close_out_id_list.append(id)

        if not close_out_id_list:
            oanda_logger.info("No close out forex for {}".format(date))

        for i, trade_id in enumerate(close_out_id_list):

            url = self.close_out_url.format(self.account_id, trade_id)
            response = requests.put(url, headers=self.headers)
            response_content = response.json()
            status_code = response.status_code
            oanda_logger.info("trade_id: ", trade_id)
            oanda_logger.info("response_content: ", response_content)
            oanda_logger.info("status_code: ", status_code)
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
                oanda_logger.info("Close out trade_id {} succesfully!".format(trade_id))
            else:
                oanda_logger.info("trade_id {} does not hold any position!".format(trade_id))
            # ===============================================================================
        oanda_logger.info("=============================Oanda Close Out END=============================\n")


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
            body['order']['units'] = '50'

            # sell or buy
            if sell_or_buy == 'sell':
                body['order']['units'] = str(int(body['order']['units']) * -1)
            else:
                pass
            response = requests.post(url, headers=headers, json=body)
            response_content = response.json()
            status_code = response.status_code
            last_transaction_id =  response_content['lastTransactionID']
            # TODO update close_out_order.txt
            if status_code == '201':
                closed_out_date = self.s1_get_close_out_date()
                self.update_close_out_order(trade_instrument, sell_or_buy, closed_out_date, last_transaction_id)

            # logging
            oanda_logger.info("=============================Oanda Trading=============================")
            oanda_logger.info("Trading Time: {}".format(time))
            oanda_logger.info("Day buy: {}".format(day_buy))
            oanda_logger.info("Day sell: {}".format(day_sell))
            oanda_logger.info("Instrument chosen: {}".format(trade_instrument))
            oanda_logger.info("status_code: {}".format(status_code))
            oanda_logger.info("response_content:\n {}".format(pprint.pformat(response_content)))
            oanda_logger.info("=============================Oanda Trading END==========================\n")

    def is_market_open(self):

        today_date = datetime.datetime.today().strftime("%Y-%m-%d")


        IsMarketOpen = True
        if not IsMarketOpen:
            oanda_logger.info("{}'s forex market is closed!".format(today_date))
        return IsMarketOpen

    def modify_close_out_date(self):
        today_date_obj = datetime.datetime.today().date()
        today_date = today_date_obj.strftime("%Y-%m-%d")
        delta = datetime.timedelta(days=1)

        # modify date
        new_close_out_list = []
        with open(self.close_out_file_path, 'r') as f:
            for line in f:
                if line == '\n':
                    continue
                line_list = line.split(',')
                date = line_list[1]
                if today_date == date:
                    new_date_obj = today_date_obj + delta
                    new_date = new_date_obj.strftime("%Y-%m-%d")
                    line_list[1] = new_date

                line_list_str = ','.join(line_list)
                print ("line_list_str: ", line_list_str)
                new_close_out_list.append(line_list_str)
        #

        # update and write
        with open(self.close_out_file_path, 'w') as f:
            for line_str in new_close_out_list:
                f.write(line_str)
                f.write('\n')
        #


    def update_close_out_order(self, trade_instrument, sell_or_buy, closed_out_date, units, last_transaction_id):
        line_list = [trade_instrument, closed_out_date, units, sell_or_buy, last_transaction_id]
        line_str = ','.join(line_list)

        # write new closed out date
        with open(self.close_out_file_path, 'a') as f:
            f.write(line_str)
            f.write('\n')
        #