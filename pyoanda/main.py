# import from pjslib
import collections
import os
import re
import sys

from pjslib.general import get_upper_folder_path
from pjslib.logger import oanda_logger
from read_forex_data import ReadForexData
from read_parameters import ReadParameters
from sub.sub_reader import SubReader
''' MAIN FUNCTION FOR TRADING '''
#=====================SUB_PROCESS================
code_main_folder = get_upper_folder_path(2)
sys.path.append(code_main_folder)
sys.path.append(os.path.join(code_main_folder, 'code'))
#print(sys.path)
#sys.path.append(os.path.join(code_main_folder, 'code', 'pjslib'))
from single_chromo_cls_result import get_single_chromo_cls_result
import subprocess
def run_python(path):
    cwd = os.path.dirname(os.path.realpath(path))
    subprocess.call("python {}".format(path), shell=True, cwd = cwd)
#from oanda_ga_classifier import ga_classifier
#========================================================================
# SET TRADING_TRACE_DATE
TRADING_TRACE_DATE = 100



#=================================================WRITE OANDA PARAMETERS================================================
# create sub_reader
sub_reader = SubReader()

code_main_folder = get_upper_folder_path(2)
# WRITE GA oanda parameters
oanda_main_w_parameter__path = os.path.join(code_main_folder, 'code', 'parameters', 'write_oanda_parameters.py')
oanda_main_parameter_json__path = os.path.join(code_main_folder, 'code', 'parameters', 'parameter.json')
run_python(oanda_main_w_parameter__path)

# adjust parameters and write new json file, set the date range of prediction
import datetime
parameter_dict = sub_reader.read_parameters(oanda_main_parameter_json__path)
today = datetime.datetime.today()
delta = datetime.timedelta(days = TRADING_TRACE_DATE)
previous_date_limit = today - delta
today_str = datetime.datetime.today().strftime("%m/%d/%Y")
previous_date_limit_str = previous_date_limit.strftime("%m/%d/%Y")
parameter_dict['input']['training_date_start'] = previous_date_limit_str
parameter_dict['input']['training_date_end'] = today_str
sub_reader.write_json(oanda_main_parameter_json__path, parameter_dict)


# WRITE process data oanda parameters
p_data_parameters__path = os.path.join(code_main_folder, 'pyoanda', 'parameters', 'write_parameters.py')
p_data_parameters_json__path = os.path.join(code_main_folder, 'pyoanda', 'parameters', 'p_data_parameters.json')
p_data_parameters_dict = sub_reader.read_parameters(p_data_parameters_json__path)
# get the data path
oanda_forex_trading_data_path = os.path.join(code_main_folder, 'data', 'oanda', 'oanda_forex_trading_data.txt')


run_python(p_data_parameters__path)
# modify parameters and save new json

p_data_parameters_dict['date_range'] = TRADING_TRACE_DATE
p_data_parameters_dict['mode'] = 'trading'
sub_reader.write_json(p_data_parameters_json__path, p_data_parameters_dict)
#=================================================WRITE OANDA PARAMETERS END============================================

# =========================================READING UP-TO-DATE-FOREX-DATA================================================
def read_up_to_date_forex_data():
    # set mode to trading
    # (1.) read parameters
    reader1 = ReadParameters(file_name = 'p_data_parameters.json')
    parameter_dict = reader1.read_parameters(reader1.path)
    print("parameter_dict: ", parameter_dict)

    # (2.) read forex data
    read_forex_data = ReadForexData(parameter_dict)
    read_forex_data.read_onanda_data()
    read_forex_data.write_forex_dict_to_file()

#read_up_to_date_forex_data()
# =========================================READING UP-TO-DATE-FOREX-DATA================================================

# =========================================READ chromosome==============================================================
def get_ga_classifier_result_dict():
    oanda_logger.info("======================GETTING FOREX RETURN START======================")
    import random
    today = datetime.datetime.today()
    today = datetime.date(year = today.year, month = today.month, day = today.day)
    ga_classifier_result_dict = collections.defaultdict(lambda :[])
    chromosome_strategy_chosen_path = os.path.join(code_main_folder, 'pyoanda',  'chromosome_strategy_chosen.txt')
    with open(chromosome_strategy_chosen_path, 'r', encoding = 'utf-8') as f:
        for line in f:
            chromosome_type = re.findall(r'#([A-Za-z0-9_]+)#', line)[0]
            chromosome = re.findall(r':chromosome#([0-9]+)#END', line)[0]
            chromosome_bits = list(chromosome)
            # convert str to int
            chromosome_bits = [int(x) for x in chromosome_bits]
            print ("len_chromosome: ", len(chromosome_bits))
            #chromosome_bits = [random.sample([0,1],1)[0] for x in range(len(chromosome_bits))]

            oanda_logger.info("chromosome_bits: {}".format(''.join([str(x) for x in chromosome_bits])))
            #(chromosome_bits, chromosome_type, parameter_path, data_path, output_path, trading = False
            # cls_result_today: (datetime.date(2017, 2, 17), 'GBP_USD')
            cls_result = get_single_chromo_cls_result(chromosome_bits, chromosome_type, oanda_main_parameter_json__path,
                                                  oanda_forex_trading_data_path, trading = True)

            oanda_logger.debug("chromosome_type: {}, cls_result :{}".format(chromosome_type, cls_result))
            # test whether this chromosome has return any forex for any date
            if cls_result == None:
                oanda_logger.info("{} has no forex return for any date".format(chromosome_type))
            else:
                cls_result_today = cls_result[0]
                # test whether the fetech result is today
                date_cls = cls_result_today[0]
                if date_cls == today:
                    ga_classifier_result_dict[chromosome_type].append(cls_result_today[1])
                    oanda_logger.info("{} has return forex {} for {}".format(chromosome_type, cls_result_today, today))
                else:
                    oanda_logger.info("{} has no forex return for {}".format(chromosome_type, today))

    print ("ga_classifier_result_dict: ", dict(ga_classifier_result_dict))
    oanda_logger.info("======================GETTING FOREX RETURN END======================")
    return ga_classifier_result_dict
# =========================================READ chromosome END==============================================================









# =========================================TRADING
from oanda_trading import OandaTrading
import time
import schedule

oanda_trading = OandaTrading()

# read parameters
trading_params = {}
strategy = 's1'

def main_loop():
    # (0.) see if market is open
    is_market_open = oanda_trading.is_market_open()
    if not is_market_open:
        oanda_trading.modify_close_out_date()
        sys.exit()

    oanda_logger.info("===============adopted strategy: {}===============".format(strategy))
    # (1.) Update Forex Data
    read_up_to_date_forex_data()

    # (2.) get ga_classifier_result_dict
    ga_classifier_result_dict = get_ga_classifier_result_dict()

    # (3.) get day_buy/day_sell
    if strategy == 's2':
        day_buy, day_sell = oanda_trading.get_day_buy_sell(ga_classifier_result_dict)
    elif strategy == 's1':
        day_buy, day_sell = oanda_trading.s1_get_day_buy_sell(ga_classifier_result_dict)

    # TODO reinforcement learning, action outputs close order date, units, which shoule be the input of close_out and trade

    # (4.) close out
    oanda_trading.close_out(trading_params, day_buy, day_sell, strategy = strategy)
    time.sleep(3)

    # (5.) buy
    oanda_trading.trade(trading_params, day_buy, day_sell)
    time.sleep(3)

    # (6.) show position and archive positions
    oanda_trading.get_all_positions()


    
main_loop()
#schedule.every(3).seconds.do(main_loop)
#schedule.every().day.at("10:30").do(main_loop)

#while not oanda_trading.isEnd:
#    schedule.run_pending()
    




