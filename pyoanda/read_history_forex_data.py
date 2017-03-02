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


from read_parameters import ReadParameters
from read_forex_data import ReadForexData
from oanda_trading import OandaTrading


# =========================================READING UP-TO-DATE-FOREX-DATA================================================
# (1.) read parameters
reader1 = ReadParameters(file_name = 'p_data_parameters.json')
parameter_dict = reader1.read_parameters(reader1.path)
print(parameter_dict)
# (2.) read forex data
read_forex_data = ReadForexData(parameter_dict)
read_forex_data.read_onanda_data()
read_forex_data.write_forex_dict_to_file()

# ===========================================get the max, min and average of the data
read_forex_data.get_data_distribution(read_forex_data.file_path)
