# import from pjslib
from pjslib.general import get_upper_folder_path
from pjslib.general import accepts
from pjslib.logger import logger1
#================================================
import random
import pprint
import os
import sys
import schedule
#================================================
from oanda_trading import OandaTrading
from ga_classifier import ga_classifier


oanda_trading = OandaTrading

# read parameters
trading_params = {}

def main_loop():
    oanda_trading.update_data()
    ga_classifier_result_dict = ga_classifier()
    day_buy, day_sell = oanda_trading.get_day_buy_sell(ga_classifier_result_dict)
    oanda_trading.trade(trading_params, day_buy, day_sell)

while not oanda_trading.isEnd:
    schedule.every(15).minutes.do(main_loop)
    # schedule.every().day.at("10:30").do(job)




