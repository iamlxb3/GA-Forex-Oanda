# import from pjslib
from pjslib.general import get_upper_folder_path
from pjslib.general import accepts
from pjslib.logger import logger1, logger_t
#================================================
import os
import sys
import collections
import math
import random
import pprint



class Solution():
    name_id = 0
    _all = []
    seed_list = []
    conserved_seed_list = []
    top_solution_list = []
    converged_solution_set = set()
    max_distance = 2
    highest_solution_list = []

    def __init__(self):
        self.chromosome_bits = []
        self.feature_dict = collections.defaultdict(lambda : {})
        self.fitness = 0.0
        self.testing_fitness = 0.0
        self.is_f_computed = False
        self.shared_fitness = 0.0
        self.is_sf_computed = False
        self.profit = 0.0
        self.m_i = 0.0
        self.isSeed = False
        self.solutions_of_same_species_list = []
        self.classification_result_dict = collections.defaultdict(lambda : [])
        # self.classification_result_list is sorted
        self.classification_result_list = []
        self.classification_result_num = 0.0
        self.decisive_feature = ''
        self.is_multiple_return = False
        #return_value_by_time_dict: 'date_objec:{0.9,0.8}, ...}
        self.return_value_by_time_dict = collections.defaultdict(lambda : [])
        self.name = self.__class__.name_id
        self.__class__.name_id += 1
        self.__class__._all.append(self)

    @classmethod
    def compute_profit(cls):
        solutions_list = cls._all
        for solution in solutions_list:
            return_value_by_time_list = sorted(solution.return_value_by_time_dict.items(), key = lambda x:x[0])
            initial_capital = 1
            capital = initial_capital
            for date, value_unit_time_list in return_value_by_time_list:
                temp_profit = 0
                # iterate by stocks, buy multiple stocks
                for value in value_unit_time_list:
                    profit = capital * (value/100)
                    temp_profit += profit
                capital += temp_profit
                #print ("solution name:{}, capital:{}, temp_profit:{}".format(solution.name, capital, temp_profit))
            profit = (capital - initial_capital) / initial_capital
            profit = float("{:2.1f}".format(profit*100))
            #print("solution name:{}, profit:{}".format(solution.name, profit))
            solution.profit = profit



    @classmethod
    def process_b_g(cls):
        highest_solution = sorted(cls._all, key = lambda x:x.fitness, reverse = True)[0]
        cls.highest_solution_list.append(highest_solution)


    @classmethod
    def update_tabu_list(cls, ga):
        ga.tabu_list = list(set(cls.conserved_seed_list) | set(cls.top_solution_list))
        for solution in cls._all:
            solution.is_sf_computed = False
        tabu_list_display = [(s.name, s.fitness) for s in ga.tabu_list]
        logger1.info("#TABU_LIST# tabu_list has been updated, content:{}".format(tabu_list_display))

    @classmethod
    def find_converged_solutions(cls,ga):
        # initailize
        cls.converged_solution_set = set()
        cls.top_solution_list = []
        ##
        converge_limit = ga.parameter_dict['DSGA']['CL']

        converge_dict = collections.defaultdict(lambda :[])
        all_solution = cls._all
        for solution in all_solution:
            returned_result = tuple(solution.classification_result_list)
            converge_dict[returned_result].append(solution)

        converge_dict_value_list = list(converge_dict.values())
        converge_dict_value_list = sorted(converge_dict_value_list, key = lambda x:len(x), reverse = True)
        for i,list1 in enumerate(converge_dict_value_list):
            converge_dict_value_list[i] = [x.name for x in list1]

        #print ("converge_dict_value_list :{}".format(pprint.pformat(converge_dict_value_list)))
        #print("converge_limit :{}".format(converge_limit))

        for converge_list, solution_list in converge_dict.items():
            if len(solution_list) < converge_limit:
                logger1.debug("CONVERGE GIVE UP, TOO few solutions converged in this species: {},"
                              "converge_limit: {}"
                              .format(len(solution_list), converge_limit))
                continue

            # add the top solution in every species,ready for tabu list
            solution_list = sorted(solution_list, key=lambda x: x.fitness, reverse=True)
            top_solution = solution_list[0]
            cls.top_solution_list.append(top_solution)
            #
            for i, solution in enumerate(solution_list):
                # skip 0, because the species best solution should be kept
                if i!= 0:
                    cls.converged_solution_set.add(solution)
                    logger1.debug("#CONVERGE# Add solution to converge list, name: {}, fitness: {}"
                                  .format(solution.name, solution.fitness))
                    logger_t.debug("#CONVERGE# Add solution to converge list, name: {}, fitness: {}"
                                  .format(solution.name, solution.fitness))

    @classmethod
    def replace_converged_solutions(cls,ga):
        cls.find_converged_solutions(ga)
        #TEMP PRINT
        converged_solution_set_print = [x.name for x in cls.converged_solution_set]
        conserved_seed_list_print = [x.name for x in cls.conserved_seed_list]
        #print("converged_solution_set: ", converged_solution_set_print)
        #print("conserved_seed_list: ", conserved_seed_list_print)

        # TEMP PRINT
        solution_set_for_delete = cls.converged_solution_set - set(cls.conserved_seed_list)
        solution_delete_num  = len(solution_set_for_delete)
        #print ("solution_delete_num: ", solution_delete_num)
        #print("solution_set_for_delete: ", solution_set_for_delete)
        for solution in solution_set_for_delete:
            cls._all.remove(solution)
            logger1.info("#SOLUTION_REMOVE# removing solution, name: {}, fitness: {}"
                          .format(solution.name, solution.fitness))
        # randomly create new solutions
        new_generation_list = []
        for i in range(solution_delete_num):
            _, chromosome_bits_length = ga.create_empty_chromosome_bits(ga.parameter_dict)
            random_chromosome = [random.randint(0, 1) for p in range(chromosome_bits_length)]
            s = Solution()
            s.chromosome_bits = random_chromosome
            new_generation_list.append(s)
        ga.process_new_solutions(new_generation_list)



    @classmethod
    def clear_seed_list(cls):
        # conserve seed list for replacement and updating tabu list
        cls.conserved_seed_list = cls.seed_list
        cls.seed_list = []

    @classmethod
    def compute_distance(cls, solution1, solution2):
        same_results_set = set(solution1.classification_result_list) & set(solution2.classification_result_list)
        same_results_set_size = len(same_results_set)
        if not same_results_set:
            distance = cls.max_distance
        else:
            distance = 1/same_results_set_size
        return distance

    @classmethod
    def compute_shared_fitness(cls, ga):
        # TODO , compute_m_i here is modified, because the one in the paper has some problem as far as I can see
        def compute_m_i(solution, tabu_list):
            fitness = float(solution.fitness)
            m_i_all = 0.0
            for tabu_solution in tabu_list:
                distance = cls.compute_distance(solution, tabu_solution)
                m_i = fitness * distance
                m_i_all += m_i
            return m_i_all

        # :::compute_shared_fitness:::
        tabu_list = ga.tabu_list
        # you do not need
        if tabu_list:
            for solution in cls._all:
                if solution.is_sf_computed:
                    continue
                fitness = solution.fitness
                shared_fitness = compute_m_i(solution, tabu_list)
                solution.shared_fitness = float(shared_fitness)
                solution.is_sf_computed = True
                logger1.debug("solution: {}, shared_fitness:{}".format(solution.name, solution.shared_fitness))

        elif tabu_list == []:
            # assgin the fitness value to the shared_fitness in the 1st iteration
            for solution in cls._all:
                solution.shared_fitness = float(solution.fitness)
            logger1.info("NO tabu_list Found!")
            return


    @classmethod
    def find_seed_solution(cls, ga):
        def get_solution_in_radius():
            pass
            #seed_list
    #:::find_seed_solution:::

        max_population_num = ga.parameter_dict['SGA']['max_population_num']
        seed_max_ratio = ga.parameter_dict['DSGA']['seed_max_ratio']
        max_seed_num = math.ceil(seed_max_ratio * max_population_num)
        seed_radius = ga.seed_radius
        seed_radius_value = seed_radius.IS

        sorted_soluion_list = sorted(cls._all, key = lambda x:x.shared_fitness, reverse = True)
        for solution in sorted_soluion_list:
            seed_list_size = len(cls.seed_list)
            # we don't expect too much seed
            if seed_list_size > max_seed_num:
                break
            is_seed = True
            # get the updated_seed_list
            newest_seed_list = cls.seed_list
            for seed_solution in newest_seed_list:
                distance = cls.compute_distance(seed_solution, solution)
                # which means this solution is in the radius of one species, break the inner for loop and test the next solution
                if distance < seed_radius_value:
                    is_seed = False
                    seed_solution.solutions_of_same_species_list.append(solution)
                    break
            # if this solution does not belong to any of the species, add to seed list
            if is_seed:
                solution.isSeed = True
                cls.seed_list.append(solution)
                logger1.debug("#SEED FOUND#")
                logger1.debug("Seed name:{}, seed shared_fitness:{}, seed fitness:{}, seed list size:{}"
                             ", current seed radius:{}, small_generation:{}, big_generation:{}"
                              .format(solution.name, solution.shared_fitness, solution.fitness,
                                      len(cls.seed_list), seed_radius_value, ga.small_generation,
                                      ga.big_generation))
                logger1.debug("#SEED FOUND END#")


    @classmethod
    def filter_solution_pool(cls,ga):
        # can be solutions_list or solution set
        def get_left_solution_num(solutions_list, eliminate_ratio):
            solution_num_in_one_species = len(solutions_list)
            # eliminate_ratio = 0.2, ceil(1-1*0.2) = 1, ceil(2-2*0.2) = 2,  ceil(3-3*0.2) = 3
            # ceil(4-4*0.2) = 4, ceil(5-5*0.2) = 4, ceil(6-6*0.2) = 5
            left_solution_num = math.ceil(solution_num_in_one_species - eliminate_ratio*solution_num_in_one_species)
            return left_solution_num

        # :::filter_solution_pool
        logger1.info("Solution removal Start!!!")
        eliminate_ratio = ga.parameter_dict['DSGA']['eliminate_ratio']
        solutions_in_seed_species_set = set()
        removed_solution_num = 0.0
        for seed_solution in cls.seed_list:
            one_species_solutions_list = sorted(seed_solution.solutions_of_same_species_list,
                                          key = lambda x:x.shared_fitness, reverse = True)
            # update the set of solutions in seed areas
            solutions_in_seed_species_set.update(set(one_species_solutions_list))
            left_solution_num = get_left_solution_num(one_species_solutions_list, eliminate_ratio)
            for i, solution in enumerate(one_species_solutions_list):
                # delete the trailing solutions
                if i > left_solution_num:
                    try:
                        cls._all.remove(solution)
                        removed_solution_num += left_solution_num
                        # temp logging
                        logger1.info("removed solution:{}, fitness: {} in seed".format(solution.name, solution.fitness))
                    except ValueError:
                        logger1.debug("Value Error, {} solution has been deleted!!".format(solution.name))
        logger1.info("{} solutions have been removed in seed areas".format(removed_solution_num))

        # start remove the solutions out of the seed area

        solutions_in_wild_list = sorted(list(set(cls._all) - solutions_in_seed_species_set), key = lambda x:x.shared_fitness, reverse = True )
        left_solution_num = get_left_solution_num(solutions_in_wild_list, eliminate_ratio)
        removed_solution_num = 0.0
        for i, solution in enumerate(solutions_in_wild_list):
            # delete the trailing solutions
            if i > left_solution_num:
                try:
                    cls._all.remove(solution)
                    # temp logging
                    logger1.info("removed solution:{}, fitness: {} in wild".format(solution.name, solution.fitness))
                except ValueError:
                    logger1.debug("Value Error, {} solution has been deleted!!".format(solution.name))
                removed_solution_num += 1
        logger1.info("{} solutions have been removed in wild".format(removed_solution_num))
        logger1.info("Solution removal END!!!")


    @classmethod
    def all(cls):
        return cls._all

    @classmethod
    def _clear(cls):
        cls._all = []

    @classmethod
    def compute_fitness(cls):
        all_solutions = cls._all

    def filter_solution_by_target_return(self, ga):
        """filter_solution with too few targets return"""
        input_data_num = ga.input_data_num
        parameter_dict = ga.parameter_dict
        target_return_percent = parameter_dict['SGA']['target_return_percent'] / 100
        classified_target_num = len(self.classification_result_list)

        threshold = math.ceil(input_data_num * target_return_percent)
        logger1.debug("#Solution Filter#")
        if classified_target_num < threshold:
            self.__class__._all.remove(self)
            logger1.debug("Solution removed!!!!, name: {}, classification_result_list:{}, classified_target_num:{}"
                          "target_return_percent: {}%, input_data_num:{}, threshold:{}"
                          .format(self.name, self.classification_result_list, classified_target_num,
                                  target_return_percent*100, input_data_num, threshold))
            logger1.debug("#Solution Filter End#")
            return False
        else:
            logger1.debug("Solution returned target number passed, name: {}, classification_result_list:{}, "
                          "classified_target_num:{}, target_return_percent: {}%, input_data_num:{}"
                          ", threshold:{} "
                            .format(self.name, self.classification_result_list, classified_target_num,
                                    target_return_percent * 100, input_data_num, threshold))
            logger1.debug("#Solution Filter End#")
            return True



    def translate_chromosome_bits(self, feature_pos_dict):

        def compute_solution_feature_value(is_sign_bit, int_value_bits, decimal_value_bits):
            # big endian eg. 0101 -> 10
            def get_fractional_value(binary_list):
                """input should be the fractional binary part"""
                # TODO, check the input
                binary_list = [int(x) for x in binary_list]
                fractional_value = 0
                for i,bit in enumerate(binary_list):
                    i = i + 1
                    if bit == 1:
                        x_square = 0.5 ** i
                        fractional_value += x_square
                return fractional_value

            def convert_binary_to_decimal(binary_list):
                decimal_value = 0
                # TODO, check the input
                binary_list = [int(x) for x in binary_list]
                for i, binary_value in enumerate(binary_list):
                    if binary_value == 1:
                        decimal_value += 2**i
                return decimal_value

            # :::compute_solution_feature_value:::
            int_value = convert_binary_to_decimal(int_value_bits)
            decimal_value = get_fractional_value(decimal_value_bits)
            feature_value  = int_value + decimal_value

            if is_sign_bit == []:
                return feature_value
            else:
                if is_sign_bit[0] == 0:
                    return feature_value * (-1)
                elif is_sign_bit[0] == 1:
                    return feature_value

        #:::translate_chromosome_bits:::
        chromosome_bits = self.chromosome_bits
        for feature_id, value_dict in feature_pos_dict.items():
            # get the index
            feature_name = value_dict['name']
            feature_pos_list = value_dict['pos']
            is_include_index = feature_pos_list[0]
            operator_index = feature_pos_list[1]
            is_sign_index = feature_pos_list[2]
            int_value_index = feature_pos_list[3]
            decimal_value_index = feature_pos_list[4]
            # get the bit_value_list
            is_include = chromosome_bits[is_include_index[0]:is_include_index[1]][0]
            operator_bits = chromosome_bits[operator_index[0]:operator_index[1]]
            # convert int to str
            operator_bits = [str(x) for x in operator_bits]
            operator_bits_str = ''.join(operator_bits)
            is_sign_bit = chromosome_bits[is_sign_index[0]:is_sign_index[1]]
            int_value_bits = chromosome_bits[int_value_index[0]:int_value_index[1]]
            decimal_value_bits = chromosome_bits[decimal_value_index[0]:decimal_value_index[1]]


            solution_feature_value = compute_solution_feature_value(is_sign_bit, int_value_bits, decimal_value_bits)

            # ============================================
            # translate the solution value and save in dict
            self.feature_dict[feature_name]['is_include'] = is_include
            self.feature_dict[feature_name]['operator'] = operator_bits_str
            self.feature_dict[feature_name]['value'] = solution_feature_value



    # input_data_dict:
    # (datetime.date(2011,6,24), defaultdict{'MRK':Feature(quarter = '2', stock = 'MRK',....), 'VZ':Feature(....)})
    def get_classification_result(self, ga):

        def find_the_decisive_feature(ga):
            # find the decisive feature according to the bits
            # =================================================================================
            feature_pos_dict = ga.feature_pos_dict
            parameter_dict = ga.parameter_dict
            feature_decisive_bit_len = parameter_dict['input']['feature_decide_bit_len']
            target_chosen_bits_list = self.chromosome_bits[(-1) * feature_decisive_bit_len:]
            # this id is not the same as the one in the para dict,
            feature_id_chosen = sum([2 ** i for i, x in enumerate(target_chosen_bits_list) if x == 1])
            # feature_pos_dict: {'14':{'pos':[(26, 27), (27,29), (29,29), (29,37), (37,37)], 'name':... },'15':....}
            sorted_feature_value_dict = sorted(list(feature_pos_dict.items()), key=lambda x: int(x[0]))
            feature_num = len(sorted_feature_value_dict)
            # use the default decisive feature if the index is too big
            if feature_id_chosen + 1 > feature_num:
                # use the default feature index
                decisive_feature_index = parameter_dict['input']['decisive_feature'][1]
            else:
                decisive_feature_index = sorted_feature_value_dict[feature_id_chosen][0]

            decisive_feature = parameter_dict['input']['raw_data_dict'][str(decisive_feature_index)]
            logger1.debug("solution name :{}, decisive_feature chosen: {}, chosen_bits_list： {}"
                          .format(self.name, decisive_feature, target_chosen_bits_list))
            self.decisive_feature = decisive_feature
            # =================================================================================

        def compare_data_solution_value(operator_bits_str, data_feature_value, solution_feature_value):
            # <
            if operator_bits_str == '00':
                if data_feature_value < solution_feature_value:
                    return True
                else:
                    return False
            # <=
            elif operator_bits_str == '01':
                if data_feature_value <= solution_feature_value:
                    return True
                else:
                    return False
            # >
            elif operator_bits_str == '10':
                if data_feature_value > solution_feature_value:
                    return True
                else:
                    return False
            # >=
            elif operator_bits_str == '11':
                if data_feature_value >= solution_feature_value:
                    return True
                else:
                    return False

        #:::get_classification_result:::
        # (1) find the decisive feature
        find_the_decisive_feature(ga)
        # logging
        logger1.debug("============get_classification_result START!!============")
        logger1.debug("chromosome_bits: {}".format(self.chromosome_bits))
        logger1.debug("solution name: {}".format(self.name))

        # get the decisive feature if more than 1 target is seleted each time frame
        parameter_dict = ga.parameter_dict
        input_data_dict = ga.input_data_dict
        is_decisive_feature, decisive_feature_index = parameter_dict['input']['decisive_feature']
        decisive_feature = parameter_dict['input']['raw_data_dict'][str(decisive_feature_index)]
        chromosome_bits = self.chromosome_bits
        # sort the input_data_list
        input_data_list = sorted(list(input_data_dict.items()), key = lambda x:x[0])

        for date_object, target_dict in input_data_list:
            # target: 'MRK','VZ', feature_value_tuple: Feature(quarter = '2', stock = 'MRK',....)
            for target,feature_value_tuple in target_dict.items():
                feature_value_dict = dict(feature_value_tuple._asdict())
                is_target_chosen = True
                while is_target_chosen == True:
                # feature_id : '8', value_dict['name']:'percent_change_price', value_dict['pos']:[(0,1),(1,3),(3,4),(4,8),(8,15)]
                    feature_num = len(self.feature_dict.items())
                    is_not_include_f_num = 0
                    for feature_name, feature_detail_dict in self.feature_dict.items():

                        # check the current feature is turned on
                        is_include = feature_detail_dict['is_include']
                        if not is_include:
                            is_not_include_f_num += 1
                            logger1.debug("date:{}, stock:{},feature_name:{} is not included".format(date_object, target,feature_name))
                            continue

                        operator_bits_str = feature_detail_dict['operator']
                        solution_feature_value = feature_detail_dict['value']
                        # check the feature_value in data is valid
                        try:
                            data_feature_value = float(feature_value_dict[feature_name])
                        except ValueError:
                            logger1.error("ERROR VALUE---{}", feature_value_dict[feature_name])
                            logger1.error("date:{}, target:{}, feature:{}",date_object, target, feature_name)
                            logger1.error("CHECK YOUR DATA")
                            sys.exit(0)


                        # ============test whether the solution will choose the current stock
                        is_feature_satisfied = compare_data_solution_value(operator_bits_str, data_feature_value,
                                                                           solution_feature_value)
                        #==========================logging==========================
                        # only log the included feature
                        logger1.debug("date:{}, stock:{}, feature_name:{}, data_feature_value:{},"
                                      " solution_feature_value:{}, operator: {} is_satisfied:{}".format(
                            date_object, target, feature_name, data_feature_value, solution_feature_value,
                            operator_bits_str, is_feature_satisfied
                        ))
                        # ==========================logging end==========================
                        if is_feature_satisfied:
                            continue
                        else:
                            is_target_chosen = False

                    # # find the decisive feature according to the bits
                    # #=================================================================================
                    # feature_pos_dict = ga.feature_pos_dict
                    # feature_decisive_bit_len = parameter_dict['input']['feature_decide_bit_len']
                    # target_chosen_bits_list = self.chromosome_bits[(-1)*feature_decisive_bit_len:]
                    # # this id is not the same as the one in the para dict,
                    # feature_id_chosen = sum([2**i for i,x in enumerate(target_chosen_bits_list) if x == 1])
                    # # feature_pos_dict: {'14':{'pos':[(26, 27), (27,29), (29,29), (29,37), (37,37)], 'name':... },'15':....}
                    # sorted_feature_value_dict = sorted(list(feature_pos_dict.items()), key = lambda x:int(x[0]))
                    # feature_num = len(sorted_feature_value_dict)
                    # # use the default decisive feature if the index is too big
                    # if feature_id_chosen + 1 > feature_num:
                    #     pass
                    # else:
                    #     decisive_feature_index = sorted_feature_value_dict[feature_id_chosen][0]
                    #     decisive_feature = parameter_dict['input']['raw_data_dict'][str(decisive_feature_index)]
                    # logger1.debug("solution name :{}, decisive_feature chosen: {}, chosen_bits_list： {}"
                    #        .format(self.name, decisive_feature, target_chosen_bits_list))
                    # self.decisive_feature = decisive_feature
                    # # =================================================================================
                    # TODO test this feature
                    # at lesat one feature should be turned on
                    if is_target_chosen == True and (is_not_include_f_num != feature_num):
                        # chose only 1 target every day, based on decisive feature, if it is sell, revert the sign
                        if is_decisive_feature == 0:
                            target_decisive_feature_tuple = (target, float(feature_value_dict[self.decisive_feature]))
                        elif is_decisive_feature == 1:
                            is_buy = self.chromosome_bits[0]
                            if is_buy == 1:
                                target_decisive_feature_tuple = (target, float(feature_value_dict[self.decisive_feature]))
                            elif is_buy == 0:
                                target_decisive_feature_tuple = (target, (-1)*float(feature_value_dict[self.decisive_feature]))


                        self.classification_result_dict[date_object].append(target_decisive_feature_tuple)
                        #logger1.info("self.classification_result_dict[date_object]: {}".format(self.classification_result_dict[date_object]))
                    is_target_chosen = False

        # multiple_return_switch
        # single return for one day
        multiple_return_switch = parameter_dict['SGA']['multiple_return_switch']
        if multiple_return_switch == 0:
            # chose only 1 target every day, based on decisive feature
            for date_object, target_decisive_feature_tuple_pairs in sorted(list(self.classification_result_dict.items()), key = lambda x:x[0]):
                if len(target_decisive_feature_tuple_pairs) > 1:
                    chosen_tuple = sorted(target_decisive_feature_tuple_pairs, key = lambda x:x[1], reverse = True)[0]
                    date_target_tuple = (date_object, chosen_tuple[0])
                    self.classification_result_list.append(date_target_tuple)
                elif len(target_decisive_feature_tuple_pairs) == 1:
                    date_target_tuple = (date_object, target_decisive_feature_tuple_pairs[0][0])
                    self.classification_result_list.append(date_target_tuple)
                else:
                    logger1.error("ERROR, CHECK target_decisive_feature_tuple_pairs!!")
        # multiple return for one day
        elif multiple_return_switch == 1:
            self.is_multiple_return = True
            for date_object, target_decisive_feature_tuple_pairs in sorted(
                    list(self.classification_result_dict.items()), key=lambda x: x[0]):
                for temp_date_target_tuple in target_decisive_feature_tuple_pairs:
                    date_target_tuple  = (date_object, temp_date_target_tuple[0])
                    self.classification_result_list.append(date_target_tuple)



        #logging
        logger1.debug("classification_result_list: {}".format(self.classification_result_list))
        logger1.debug("============get_classification_result END!!============")

        # return
        return self.classification_result_list






    def __str__(self):
        return self.name
