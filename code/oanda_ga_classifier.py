# import from pjslib
from pjslib.general import get_upper_folder_path
from pjslib.general import accepts
from pjslib.logger import logger1,logger2
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


def oanda_ga_classifier():
    # TODO
    def get_chromosome_path_list(oanda_parameter_dict):
        chromosome_path_list = []
        return chromosome_path_list

    logger2.info("Genetic Algorithm Starting......")
    # (1.) read parameters
    reader1 = ReadParameters()
    parameter_dict = reader1.read_parameters(reader1.path)
    oanda_parameter_dict = reader1.read_oanda_parameters('')
    chromosome_path_list = get_chromosome_path_list(oanda_parameter_dict)
    # TODO, set the oanda parameter dict, need another for loop


    for chromosome_path in chromosome_path_list:
        #testing_parameter_dict = reader1.read_parameters('parameters/testing_parameter.json')

        logger2.info("Sell/Buy Switch :{}".format(parameter_dict['SGA']['buy_sell_switch']))
        logger2.info("read testing parameters successful")

        # (2.) put data into dict
        formatter1 = Formatter(parameter_dict)
        testing_data_dict = formatter1.format_and_create_dict(formatter1.path, formatter1.feature_choice_list, testing = True)
        logger2.info("Create Testing_data_dict Successful")
        print (testing_data_dict.keys())

        #(3.) read basic info
        sell_tuple = ('buy', 'sell')
        # 1d_[buy]_chromosome.txt
        time_frame =  re.findall(r'^(\w+)_', chromosome_path)[0]
        sell_or_buy = re.findall(r'_[(\w+)]', chromosome_path)[0]

        if sell_or_buy == 'sell':
            parameter_dict['SGA']['buy_sell_switch'] = 0
        elif sell_or_buy == 'buy':
            parameter_dict['SGA']['buy_sell_switch'] = 1


        with open(chromosome_path, 'r', encoding = 'utf-8') as f:
            for line in f:
                print(line)
                is_CHROMOSOME_end = re.findall("CHROMOSOME_END", line)
                if is_CHROMOSOME_end:
                    break
                chromosome = re.findall(r'[0-9,]+', line)[0]
                chromosome_bits = chromosome.split(',')
                # convert str to int
                buy_chromosome_bits = [int(x) for x in chromosome_bits]


                #(4.) create solution
                s = Solution()
                s.chromosome_bits = buy_chromosome_bits

                #(5.) compute fitness
                ga = GeneticAlgorithm(parameter_dict, testing_data_dict)
                # -(a) translate
                s.translate_chromosome_bits(ga.feature_pos_dict)
                # -(c) get the classfiled result in each day
                classification_result = s.get_classification_result(ga)
                if not classification_result:
                    print("No stocks returned for {} chromosome".format(string))
                    continue
                # -(d) compute fitness
                american_stock_fitness = AmericanStockFitness(parameter_dict)
                american_stock_fitness(testing_data_dict, s)
                testing_output_path = "test_data_result/{}_chromosome_testing.txt".format(string)


                print("--------------------------------------------------------------")
                print("name:{}, fitness:{}, profit:{}".format(s.name, s.fitness, s.profit))
                for result_tuple in s.classification_result_list:
                    print(str(result_tuple[0]) + ',' + str(result_tuple[1]))
                print("--------------------------------------------------------------")

        # return the result
        ga_classifier_result_dict = collections.defaultdict(lambda: {})
        ga_classifier_result_dict[time_frame][sell_or_buy] = s.classification_result_list
        return ga_classifier_result_dict
