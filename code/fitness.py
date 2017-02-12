# import from pjslib
from pjslib.general import get_upper_folder_path
from pjslib.general import accepts
from pjslib.logger import logger1
#================================================
import os
import sys
import re
import collections
from ga import GeneticAlgorithm



class AmericanStockFitness():
    def __init__(self, parameter_dict):
        self._next_price_str = parameter_dict['input']['next_price_str']
        pass

    # population_dict：{‘asd':((datetime_object1,EUR), (datetime_object2,USD), (datetime_object3,JPY),...)}
    def __call__(self, input_data_dict, population_dict, result_dict):
        # predicted_stock_sequence is sorted by time, from past to future
        population_name = population_dict['name']
        predicted_stock_sequence_tuple = population_dict['date_stock_tuple']
        chosen_days_num = len(predicted_stock_sequence_tuple)
        input_days_num = len(list(input_data_dict.keys()))
        # test if the input and the compared num of stocks are equal
        if chosen_days_num != input_days_num:
            logger1.error("stocks number doesn't match for the input and the chosen one!")
            sys.exit(0)
        else:
            average_sum = 0
            for date,stock in predicted_stock_sequence_tuple:
                features_tuple = input_data_dict[date][stock]
                features_dict = dict(features_tuple._asdict())
                average_sum += float(features_dict[self._next_price_str])
                print('profit_percent: ', float(features_dict[self._next_price_str]))
            average = average_sum/input_days_num

            logger1.info("result: {},{}".format(population_name, average))
            # return tuple
            result_dict[population_name] = average
            return (population_name, average)
















