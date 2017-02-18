# import from pjslib
from pjslib.general import get_upper_folder_path
from pjslib.general import accepts
from pjslib.logger import logger1, logger3
#================================================

# import local .py files
from read_parameters import ReadParameters
from formatter import Formatter
from ga import GeneticAlgorithm
from ga import SeedRadius
from fitness import AmericanStockFitness
from solution import Solution
from evolution import OffspringGeneration, CrossOver, Mutation

#================================================
import unittest
import collections
import os
import time
import datetime
import pprint


#------------------------STANDARD TESING MODULE
class TestGaReturnedResults(unittest.TestCase):


    def fitness(self, testing, golden):
        self.assertEqual(testing, golden)
        self.assertEqual(1, 1)


    def return_results(self, testing, golden):
        self.assertEqual(testing, golden)

# ------------------------STANDARD TESING MODULE END






#-----------------------------------------------------
#FUNCTIONS

def convert_date_str_to_date_object(date_str):
    date = time.strptime(date_str, '%Y-%m-%d')
    date = datetime.datetime(*date[:3])
    date = datetime.date(year=date.year, month=date.month, day=date.day)
    return date






#------------------------------------------------------
# BUILD GA_UNITEST_DICT
ga_unittest_dict = collections.defaultdict(lambda :{})
# add 1-----------------------------------------------------------------------------------------------------------------
ga_unittest_dict['1']['catagory'] = 'USA_stock'
ga_unittest_dict['1']['chromosome_str'] = '1111010010001110100010000011001001111001001011010'
ga_unittest_dict['1']['temp_golden_result'] = [
    ('2011-2-4','DIS'),
    ('2011-2-11','DIS'),

]
ga_unittest_dict['1']['golden_fitness'] = float(3.627)
ga_unittest_dict['1']['para_file_name'] = 'parameter.json'
ga_unittest_dict['1']['data_file_name'] = 'cleaned_data.txt'
# ======================================================================================================================
# Returned stocks are all within the range of the chromosome value, have not yet check the other stocks may also be
# returned by this chromosome. 2017/2/17 (Manually Check)
# ======================================================================================================================
# end 1-----------------------------------------------------------------------------------------------------------------

#------------------------------------------------------
# BUILD GA_UNITEST_DICT
# add 2-----------------------------------------------------------------------------------------------------------------
ga_unittest_dict['2']['catagory'] = 'USA_stock'
ga_unittest_dict['2']['chromosome_str'] = '1101100011101110100001110001001011100111000110010'
ga_unittest_dict['2']['temp_golden_result'] = [
    ('2011-01-14', 'AXP'),
    ('2011-01-21', 'GE'),
    ('2011-01-28', 'CAT'),
    ('2011-02-04', 'DIS'),
    ('2011-02-11', 'DIS'),
    ('2011-02-18', 'CVX'),
    ('2011-02-25', 'CVX'),
    ('2011-03-04', 'MCD'),
    ('2011-03-18', 'CVX'),
    ('2011-03-25', 'DIS'),

]
ga_unittest_dict['2']['golden_fitness'] = float(1.895)
ga_unittest_dict['2']['para_file_name'] = 'parameter.json'
ga_unittest_dict['2']['data_file_name'] = 'cleaned_data.txt'
# ======================================================================================================================
# Returned stocks are all within the range of the chromosome value, have not yet check the other stocks may also be
# returned by this chromosome. 2017/2/17 (Manually Check)
# ======================================================================================================================
# end 2-----------------------------------------------------------------------------------------------------------------













#====================format ga_unittest_dict=======================
for key, ga_unittest_dict in ga_unittest_dict.items():
    para_file_path = os.path.join('testing', ga_unittest_dict['catagory'],
                                  str(key), 'parameter', ga_unittest_dict['para_file_name'])
    data_file_path = os.path.join('testing', ga_unittest_dict['catagory'],
                              str(key), 'data', ga_unittest_dict['data_file_name'])
    temp_golden_result_list = ga_unittest_dict['temp_golden_result']

    # convert type in golden_result
    ga_unittest_dict['golden_result'] = []
    for date_target_pair in temp_golden_result_list:
        date_str = date_target_pair[0]
        date_obj = convert_date_str_to_date_object(date_str)
        new_date_target_pair = (date_obj, date_target_pair[1])
        ga_unittest_dict['golden_result'].append(new_date_target_pair)

    # convert chromosome_str into list
    ga_unittest_dict['chromosome_bits'] = [int(x) for x in list(ga_unittest_dict['chromosome_str'])]

# ====================format ga_unittest_dict end=======================

    #-----------------------get targets returned and fitness
    #(1.) read para
    reader1 = ReadParameters()
    parameter_dict = reader1.read_parameters(para_file_path)

    # (2.) put data into dict
    formatter1 = Formatter(parameter_dict, path = data_file_path)
    input_data_dict = formatter1.format_and_create_dict(formatter1.path, formatter1.feature_choice_list)
    formatter1.compute_chosen_feature_value_range()

    # (3.) create initial parents
    ga = GeneticAlgorithm(parameter_dict, input_data_dict)

    #(4.) create solution
    s = Solution()
    s.chromosome_bits = ga_unittest_dict['chromosome_bits']
    # (a) translate chromosome bits list to decimal value
    s.translate_chromosome_bits(ga.feature_pos_dict)
    # (b) get the classfiled result in each day
    s.get_classification_result(ga)
    # (c) compute the fitness for solution
    american_stock_fitness = AmericanStockFitness(parameter_dict)
    american_stock_fitness(ga.input_data_dict, s)

    # TESING CODE
    golden_return = ga_unittest_dict['golden_result']
    golden_fitness = ga_unittest_dict['golden_fitness']
    testing_return = sorted(s.classification_result_list, key = lambda x:x[0])
    testing_fitness = float(s.fitness)
    #test11 = TestGaReturnedResults()
    TestGaReturnedResults().fitness(testing_fitness, golden_fitness)
    TestGaReturnedResults().return_results(testing_return, golden_return)
    print("----------------------------")
    print ("id {} test ok...".format(key))
    logger3.info("id {} test ok...".format(key))
    logger3.info("solution chromosome: {}".format(ga_unittest_dict['chromosome_str']))
    # TODO PPrint this, need the id of the feature, operator shoule be like >=
    logger3.info("solution feature dict: \n{}\n".format(pprint.pformat(dict(s.feature_dict))))
    logger3.info("solution decisive feature: {}".format(pprint.pformat(s.decisive_feature)))
    logger3.info("solution fitness: {}".format(pprint.pformat(s.fitness)))
    logger3.info("solution returned_result: {}".format(pprint.pformat(testing_return)))
    logger3.info("Training End Date: {}".format(pprint.pformat(parameter_dict['input']['training_date_end'])))
    logger3.info("===============================================================")

#====================format ga_unittest_dict end=======================


if __name__ == '__main__':
    unittest.main()







