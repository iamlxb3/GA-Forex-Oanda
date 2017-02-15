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

    def create_feature_pos_dict(self, parameter_dict):
        feature_pos_dict = collections.defaultdict(lambda: {})
        data_pos_in_chromosome_dict = parameter_dict['input']['data_pos_in_chromosome']
        id_feature_dict = parameter_dict['input']['raw_data_dict']
        data_pos_in_chromosome_sorted_list = sorted(list(data_pos_in_chromosome_dict.items()), key=lambda x: int(x[0]))
        print (data_pos_in_chromosome_sorted_list)
        pointer = 0
        for feature_id, feature_bit_config in data_pos_in_chromosome_sorted_list:
            feature_pos_list = []
            for bit_length in feature_bit_config:
                pos_tuple = (pointer, pointer + bit_length)
                feature_pos_list.append(pos_tuple)
                pointer += bit_length
                feature_pos_dict[feature_id]['pos'] = feature_pos_list
        for key, value_dict in feature_pos_dict.items():
            feature_pos_dict[key]['name'] = id_feature_dict[key]
        self.feature_pos_dict = feature_pos_dict
        return feature_pos_dict

    def create_empty_chromosome_bits(self, parameter_dict):
        empty_chromosome_bits = []
        data_pos_in_chromosome_dict = parameter_dict['input']['data_pos_in_chromosome']
        data_pos_in_chromosome_sorted_list = sorted(list(data_pos_in_chromosome_dict.items()), key = lambda x:x[0])
        for feature_id, feature_bit_config in data_pos_in_chromosome_sorted_list:
            switch_bit = feature_bit_config[0]
            operator_bits = feature_bit_config[1]
            sign_bit = feature_bit_config[2]
            int_value_bits = feature_bit_config[3]
            decimal_value_bits = feature_bit_config[4]

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
        chromosome_bits_length = len(empty_chromosome_bits)
        return empty_chromosome_bits, chromosome_bits_length