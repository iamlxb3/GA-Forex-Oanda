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


# =================================================
import sys
import os
# import from pjslib
parent_folder = get_upper_folder_path(1)
sys.path.append(os.path.join(parent_folder, 'pjslib'))
sys.path.append(os.path.join(parent_folder))

from general import get_upper_folder_path
from general import accepts
from logger import logger2



#================================================
import os

import json
import re
import collections
import random
from solution import Solution
from formatter_0 import Formatter
from read_parameters import ReadParameters
from ga import GeneticAlgorithm
from fitness import AmericanStockFitness


# TODO, pending for this feature, it has to include buy, sell switch, too complicated
# should be imported into

# chromosome_type = '1_day', '3_day', '7_day'
def get_single_chromo_cls_result(chromosome_bits, chromosome_type, parameter_path, data_path,
                                 trading = False, return_data_dict = False):
    # (1.) read the parameters
    logger2.info("Genetic Algorithm Starting......")
    reader1 = ReadParameters()
    parameter_dict = reader1.read_parameters(parameter_path)

    
    # (2.) put data into dict
    formatter1 = Formatter(parameter_dict)
    testing_data_dict = formatter1.format_and_create_dict(data_path, formatter1.feature_choice_list)
    logger2.info("Create Testing_data_dict Successful")

    # (3.) get the chromosome bits and return the classification result
    s = Solution()
    s.chromosome_bits = chromosome_bits

    # (4.) compute fitness
    ga = GeneticAlgorithm(parameter_dict, testing_data_dict)
    # -(a) translate
    s.translate_chromosome_bits(ga.feature_pos_dict)
    # -(c) get the classfiled result in each day
    classification_result = s.get_classification_result(ga)
    if not classification_result:
        logger2.info("No forex returned of any date for {}".format(chromosome_type))
        logger2.info("chromosome_bits: {}".format(chromosome_bits))
        return None
    # print ("testing_data_dict: ", testing_data_dict)
    # print("parameter_dict: ", parameter_dict)
    # print ("chromosome_bits: ", chromosome_bits)
    #print ("classification_result:", classification_result)
    classification_result_1_day = sorted(classification_result, key = lambda x:x[0], reverse = True)[0]


    # (5.) judge buy or sell
    is_buy_bit = chromosome_bits[0]
    if is_buy_bit == 1:
        is_buy = True
        buy_or_sell = 'buy'
    elif is_buy_bit == 0:
        is_buy = False
        buy_or_sell = 'sell'
    else:
        print ("ERROR!!! check your chromosome_bits_list: ", chromosome_bits)

    # # (6.) write the data to file
    # if trading == False:
    #     with open(output_path, 'a', encoding = 'utf-8') as f:
    #         f.write("[buy_or_sell]{}[END]-[chromosome_type]{}[END]-[cls_result]{}[END]\n"
    #                 .format(buy_or_sell, chromosome_type, classification_result))
    # elif trading == True:
    #     with open(output_path, 'a', encoding = 'utf-8') as f:
    #         f.write("[buy_or_sell]{}[END]-[chromosome_type]{}[END]-[cls_result]{}[END]\n"
    #                 .format(buy_or_sell, chromosome_type, classification_result_1_day))

    # return
    if trading:
        return classification_result
    elif not trading and return_data_dict:
        return classification_result, testing_data_dict
    elif not trading:
        return classification_result
