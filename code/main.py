# import from pjslib
from pjslib.general import get_upper_folder_path
from pjslib.general import accepts
from pjslib.logger import logger1
#================================================

# import local .py files
from read_parameters import ReadParameters
from formatter import Formatter
from ga import GeneticAlgorithm
from fitness import AmericanStockFitness
from solution import Solution
from evolution import OffspringGeneration, CrossOver, Mutation

#================================================
import random




# (1.) read parameters
reader1 = ReadParameters()
parameter_dict = reader1.read_parameters(reader1.path)
logger1.info("read parameters successful")


# (2.) put data into dict
formatter1 = Formatter(parameter_dict)
input_data_dict = formatter1.format_and_create_dict(formatter1.path, formatter1.feature_choice_list)
logger1.info("create input_data_dict successful")



































# ==================================SIMPLE UNIT TEST=================================================
# ===================================================================================================
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
# # multi_point
# cross_over_multi_point = CrossOver(parameter_dict)
# cross_over_multi_point.mode = 'multi_point'
# c1,c2 = cross_over_multi_point(p1,p2)
# print ("c1:{}c2:{}".format(c1,c2))
# # one_point
# cross_over_one_point = CrossOver(parameter_dict)
# cross_over_one_point.mode = 'one_point'
# c1,c2 = cross_over_one_point(p1,p2)
# print ("c1:{}c2:{}".format(c1,c2))
# # uniform
# cross_over_uniform = CrossOver(parameter_dict)
# cross_over_uniform.mode = 'uniform'
# c1,c2 = cross_over_uniform(p1,p2)
# print ("c1:{}c2:{}".format(c1,c2))
# #---------------------------------------------------------------------------------------------------
# #::: cross_over simple test pass; DATA:2017-2-12
# #====================================================================================================


# #====================================================================================================
# #::: solution :::
# #----------------------------------TEST CODE--------------------------------------------------------
# chromosome_bit_list = ['0','0','1','1','0','1','1','0']
#
# for i in range(5):
#     s = Solution()
#     s.chromosome_bits = random.sample(chromosome_bit_list, 5)
#
# print (Solution.all()[0].chromosome_bits)
# Solution._clear()
# print (Solution.all())
# #---------------------------------------------------------------------------------------------------
# # #:::solution test ; DATA:2017-2-13
# #====================================================================================================





# #====================================================================================================
# #::: offspring generation :::
# #----------------------------------TEST CODE--------------------------------------------------------
# chromosome_bit_list = [0,0,1,1,0,1,1,0]
#
# #----------------------------------------------------------
# # test for tournament_selection
# for i in range(5):
#     s = Solution()
#     s.chromosome_bits = random.sample(chromosome_bit_list, 5)
#     s.fitness = random.random()
#
# parent_list = Solution.all()
# parameter_dict['SGA']['TS']['TS_K'] = 3
# parameter_dict['SGA']['parent_select_mode'] = 'TS'
# off_spring_generation = OffspringGeneration(parameter_dict)
# off_spring_generation(parent_list)
# #----------------------------------------------------------
# # Clear
# Solution._clear()
# #----------------------------------------------------------
# # test for roulette_wheel_selection
# for i in range(5):
#     s = Solution()
#     s.chromosome_bits = random.sample(chromosome_bit_list, 5)
#     s.fitness = random.random()
#
# Solution.all()[0].fitness = 0.9
# Solution.all()[1].fitness = 0.1
# parent_list = Solution.all()
# parameter_dict['SGA']['parent_select_mode'] = 'RWS'
# off_spring_generation = OffspringGeneration(parameter_dict)
# off_spring_generation(parent_list)
# #----------------------------------------------------------
# #---------------------------------------------------------------------------------------------------
# #:::solution test ; DATA:2017-2-13
# #====================================================================================================


# #====================================================================================================
# #::: create_empty_chromosome_bits generation :::
# #----------------------------------TEST CODE--------------------------------------------------------
#
# ga = GeneticAlgorithm()
# empty_chromosome_bits = ga.create_empty_chromosome_bits(parameter_dict)
# feature_pos_dict = ga.create_feature_pos_dict(parameter_dict)
# print (feature_pos_dict)
# print (empty_chromosome_bits)
# print (len(empty_chromosome_bits))
# #---------------------------------------------------------------------------------------------------
# #:::create_empty_chromosome_bits test ; DATA:2017-2-14
# #====================================================================================================


#====================================================================================================
#::: select stocks :::
#----------------------------------TEST CODE--------------------------------------------------------

ga = GeneticAlgorithm()
empty_chromosome_bits, chromosome_bits_length = ga.create_empty_chromosome_bits(parameter_dict)
feature_pos_dict = ga.create_feature_pos_dict(parameter_dict)
print (feature_pos_dict)
random_chromosome = [random.randint(0,1) for p in range(chromosome_bits_length)]
# create solution with random chromosome
s = Solution(parameter_dict)
s.chromosome_bits = [1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1]
print(s.chromosome_bits)

s.get_classification_result(feature_pos_dict, input_data_dict)

#---------------------------------------------------------------------------------------------------
#:::create_empty_chromosome_bits test ; DATA:2017-2-14
#====================================================================================================







































#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# ===================================================================================================
# =================================SIMPLE UNIT TEST END==============================================