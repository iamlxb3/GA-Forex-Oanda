# import from pjslib=====================================
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

import sys
import os

parent_folder = get_upper_folder_path(1)
sys.path.append(os.path.join(parent_folder, 'pjslib'))
sys.path.append(os.path.join(parent_folder))

from general import get_upper_folder_path
from general import accepts
from logger import logger1
#================================================
import os
import sys
import re
import collections
import pprint



class AmericanStockFitness():
    def __init__(self, parameter_dict):
        self._next_price_str = parameter_dict['input']['next_price_str']
        self.buy_sell_switch = parameter_dict['SGA']['buy_sell_switch']

    # population_dict：{‘asd':((datetime_object1,EUR), (datetime_object2,USD), (datetime_object3,JPY),...)}
    def __call__(self, input_data_dict, solution):
        if solution.is_f_computed:
            return
        # predicted_stock_sequence is sorted by time, from past to future
        population_name = solution.name
        predicted_stock_sequence_tuple = solution.classification_result_list

        is_buy = self.buy_sell_switch
        predicted_days_num = len(predicted_stock_sequence_tuple)
        average_sum = 0
        for date,stock in predicted_stock_sequence_tuple:
            features_tuple = input_data_dict[date][stock]
            features_dict = dict(features_tuple._asdict())
            #print ("features_dict: ", features_dict)
            if is_buy == 1:
                value = float(features_dict[self._next_price_str])
            elif is_buy == 0:
                value = (-1) * float(features_dict[self._next_price_str])
            average_sum += value

            # update return_value_by_time_list
            solution.return_value_by_time_dict[date].append(value)

            #print('profit_percent: ', float(features_dict[self._next_price_str]))

        average = average_sum/predicted_days_num
        #print('average: ', float(average))
        solution.fitness = float("{:.3f}".format(average))
        solution.is_f_computed = True
        logger1.debug("----------SOLUTION_INFO-----------------------")
        logger1.debug("solution_name: {}, result:{}"
                     .format(population_name, average, pprint.pformat(solution.classification_result_list)))
        logger1.debug("chromosome_length: {}"
                     .format(pprint.pformat(len(''.join([str(x) for x in solution.chromosome_bits])))))
        logger1.debug("chromosome: {}"
                     .format(pprint.pformat(''.join([str(x) for x in solution.chromosome_bits]))))
        logger1.debug("decisive feature:{}\n"
                     .format(solution.decisive_feature))
        logger1.debug("classification_result:\n{}"
                     .format(pprint.pformat(solution.classification_result_list)))
        logger1.debug("feature_dict: {}"
                     .format(pprint.pformat(solution.feature_dict)))
        logger1.debug("----------SOLUTION_INFO END-------------------")
        logger1.debug("\n\n")
        # return tuple
        return (population_name, average)
















