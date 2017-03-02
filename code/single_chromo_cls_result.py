# import from pjslib
from pjslib.general import get_upper_folder_path
from pjslib.general import accepts
from pjslib.logger import logger2
#================================================
import os
import sys
import json
import re
import collections
import random
from solution import Solution
from formatter import Formatter
from read_parameters import ReadParameters
from ga import GeneticAlgorithm
from fitness import AmericanStockFitness

# chromosome_type = '1_day', '3_day', '7_day'
def get_single_chromo_cls_result(chromosome_bits, chromosome_type, parameter_path, data_path, output_path):
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
    classification_result_str = ','.join(classification_result)

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

    # (6.) write the data to file
    with open(output_path, 'a', encoding = 'utf-8') as f:
        f.write("[buy_or_sell]{}[END]-[chromosome_type]{}[END]-[cls_result]{}[END]\n"
                .format(buy_or_sell, chromosome_type, classification_result_str))

    # return
    return classification_result