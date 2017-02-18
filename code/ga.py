# import from pjslib
from pjslib.general import get_upper_folder_path
from pjslib.general import accepts
from pjslib.logger import logger1
#================================================
import os
import sys
import re
import json
import collections
import random
from solution import Solution
import matplotlib.pyplot as plt
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
            logger1.info("feature_pos_dict: {}".format(feature_pos_dict))
            return feature_pos_dict




        # --------------:::__init__:::----------------------
        self.parameter_dict = parameter_dict
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
        self.generation_dict = collections.defaultdict(lambda :{})
        self.END = False
        # the number of date or hour or week
        self.input_data_num = len(self.input_data_dict.keys())

    def save_info_to_file(self, Solution):
        current_path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current_path,'result', 'ga_info.txt')
        with open(path,'w', encoding = 'utf-8') as f:
            json.dump(self.generation_dict, f, indent = 4)

        # save the chromosome with highest fitness
        highest_solution = sorted(Solution._all, key = lambda x:x.fitness, reverse = True)[0]
        fitness = highest_solution.fitness
        print ("highest fitness:{}".format(fitness))
        chromosome = [str(x) for x in highest_solution.chromosome_bits]
        chromosome_str = ','.join(chromosome)
        buy_sell_switch = self.parameter_dict['SGA']['buy_sell_switch']
        buy_sell_dict = {1:'buy', 0:'sell'}
        buy_sell_str = buy_sell_dict[buy_sell_switch]
        with open('chromosome/{}_chromosome.txt'.format(buy_sell_str), 'w', encoding = 'utf-8') as f:
            f.write(chromosome_str)
            f.write('\nfitness:{}'.format(fitness))

    #TODO
    def plot_generation_trend(self):
        #self.generation_dict
        # self.generation_dict['s_g_trend'][self.small_generation]
        seed_list = [] # highest seed fitness
        s_list = [] # highest solution fitness
        fitness_list = []
        seed_fitness_list = []
        shared_fitness_list = []
        # self.generation_dict['s_fitness_g_trend']:
        # s_g: small generation
        # (sorted_solution_list[0].name, sorted_solution_list[0].fitness, sorted_solution_list[0].shared_fitness)
        for s_g, top_solution_tuple in self.generation_dict['s_fitness_g_trend'].items():
            s_list.append(s_g)
            fitness_list.append(top_solution_tuple[1])
            shared_fitness_list.append(top_solution_tuple[2])

        for s_g, top_seed_tuple in self.generation_dict['s_g_trend'].items():
            seed_list.append(s_g)
            seed_fitness_list.append(top_seed_tuple[1])
        # display and save file
        plt.plot(seed_list, seed_fitness_list, 'rx', label="h_seed_fitness")
        plt.plot(s_list, fitness_list, 'bx', label="solution_fitness")
        plt.plot(s_list, shared_fitness_list, 'gx', label="solution_shared_fitness")
        plt.legend(loc=2)
        path = os.path.join("result", 'fitness.png')
        plt.savefig(path)
        plt.show()


    def logging(self, Solution, generation = 's'):
        if generation == 's':
            top_5_solution = sorted(Solution._all, key = lambda x:x.fitness, reverse = True)[0:5]
            logger1.info("\n\n")
            logger1.info("###Small Generation Logging###")
            logger1.info("==============================")
            logger1.info("big generation: {}".format(self.big_generation))
            logger1.info("small generation: {}, {} solution survived."
                         .format(self.small_generation, len(Solution._all)))
            logger1.info("Species Found:{}"
                         .format(len(Solution.seed_list)))
            # logging seed
            logger1.info("SEED INFORMATION")
            sorted_seed_list = sorted(Solution.seed_list, key = lambda x:x.shared_fitness, reverse = True)
            #　save the highest fitness of seed
            self.generation_dict['s_g_trend'][self.small_generation] = \
                (sorted_seed_list[0].name, sorted_seed_list[0].fitness, sorted_seed_list[0].shared_fitness)
            # logging highest solution
            sorted_solution_list = sorted(Solution._all, key = lambda x:x.fitness, reverse = True)
            #　save the highest fitness of seed
            self.generation_dict['s_fitness_g_trend'][self.small_generation] = \
                (sorted_solution_list[0].name, sorted_solution_list[0].fitness, sorted_solution_list[0].shared_fitness)


            for i, seed in enumerate(sorted_seed_list):
                logger1.info("Rank:{}, Seed name:{}, fitness:{}, shared_fitness:{}"
                .format(i, seed.name, seed.fitness, seed.shared_fitness))
                logger1.info("Seed returned :{}"
                .format([stock_tuple for stock_tuple in sorted(seed.classification_result_list, key = lambda x:x[0])]))
            logger1.info("----top5 fitness found in this generation----")
            for i, solution in enumerate(top_5_solution):
                rank = i + 1
                logger1.info(
                             "rank:{}， name:{}, fitness:{}, shared_fitness:{}"
                             "  ,isSeed:{}, \nchromosome_bits: {}"
                             .format(rank, solution.name, solution.fitness,
                                     solution.shared_fitness, solution.isSeed,
                                     ''.join([str(x) for x in solution.chromosome_bits])))
            logger1.info("\n\n")

        elif generation == 'b':
            logger1.info("\n\n\n")
            logger1.info("<<<<<<<<<<<<<<<<<<<<<<<<<<Big Generation Logging>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            logger1.info("highest fitness in this Big Generation, name, fitness")
            logger1.info("highest fitness so far, name, fitness")
            logger1.info("no progress generation: {}".format(self.no_progress_generation))

    def monitor_progress(self, Solution):
        # TODO use highest_value
        self.no_progress_generation += 1
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
            s.get_classification_result(self)
            # (d) filter the solution with limited target returns
            is_s_not_removed = s.filter_solution_by_target_return(self)
            # (e) compute the fitness for solution
            if is_s_not_removed:
                american_stock_fitness = AmericanStockFitness(parameter_dict)
                american_stock_fitness(self.input_data_dict, s)
            # (f) s_fitness fix
            s.shared_fitness = s.fitness

    def process_new_solutions(self,new_generation_list):
        """Translate chromosome_bits, find targets, compute fitness"""
        for s in new_generation_list:
            # (b) translate chromosome bits list to decimal value
            s.translate_chromosome_bits(self.feature_pos_dict)
            # (c) get the classfiled result in each day
            s.get_classification_result(self)
            # (d) filter the solution with limited target returns
            is_s_not_removed = s.filter_solution_by_target_return(self)
            # (e) compute the fitness for solution
            if is_s_not_removed:
                american_stock_fitness = AmericanStockFitness(self.parameter_dict)
                american_stock_fitness(self.input_data_dict, s)

    def create_empty_chromosome_bits(self, parameter_dict):
        empty_chromosome_bits = []
        data_pos_in_chromosome_dict = parameter_dict['input']['data_pos_in_chromosome']
        data_pos_in_chromosome_sorted_list = sorted(list(data_pos_in_chromosome_dict.items()), key = lambda x:x[0])
        # append the buy/sell bit
        #empty_chromosome_bits.append(0)
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

        # add the decisive feature chosen bit to the end of the chromosome
        empty_chromosome_bits.extend([0 for x in range(parameter_dict['input']['feature_decide_bit_len'])])

        self.empty_chromosome_bits = empty_chromosome_bits
        chromosome_bits_length = len(empty_chromosome_bits)
        #print (empty_chromosome_bits, len(empty_chromosome_bits))
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