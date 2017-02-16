# import from pjslib
from pjslib.general import get_upper_folder_path
from pjslib.general import accepts
from pjslib.logger import logger1
#================================================
import os
import sys
import re
import collections
import random
from solution import Solution
from fitness import AmericanStockFitness

class GeneticAlgorithm():
    def __init__(self, parameter_dict, input_data_dict):

        def create_feature_pos_dict(parameter_dict):
            feature_pos_dict = collections.defaultdict(lambda: {})
            data_pos_in_chromosome_dict = parameter_dict['input']['data_pos_in_chromosome']
            id_feature_dict = parameter_dict['input']['raw_data_dict']
            data_pos_in_chromosome_sorted_list = sorted(list(data_pos_in_chromosome_dict.items()),
                                                        key=lambda x: int(x[0]))
            print(data_pos_in_chromosome_sorted_list)
            # set pointer = 1 because of the buy/sell
            pointer = 1
            for feature_id, feature_bit_config in data_pos_in_chromosome_sorted_list:
                feature_pos_list = []
                for bit_length in feature_bit_config:
                    pos_tuple = (pointer, pointer + bit_length)
                    feature_pos_list.append(pos_tuple)
                    pointer += bit_length
                    feature_pos_dict[feature_id]['pos'] = feature_pos_list
            for key, value_dict in feature_pos_dict.items():
                feature_pos_dict[key]['name'] = id_feature_dict[key]
            logger1.info("feature_pos_dict: {}".format(feature_pos_dict))
            return feature_pos_dict




        # --------------:::__init__:::----------------------

        self.result_dict = collections.defaultdict(lambda :0)
        self.tabu_list = []
        self.current_solutions_list = []
        self.seed_list = []
        self.input_data_dict = input_data_dict
        self.parameter_dict = parameter_dict
        self.feature_pos_dict = create_feature_pos_dict(parameter_dict)
        self.highest_value = 0
        self.no_progress_generation = 0
        self.small_generation = 0
        self.big_generation = 0
        self.END = False

    def write_result_to_file(self):
        pass

    def monitor_progress(self, Solution):
        # TODO use highest_value
        no_progress_generation_threshold = self.parameter_dict['SGA']['no_progress_generation']
        if self.no_progress_generation > no_progress_generation_threshold:
            self.END = True


    def create_initial_parents(self):
        parameter_dict = self.parameter_dict
        empty_chromosome_bits, chromosome_bits_length = self.create_empty_chromosome_bits(parameter_dict)
        feature_pos_dict = self.feature_pos_dict
        intial_solution_number = parameter_dict['SGA']['intial_solution_number']
        for i in range(intial_solution_number):
            # (a) create solution with random chromosome
            random_chromosome = [random.randint(0, 1) for p in range(chromosome_bits_length)]
            s = Solution()
            s.chromosome_bits = random_chromosome
            # (b) translate chromosome bits list to decimal value
            s.translate_chromosome_bits(feature_pos_dict)
            # (c) get the classfiled result in each day
            s.get_classification_result(self.parameter_dict, self.input_data_dict)
            # (d) filter the solution with limited target returns
            input_data_num = len(self.input_data_dict.keys())
            is_s_not_removed = s.filter_solution(self.parameter_dict, input_data_num)
            # (e) compute the fitness for solution
            if is_s_not_removed:
                american_stock_fitness = AmericanStockFitness(parameter_dict)
                american_stock_fitness(self.input_data_dict, s)

    def process_new_solutions(self,new_generation_list):
        """Translate chromosome_bits, find targets, compute fitness"""
        for s in new_generation_list:
            # (b) translate chromosome bits list to decimal value
            s.translate_chromosome_bits(self.feature_pos_dict)
            # (c) get the classfiled result in each day
            s.get_classification_result(self.parameter_dict, self.input_data_dict)
            # (d) filter the solution with limited target returns
            input_data_num = len(self.input_data_dict.keys())
            is_s_not_removed = s.filter_solution(self.parameter_dict, input_data_num)
            # (e) compute the fitness for solution
            if is_s_not_removed:
                american_stock_fitness = AmericanStockFitness(self.parameter_dict)
                american_stock_fitness(self.input_data_dict, s)

    def create_empty_chromosome_bits(self, parameter_dict):
        empty_chromosome_bits = []
        data_pos_in_chromosome_dict = parameter_dict['input']['data_pos_in_chromosome']
        data_pos_in_chromosome_sorted_list = sorted(list(data_pos_in_chromosome_dict.items()), key = lambda x:x[0])
        # append the buy/sell bit
        empty_chromosome_bits.append(0)
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


class SeedRadius:
    def __init__(self, parameter_dict):
        self.initial_IS = float(parameter_dict['DSGA']['IS'])
        # radius delta
        self.initial_SD = float(parameter_dict['DSGA']['SD'])
        self._IS = self.initial_IS
        self._SD = self.initial_SD

    @property
    def IS(self):
        return self._IS

    def add(self):
        self._IS += self._SD
        logger1.debug("#SeedRadius#")
        logger1.debug("Add SD, SD:{}, IS:{}".format(self._SD, self._IS))
        logger1.debug("#SeedRadius END#")

    def __str__(self):
        return ("IS:{}, SD:{}".format(self._IS,self._SD))