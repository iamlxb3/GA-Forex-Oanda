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
from formatter_0 import Formatter
from read_parameters import ReadParameters
from ga import GeneticAlgorithm
from fitness import AmericanStockFitness


logger2.info("Genetic Algorithm Starting......")
# (1.) read parameters
reader1 = ReadParameters()
parameter_dict = reader1.read_parameters(reader1.path)
#testing_parameter_dict = reader1.read_parameters('parameters/testing_parameter.json')

logger2.info("Sell/Buy Switch :{}".format(parameter_dict['SGA']['buy_sell_switch']))
logger2.info("read testing parameters successful")

# (2.) put data into dict
formatter1 = Formatter(parameter_dict)
testing_data_dict = formatter1.format_and_create_dict(formatter1.path, formatter1.feature_choice_list, testing = True)
logger2.info("Create Testing_data_dict Successful")
print (testing_data_dict.keys())

#(3.) read chromosome
sell_tuple = ('buy', 'sell')
for string in sell_tuple:
    if string == 'sell':
        parameter_dict['SGA']['buy_sell_switch'] = 0
    elif string == 'buy':
        parameter_dict['SGA']['buy_sell_switch'] = 1

    chromosome_path = "chromosome/{}_chromosome.txt".format(string)
    with open(chromosome_path, 'r', encoding = 'utf-8') as f:
        for line in f:
            print(line)
            is_CHROMOSOME_end = re.findall("CHROMOSOME_END", line)
            if is_CHROMOSOME_end:
                break
            try:
                chromosome = re.findall(r'[0-9,]+', line)[0]
            except IndexError:
                logger2.error("Check your {} chromosome!!".format(string))
                sys.exit(0)
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
            print ("testing_output_path: ", testing_output_path)


    Solution.compute_profit()
    sorted_solution_list = sorted(Solution._all, key = lambda x:x.profit, reverse = True)

    # remove file
    is_testing_output_path = os.path.exists(testing_output_path)
    if is_testing_output_path and sorted_solution_list:
        os.remove(testing_output_path)
    
    for s in sorted_solution_list:
        print("--------------------------------------------------------------")
        print("name:{}, fitness:{}, profit:{}".format(s.name, s.fitness, s.profit))
        for result_tuple in s.classification_result_list:
            print(str(result_tuple[0]) + ',' + str(result_tuple[1]))
        print("--------------------------------------------------------------")

        # get chromeosome
        chromosome_list = [str(x) for x in s.chromosome_bits]
        chromosome = ''.join(chromosome_list)

        with open(testing_output_path, 'a', encoding = 'utf-8') as f:
            print  ("testing_output_path :", testing_output_path)
            #sys.exit(0)
            f.write("\n==========================================================================================\n")
            f.write("name: {}\n".format(s.name))
            f.write(chromosome + '\n')
            f.write('profit: {}\n'.format(s.profit))
            f.write('fitness: {}\n'.format(s.fitness))
            f.write('stock return..\n')
            f.write('-------------------------------------------------\n')
            for result_tuple in sorted(s.classification_result_list, key = lambda x:x[0]):
                f.write(str(result_tuple[0]) + ',' + str(result_tuple[1]) + '\n')
            f.write('-------------------------------------------------\n')
            f.write('feature_dict\n')
            json.dump(s.feature_dict,f, indent= 4)
            f.write("\n==========================================================================================\n")


    # clear the solution for buy or sell
    Solution._clear()

