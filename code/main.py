# import from pjslib
from pjslib.general import get_upper_folder_path
from pjslib.general import accepts
from pjslib.logger import logger1
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
import random
import pprint

# #======TEMP
# # (2) translate chromosome bits list to decimal value
# s.translate_chromosome_bits(feature_pos_dict)
# # (3) get the classfiled result in each day
# s.get_classification_result(input_data_dict)
# # (4) filter the solution with limited target returns
# input_data_num = len(input_data_dict.keys())
# is_s_not_removed = s.filter_solution(input_data_num)
# # (5) compute the fitness for solution
# if is_s_not_removed:
#     american_stock_fitness = AmericanStockFitness(parameter_dict)
#     american_stock_fitness(input_data_dict, s)
# top_solutions_list = sorted([(solution.name, solution.fitness) for solution in Solution._all], key = lambda x:x[1], reverse = True)[0:10]
# print (top_solutions_list)
# print ("Found solution num:{}".format(len(Solution._all)))
# #TEMP END

logger1.info("Genetic Algorithm Starting......")
# (1.) read parameters
reader1 = ReadParameters()
parameter_dict = reader1.read_parameters(reader1.path)
logger1.info("Sell/Buy Switch :{}".format(parameter_dict['SGA']['buy_sell_switch']))
logger1.info("read parameters successful")
# seed radius
IS = parameter_dict['DSGA']['IS']
# radius delta
SD = parameter_dict['DSGA']['SD']
seed_radius = SeedRadius(parameter_dict)


# (2.) put data into dict
formatter1 = Formatter(parameter_dict)
input_data_dict = formatter1.format_and_create_dict(formatter1.path, formatter1.feature_choice_list)
logger1.info("create input_data_dict successful")

# (3.) create initial parents
ga = GeneticAlgorithm(parameter_dict, input_data_dict)
ga.seed_radius = seed_radius
ga.create_initial_parents()
off_spring_generation = OffspringGeneration(parameter_dict)


while not ga.END:
    RLC = parameter_dict['DSGA']['RLC']
    for i in range(5):
        # (4.) offspring generation , return target, compute fitness
        current_solution_pool = off_spring_generation(Solution.all())
        ga.process_new_solutions(current_solution_pool)
        # (5.) compute shared fitness
        Solution.compute_shared_fitness(ga)
        # (6.) find seed solution
        Solution.find_seed_solution(ga)
        # (7.) filter_solution_pool and ready for new parents
        Solution.filter_solution_pool(ga)
        ga.small_generation += 1
        ga.logging(Solution,'s')
    Solution.replace_converged_seeds()
    ga.monitor_progress(Solution)
    ga.seed_radius.add()
    ga.big_generation += 1
    ga.logging(Solution, 'b')
    # TEST
    ga.END = True

# END
ga.write_result_to_file()

#================TEMP PRINT===============
top_solutions_list = sorted([(solution.name, solution.fitness) for solution in Solution._all], key = lambda x:x[1], reverse = True)[0:10]
print (top_solutions_list)
print ("Found solution num:{}".format(len(Solution._all)))


# (5.) continue running unless no better solution is found in n iterations
# (6.) loop n iterations



































# # ==================================SIMPLE UNIT TEST=================================================
# # ===================================================================================================
# # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#
# #:::test for fitness function:::  out-dated test
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


# #====================================================================================================
# #::: select stocks test:::
# #----------------------------------TEST CODE--------------------------------------------------------
#
# ga = GeneticAlgorithm()
# empty_chromosome_bits, chromosome_bits_length = ga.create_empty_chromosome_bits(parameter_dict)
# feature_pos_dict = ga.create_feature_pos_dict(parameter_dict)
# print (feature_pos_dict)
# solution_num = 100
# for i in range(solution_num):
#     # (1) create solution with random chromosome
#     random_chromosome = [random.randint(0,1) for p in range(chromosome_bits_length)]
#     s = Solution(parameter_dict)
#     s.chromosome_bits = random_chromosome
#     #s.chromosome_bits = [1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1]
#     # (2) translate chromosome bits list to decimal value
#     s.translate_chromosome_bits(feature_pos_dict)
#     # (3) get the classfiled result in each day
#     s.get_classification_result(input_data_dict)
#     # (4) filter the solution with limited target returns
#     input_data_num = len(input_data_dict.keys())
#     is_s_not_removed = s.filter_solution(input_data_num)
#     # (5) compute the fitness for solution
#     if is_s_not_removed:
#         american_stock_fitness = AmericanStockFitness(parameter_dict)
#         american_stock_fitness(input_data_dict, s)
#
# top_solutions_list = sorted([(solution.name, solution.fitness) for solution in Solution._all], key = lambda x:x[1], reverse = True)[0:10]
# print (top_solutions_list)
# print ("Found solution num:{}".format(len(Solution._all)))
# #---------------------------------------------------------------------------------------------------
# #:::create_empty_chromosome_bits test ; DATA:2017-2-14
# #====================================================================================================







































#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# ===================================================================================================
# =================================SIMPLE UNIT TEST END==============================================