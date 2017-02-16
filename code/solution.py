# import from pjslib
from pjslib.general import get_upper_folder_path
from pjslib.general import accepts
from pjslib.logger import logger1
#================================================
import os
import sys
import collections





class Solution():
    name_id = 0
    _all = []
    def __init__(self, parameter_dict):
        self.chromosome_bits = []
        self.feature_dict = collections.defaultdict(lambda : {})
        self.fitness = 0.0
        self.is_f_computed = False
        self.shard_fitness = 0.0
        self.m_i = 0.0
        self.isSeed = False
        self.classification_result_dict = collections.defaultdict(lambda : [])
        self.classification_result_list = []
        self.classification_result_num = 0.0
        self.name = self.__class__.name_id
        self.__class__.name_id += 1
        self.__class__._all.append(self)
        self.parameter_dict = parameter_dict


    @classmethod
    def all(cls):
        return cls._all

    @classmethod
    def _clear(cls):
        cls._all = []

    @classmethod
    def compute_fitness(cls):
        all_solutions = cls._all

    def compute_distance(self, solution1, solution2):
        same_results_set = set(solution1.classification_result_list) & set(solution2.classification_result_list)
        distance = 1/same_results_set
        return distance

    def translate_chromosome_bits(self, feature_pos_dict):

        def compute_solution_feature_value(is_sign_bit, int_value_bits, decimal_value_bits):
            # big endian eg. 0101 -> 10
            def convert_binary_to_decimal(binary_list):
                decimal_value = 0
                for i, binary_value in enumerate(binary_list):
                    if binary_value == 1:
                        decimal_value += 2**i
                return decimal_value

            def get_real_decimal_value(temp_decimal_value):
                while temp_decimal_value >= 1:
                    temp_decimal_value /= 10
                decimal_value = temp_decimal_value
                return decimal_value

            # :::compute_solution_feature_value:::
            int_value = convert_binary_to_decimal(int_value_bits)
            temp_decimal_value = convert_binary_to_decimal(decimal_value_bits)
            decimal_value = get_real_decimal_value(temp_decimal_value)
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
    def get_classification_result(self, input_data_dict):

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
        decisive_feature_index = str(self.parameter_dict['input']['decisive_feature'])
        decisive_feature = self.parameter_dict['input']['raw_data_dict'][decisive_feature_index]

        chromosome_bits = self.chromosome_bits
        input_data_list = list(input_data_dict.items())
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
                        date_target_tuple = (date_object, target)
                        # chose only 1 target every day, based on decisive feature
                        target_decisive_feature_tuple = (target, float(feature_value_dict[decisive_feature]))
                        self.classification_result_dict[date_object].append(target_decisive_feature_tuple)


                        is_target_chosen = False

        # chose only 1 target every day, based on decisive feature
        for date_object, target_decisive_feature_tuple_pairs in self.classification_result_dict.items():
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



    def compute_m_i(self, tabu_list):
        pass



    def __str__(self):
        return self.name
