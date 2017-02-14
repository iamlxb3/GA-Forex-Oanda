# import from pjslib
from pjslib.general import get_upper_folder_path
from pjslib.general import accepts
from pjslib.logger import logger1
#================================================
import os
import sys
import re
import collections

class GeneticAlgorithm():
    def __init__(self):
        self.result_dict = collections.defaultdict(lambda :0)
        self.tabu_list = []
        self.current_solutions_list = []
        self.seed_list = []

    def create_empty_chromosome_bits(self, parameter_dict):
        empty_chromosome_bits = []
        data_pos_in_chromosome_dict = parameter_dict['input']['data_pos_in_chromosome']
        data_pos_in_chromosome_sorted_list = sorted(list(data_pos_in_chromosome_dict.items()), key = lambda x:x[0])
        for feature_id, feature_bit_config in data_pos_in_chromosome_sorted_list:
            switch_bit = feature_bit_config[0]
            operator_bits = feature_bit_config[1]
            value_bits_list = feature_bit_config[2]
            sign_bit = value_bits_list[0]
            int_value_bits = value_bits_list[1]
            decimal_value_bits = value_bits_list[2]

            if switch_bit:
                empty_chromosome_bits.append(0)
            if operator_bits:
                empty_chromosome_bits.extend([0 for x in range(operator_bits)])
            if sign_bit:
                empty_chromosome_bits.append(0)
            if int_value_bits:
                empty_chromosome_bits.extend([0 for x in range(int_value_bits)])
            if decimal_value_bits:
                empty_chromosome_bits.extend([0 for x in range(decimal_value_bits)])
        self.empty_chromosome_bits = empty_chromosome_bits
        return empty_chromosome_bits