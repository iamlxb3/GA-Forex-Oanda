# import from pjslib
from pjslib.general import get_upper_folder_path
from pjslib.general import accepts
from pjslib.logger import logger1
#================================================


from read_parameters import ReadParameters
from formatter import Formatter
from ga import GeneticAlgorithm
from fitness import AmericanStockFitness

# (1.) read parameters
reader1 = ReadParameters()
parameter_dict = reader1.read_parameters(reader1.path)
logger1.info("read parameters successful")
# (2.) put data into dict
formatter1 = Formatter(parameter_dict)
input_data_dict = formatter1.format_and_create_dict(formatter1.path, formatter1.feature_choice_list)
logger1.info("create input_data_dict successful")


















# ==================================SIMPLE UNIT TEST=================================================
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

# #:::test for fitness function:::
# #==================================================================================================
# # debug: create population_dict
# date_list = input_data_dict.keys()
# stock_list = ['BA' for x in range(len(date_list))]
# sorted_date_stock_list = sorted(list(zip(date_list, stock_list)), key = lambda x:x[0])
# date_stock_tuple = tuple(sorted_date_stock_list)
#
# individual_population_dict = {'name':'sss', 'date_stock_tuple': date_stock_tuple}
#
# # compute result for one population
# genetic_algorithm = GeneticAlgorithm()
# american_stock_fitness = AmericanStockFitness(parameter_dict)
# # augument : (input_data_dict, population_dict, result_dict)
# training_dict = input_data_dict
# tuple1 = american_stock_fitness(training_dict, individual_population_dict, genetic_algorithm.result_dict)
# #==================================================================================================




# #====================================================================================================
# #::: mutation :::
# #----------------------------------TEST CODE--------------------------------------------------------
# from evolution import Mutation
# mutation = Mutation(parameter_dict)
# chromosome_bits = [1,0,0,0,1,0]
# new_chromosome_bits = mutation(chromosome_bits)
# print ("chromosome_bits: ", chromosome_bits)
# #---------------------------------------------------------------------------------------------------
# #::: mutation test result: all pass; DATA:2017-2-12
# #====================================================================================================



# #====================================================================================================
# #::: cross over :::
# #----------------------------------TEST CODE--------------------------------------------------------
# from evolution import CrossOver
# p1 = [0,0,0,0,0]
# p2 = [1,1,1,1,1]
# cross_over = CrossOver(parameter_dict)
# c1,c2 = cross_over(p1,p2)
# print ("c1:{}c2:{}".format(c1,c2))
# #---------------------------------------------------------------------------------------------------
# #::: cross_over simple test pass; DATA:2017-2-12
# #====================================================================================================



#==================================================================================================
# :::test for parent selection:::
#==================================================================================================



#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# =================================SIMPLE UNIT TEST END==============================================