def get_upper_folder_path(num, path = ''):
    if not path:
        path = os.path.dirname(os.path.abspath(__file__))
    else:
        path = os.path.dirname(path)
    num -= 1
    if num > 0:
        return get_upper_folder_path(num, path = path)
    else:
        return path







import collections
import time
import datetime
import sys
import os
current_path = get_upper_folder_path(1)
logger_path = os.path.join(current_path, 'pjslib')
sys.path.append(logger_path)

from s_logger import strategy_logger


class OandaStrategy:
    def __init__(self, data_path, ga_buy_list, ga_sell_list):
        self.start_capital = 100.0
        self.capital = self.start_capital
        self.ga_buy_list = sorted(ga_buy_list, key = lambda x:x[0])
        self.ga_sell_list = sorted(ga_sell_list, key = lambda x:x[0])
        self.buy_pos = []
        self.sell_pos = []
        self.data_path = data_path
        self.potential_close_out_list = []
        self.close_out_pair_list = []
        self.forex_data = []
        # get data_dict and date_list
        self.data_dict, self.date_list = self.read_data_into_dict(data_path)
        self.date = self.date_list[0]


    def read_data_into_dict(self, data_path):
        data_dict = collections.defaultdict(lambda: {})
        date_list = []
        with open(data_path, 'r', encoding = 'utf-8') as f:
            for line in f:
                line_list = line.split(',')
                instrument = line_list[1]
                date_str = line_list[2]
                date = time.strptime(date_str, '%m/%d/%Y')
                date = datetime.datetime(*date[:3])
                date = datetime.date(year=date.year, month=date.month, day=date.day)
                price = line_list[19]
                data_dict[instrument][date] = price
                # make the date list
                date_list.append(date)
        date_list = list(set(date_list))
        date_list = sorted(date_list)
        return data_dict, date_list

    def close_out(self):
        new_close_out_pair_list = []
        for order_pos_tuple, close_out_tuple, capital, buy_or_sell in self.close_out_pair_list:
            strategy_logger.info("======================TRANSACTION======================")
            if close_out_tuple == None:
                strategy_logger.info("order:{} has not date for closed out!".format(order_pos_tuple))
                continue
            if buy_or_sell == 'buy':
                profit_factor = 1
            elif buy_or_sell == 'sell':
                profit_factor = -1
            instrument = close_out_tuple[1]
            order_date = order_pos_tuple[0]
            close_out_date = close_out_tuple[0]
            # get bought prise
            if close_out_date == self.date:
                order_price = float(self.data_dict[instrument][order_date])
                close_out_price = float(self.data_dict[instrument][close_out_date])
                close_out_profit = profit_factor * capital * ((close_out_price - order_price)/order_price)
                self.capital += close_out_profit
                strategy_logger.info("instrument:{}".format(instrument))
                strategy_logger.info("order_date:{}, close_out_date:{}".format(order_date, close_out_date))
                strategy_logger.info("order_price:{}, close_out_price:{}".format(order_price, close_out_price))
                strategy_logger.info("date:{}, profit: {}, capital: {}".
                                     format(self.date, close_out_profit, self.capital))
                strategy_logger.info("===================TRANSACTION END=====================\n")

            else:
                new_close_out_pair_list.append((order_pos_tuple, close_out_tuple, capital, buy_or_sell))
                continue

        self.close_out_pair_list = new_close_out_pair_list


    def get_close_out_tuple(self, order_pos_tuple, is_buy):
        order_date = order_pos_tuple[0]
        instrument = order_pos_tuple[1]

        if is_buy:
            # ga_sell_list is sorted
            for sell_tuple in self.ga_sell_list:
                sell_date = sell_tuple[0]
                sell_instrument = sell_tuple[1]
                if sell_date > order_date and instrument == sell_instrument:
                    return sell_tuple
                else:
                    return None
        else:
            for buy_tuple in self.ga_buy_list:
                buy_date = buy_tuple[0]
                buy_instrument = buy_tuple[1]
                if buy_date > order_date and instrument == buy_instrument:
                    return buy_tuple
                else:
                    return None

    def update_close_out_pair_list(self):
        # update close_out_pair_list for buy
        for buy_tuple in self.ga_buy_list:
            tuple_date = buy_tuple[0]
            if tuple_date == self.date:
                order_pos_tuple = buy_tuple
                close_out_tuple = self.get_close_out_tuple(order_pos_tuple, is_buy = True)
                capital = self.capital
                buy_or_sell = 'buy'
                self.close_out_pair_list.append((order_pos_tuple, close_out_tuple, capital, buy_or_sell))
        # update close_out_pair_list for sell
        for sell_tuple in self.ga_sell_list:
            tuple_date = sell_tuple[0]
            if tuple_date == self.date:
                order_pos_tuple = sell_tuple
                close_out_tuple = self.get_close_out_tuple(order_pos_tuple, is_buy = False)
                capital = self.capital
                buy_or_sell = 'sell'
                self.close_out_pair_list.append((order_pos_tuple, close_out_tuple, capital, buy_or_sell))


    def get_profit(self):
        profit = "{:2.2f}".format((self.capital - self.start_capital)/self.capital)
        return profit

    def compute_profit(self):
        #strategy_logger.info("sell_list:{}".format(self.ga_sell_list))
        i = 0
        while self.date <= self.date_list[-1]:
            self.update_close_out_pair_list()
            strategy_logger.debug("close_out_pair_list:{}".format(self.close_out_pair_list))
            #print ("close_out_pair_list: ", self.close_out_pair_list[0])
            self.close_out()
            i += 1
            self.date = self.date_list[i]
            if self.capital <= 0:
                strategy_logger.info("==================GO bankruptcy!!!==================")
                self.capital = 0
                break

            print ("date: {}, capital:{}".format(self.date, self.capital))


