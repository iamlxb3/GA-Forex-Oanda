def find_upper_level_folder_path(num, path=''):
    if not path:
        path = os.path.dirname(os.path.abspath(__file__))
    else:
        path = os.path.dirname(path)
    num -= 1
    if num > 0:
        return find_upper_level_folder_path(num, path=path)
    else:
        return path

# import single_chromo_cls_result
import sys
import os
code_main_folder = find_upper_level_folder_path(2)
sys.path.append(code_main_folder)
sys.path.append(os.path.join(code_main_folder, 'code'))
#sys.path.append(os.path.join(code_main_folder, 'pyoanda'))
from single_chromo_cls_result import get_single_chromo_cls_result
from oanda_strategy import OandaStrategy


# import subprocess
import os

import re
import subprocess
import collections
import pprint


# TODO, pending for this feature, it has to include buy, sell switch, too complicated
# >>> 7*7  number of chromosome_buy combo * number of chromosome_sell combo
# 49
# >>> 49*64 chromosome_combo_list = 64, if every type(1-day) has only 2 chromosome for buy and 2 chromosome for sell
# 3136
# >>>


main_path = find_upper_level_folder_path(2)
chosen_chromosome_path = os.path.join(main_path, 'code', 'chromosome', 'conserved_best_chromosome.txt')
oanda_main_parameter_json__path = os.path.join(code_main_folder, 'code', 'parameters', 'parameter.json')
oanda_forex_testing_data_path = os.path.join(code_main_folder, 'data', 'oanda', 'oanda_forex_testing_data.txt')

# initialize and read the chromosome into dict
chosen_chromosome_dict = collections.defaultdict(lambda:[])
chosen_chromosome_dict['1_day_buy']
chosen_chromosome_dict['1_day_sell']
chosen_chromosome_dict['3_day_buy']
chosen_chromosome_dict['3_day_sell']
chosen_chromosome_dict['7_day_buy']
chosen_chromosome_dict['7_day_sell']


# read the chosen chromosome of 1,3,7 days
with open(chosen_chromosome_path, 'r', encoding = 'utf-8') as f:
    for line in f:
        day = re.findall(r'#([0-9A-Za-z_]+)#', line)[0]
        chromosome = re.findall(r'chromosome#([0-9]+)#END', line)[0]
        chromosome_list = list(chromosome)
        chromosome_list = [int(x) for x in chromosome_list]
        chosen_chromosome_dict[day].append(chromosome_list)

print(chosen_chromosome_dict)

chromosome_combo_dict = collections.defaultdict(lambda:[])


for key, value_list in chosen_chromosome_dict.items():
    for chromosome_value in value_list:
        chromosome_combo_dict[key].append((key, chromosome_value, True))
        chromosome_combo_dict[key].append((key, chromosome_value, False))

# add empty tuple to those unwritten chromosome
key_list = ['1_day_buy', '1_day_sell', '3_day_buy', '3_day_sell', '7_day_buy', '7_day_sell']
for key in key_list:
    if not chromosome_combo_dict[key]:
        chromosome_combo_dict[key].append(tuple())



print ("chromosome_combo_dict", chromosome_combo_dict)
# make the chromosome_combo_list
chromosome_combo_list = []
for chromosome_1_buy in chromosome_combo_dict['1_day_buy']:
    for chromosome_1_sell in chromosome_combo_dict['1_day_sell']:
        for chromosome_3_buy in chromosome_combo_dict['3_day_buy']:
            for chromosome_3_sell in chromosome_combo_dict['3_day_sell']:
                for chromosome_7_buy in chromosome_combo_dict['7_day_buy']:
                    for chromosome_7_sell in chromosome_combo_dict['7_day_sell']:
                        chromosome_combo = (chromosome_1_buy, chromosome_1_sell, chromosome_3_buy, chromosome_3_sell,
                                            chromosome_7_buy, chromosome_7_sell)
                        chromosome_combo_list.append(chromosome_combo)

print(chromosome_combo_list[-1])
print(len(chromosome_combo_list))





for chromosome_combo in chromosome_combo_list:
    buy_set = set()
    sell_set = set()
    is_buy_set_initialized = False
    is_sell_set_initialized = False
    for i, chromosome_detail in enumerate(chromosome_combo):
        if not chromosome_detail:
            continue
        chromosome_type = chromosome_detail[0]
        is_buy = re.findall(r'buy', chromosome_type)
        is_sell = re.findall(r'sell', chromosome_type)
        chromosome_bit_list = chromosome_detail[1]
        is_chromosome_chosen = chromosome_detail[2]
        if not chromosome_bit_list:
            print ("chromosome_type has not chromosome: ", chromosome_bit_list)
            continue
        if not is_chromosome_chosen:
            print ("chromosome_type chosen state: ", is_chromosome_chosen)
            continue
        cls_result,testing_data_dict = get_single_chromo_cls_result(chromosome_bit_list, chromosome_type, oanda_main_parameter_json__path,
                                                  oanda_forex_testing_data_path, return_data_dict = True)
        if cls_result == None:
            cls_result = []

        # update buy set
        if not is_buy_set_initialized and is_buy:
            buy_set = set(cls_result)
            is_buy_set_initialized = True
        elif is_buy_set_initialized and is_buy:
            buy_set &= set(cls_result)
        #
        # update sell set
        if not is_sell_set_initialized and is_sell:
            sell_set = set(cls_result)
            is_sell_set_initialized = True
        elif is_sell_set_initialized and is_sell:
            sell_set &= set(cls_result)

    #
    buy_set_complete = buy_set.copy()
    sell_set_complete = sell_set.copy()
    buy_set -= sell_set_complete
    sell_set -= buy_set_complete
    ga_buy_list = sorted(list(buy_set), key = lambda x:x[0])
    ga_sell_list = sorted(list(sell_set), key = lambda x: x[0])
    print ("buy_set_len", len(buy_set))
    print ("sell_set_len", len(sell_set))
    #(data_path, ga_buy_list, ga_sell_list):
    oanda_strategy = OandaStrategy(oanda_forex_testing_data_path, ga_buy_list, ga_sell_list)
    oanda_strategy.compute_profit()
    sys.exit(0)





















# ===============================================BACK UP================================================================

# # chromosome_combo_list = [(1_c1, 3_c1, 7_c1), (1_c2, 3_c2, 7_c2), ...]
# chromosome_combo_list = []
# chromosome_buy_in_use_list = [(True, True, True), (True, True, False), (True, False, True),
#                           (False, True, True), (True, False, False), (False, True, False),
#                           (False, False, True)
#                           ]
# chromosome_sell_in_use_list = [(True, True, True), (True, True, False), (True, False, True),
#                           (False, True, True), (True, False, False), (False, True, False),
#                           (False, False, True)
#                           ]
