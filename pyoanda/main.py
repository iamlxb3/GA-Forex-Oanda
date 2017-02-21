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
code_path = os.path.join(get_upper_folder_path(4), 'code')
print ("code_path: ", code_path)
sys.path.insert(0, code_path)

from oanda_trading import OandaTrading
#from oanda_ga_classifier import ga_classifier


oanda_trading = OandaTrading()

# read parameters
trading_params = {}
def test():
    print ("testttttt")


def main_loop():
    # (1.) read parameters
    start_time = ''
    end_time = ''
    oanda_trading.update_data(start_time, end_time)
    #ga_classifier_result_dict = ga_classifier()
    ga_classifier_result_dict = ''
    day_buy, day_sell = oanda_trading.get_day_buy_sell(ga_classifier_result_dict)
    oanda_trading.close_out(trading_params, day_buy, day_sell)
    time.sleep(3)
    oanda_trading.trade(trading_params, day_buy, day_sell)
    time.sleep(3)
    oanda_trading.get_all_positions()


schedule.every(5).seconds.do(main_loop)
while not oanda_trading.isEnd:
    schedule.run_pending()
    # schedule.every().day.at("10:30").do(job)




