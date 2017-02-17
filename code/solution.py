# import from pjslib
from pjslib.general import get_upper_folder_path
from pjslib.general import accepts
from pjslib.logger import logger1
#================================================
import os
import sys
import collections
import math





class Solution():
    name_id = 0
    _all = []
    seed_list = []
    max_distance = 2

    def __init__(self):
        self.chromosome_bits = []
        self.feature_dict = collections.defaultdict(lambda : {})
        self.fitness = 0.0
        self.testing_fitness = 0.0
        self.is_f_computed = False
        self.shared_fitness = 0.0
        self.is_sf_computed = False
        self.m_i = 0.0
        self.isSeed = False
        self.solutions_of_same_species_list = []
        self.classification_result_dict = collections.defaultdict(lambda : [])
        self.classification_result_list = []
        self.classification_result_num = 0.0
        self.name = self.__class__.name_id
        self.__class__.name_id += 1
        self.__class__._all.append(self)

    @classmethod
    def replace_converged_seeds(cls):
        pass

    @classmethod
    def clear_seed_list(cls):
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
        def compute_m_i(fitness, tabu_list):
            m_i_all = 0.0
            for tabu_solution in tabu_list:
                distance = cls.compute_distance(fitness, tabu_solution)
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
                shared_fitness = compute_m_i(fitness, tabu_list)
                solution.shared_fitness = shared_fitness
                solution.is_sf_computed = True
                logger1.debug("solution: {}, shared_fitness:{}".format(solution.name, solution.shared_fitness))

        elif tabu_list == []:
            # assgin the fitness value to the shared_fitness in the 1st iteration
            for solution in cls._all:
                solution.shared_fitness = solution.fitness
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
                logger1.info("#SEED FOUND#")
                logger1.info("Seed name:{}, seed shared_fitness:{}, seed fitness:{}, seed list size:{}"
                             ", current seed radius:{}, small_generation:{}, big_generation:{}"
                              .format(solution.name, solution.shared_fitness, solution.fitness,
                                      len(cls.seed_list), seed_radius_value, ga.small_generation,
                                      ga.big_generation))
                logger1.info("#SEED FOUND END#")


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
                fractional_value = 0
                for i,bit in enumerate(binary_list):
                    i = i + 1
                    if bit == 1:
                        x_square = 0.5 ** i
                        fractional_value += x_square
                return fractional_value

            def convert_binary_to_decimal(binary_list):
                decimal_value = 0
                for i, binary_value in enumerate(binary_list):
                    if binary_value == 1:
                        decimal_value += 2**i
                return decimal_value

            # :::compute_solution_feature_value:::
            int_value = convert_binary_to_decimal(int_value_bits)
            decimal_value = get_fractional_value(decimal_value_bits)
            #print ("decimal_value:", decimal_value)
            feature_value  = int_value + decimal_value
            if is_sign_bit == []:
                return feature_value
            else:
                if is_sign_bit == 0:
                    return feature_value * (-1)
                else:
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
    def get_classification_result(self, parameter_dict, input_data_dict):

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
        # logging
        logger1.debug("============get_classification_result START!!============")
        logger1.debug("chromosome_bits: {}".format(self.chromosome_bits))
        logger1.debug("solution name: {}".format(self.name))

        # get the decisive feature if more than 1 target is seleted each time frame
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
                    for feature_name, feature_detail_dict in self.feature_dict.items():
                        # check the current feature is turned on
                        is_include = feature_detail_dict['is_include']
                        if not is_include:
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

                    if is_target_chosen == True:
                        # chose only 1 target every day, based on decisive feature, if it is sell, revert the sign
                        if is_decisive_feature == 0:
                            target_decisive_feature_tuple = (target, float(feature_value_dict[decisive_feature]))
                        elif is_decisive_feature == 1:
                            is_buy = self.chromosome_bits[0]
                            if is_buy == 1:
                                target_decisive_feature_tuple = (target, float(feature_value_dict[decisive_feature]))
                            elif is_buy == 0:
                                target_decisive_feature_tuple = (target, (-1)*float(feature_value_dict[decisive_feature]))


                        self.classification_result_dict[date_object].append(target_decisive_feature_tuple)
                        #logger1.info("self.classification_result_dict[date_object]: {}".format(self.classification_result_dict[date_object]))
                        is_target_chosen = False

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


        #logging
        logger1.debug("classification_result_list: {}".format(self.classification_result_list))
        logger1.debug("============get_classification_result END!!============")

        # return
        return self.classification_result_list






    def __str__(self):
        return self.name
