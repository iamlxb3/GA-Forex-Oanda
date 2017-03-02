# import from pjslib
from pjslib.general import get_upper_folder_path
from pjslib.general import accepts
from pjslib.logger import oanda_logger
#================================================
import random
import pprint
import os
import sys
import schedule
import time
#================================================
from read_parameters import ReadParameters
from read_forex_data import ReadForexData
from oanda_trading import OandaTrading


#from oanda_ga_classifier import ga_classifier


# =========================================READING UP-TO-DATE-FOREX-DATA================================================
# (1.) read parameters
reader1 = ReadParameters(file_name = 'p_data_parameters.json')
parameter_dict = reader1.read_parameters(reader1.path)
print(parameter_dict)
# (2.) read forex data
read_forex_data = ReadForexData(parameter_dict)
read_forex_data.read_onanda_data()
read_forex_data.write_forex_dict_to_file()







# =========================================READING UP-TO-DATE-FOREX-DATA================================================


# =========================================TRADING

# oanda_trading = OandaTrading()
#
# # read parameters
# trading_params = {}
#
#
# def main_loop():
#     # (1.) read parameters
#     start_time = ''
#     end_time = ''
#     oanda_trading.update_data(start_time, end_time)
#     #ga_classifier_result_dict = ga_classifier()
#     ga_classifier_result_dict = ''
#     day_buy, day_sell = oanda_trading.get_day_buy_sell(ga_classifier_result_dict)
#     oanda_trading.close_out(trading_params, day_buy, day_sell)
#     time.sleep(3)
#     oanda_trading.trade(trading_params, day_buy, day_sell)
#     time.sleep(3)
#     oanda_trading.get_all_positions()
#
#
# schedule.every(5).seconds.do(main_loop)
# while not oanda_trading.isEnd:
#     schedule.run_pending()
#     # schedule.every().day.at("10:30").do(job)




