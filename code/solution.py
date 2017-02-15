# import from pjslib
from pjslib.general import get_upper_folder_path
from pjslib.general import accepts
from pjslib.logger import logger1
#================================================
import os
import sys





class Solution():
    name_id = 0
    _all = []
    def __init__(self):
        self.chromosome_bits = []
        self.fitness = 0.0
        self.is_f_computed = False
        self.shard_fitness = 0.0
        self.m_i = 0.0
        self.isSeed = False
        self.classification_result_list = []
        self.name = self.__class__.name_id
        self.__class__.name_id += 1
        self.__class__._all.append(self)

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

    # input_data_dict:
    # (datetime.date(2011,6,24), defaultdict{'MRK':Feature(quarter = '2', stock = 'MRK',....), 'VZ':Feature(....)})
    def get_classification_result(self, feature_pos_dict, input_data_dict):

        def compute_solution_value(is_sign_bit, int_value_index, decimal_value_index):
            pass
        def compare_data_solution_value(operator_bit_str, data_feature_value, solution_feature_value):
            if operator_bit_str == '00':
                pass
            elif operator_bit_str == '01':
                pass
            elif operator_bit_str == '10':
                pass
            elif operator_bit_str == '11':
                pass
        #:::get_classification_result:::



        chromosome_bits = self.chromosome_bits
        input_data_list = list(input_data_dict.items())
        for date_object, target_dict in input_data_list:
            chosen_target_list = []
            _1 = True
            _2 = True
            _3 = True
            # target: 'MRK','VZ', feature_value_tuple: Feature(quarter = '2', stock = 'MRK',....)
            for target,feature_value_tuple in target_dict.items():
                feature_value_dict = dict(feature_value_tuple._asdict)
                _1 = True
                while _1 == True:
                # feature_id : '8', value_dict['name']:'percent_change_price', value_dict['pos']:[(0,1),(1,3),(3,4),(4,8),(8,15)]
                    for feature_id, value_dict in feature_pos_dict.items():
                        _2 = True
                        feature_name = value_dict['name']
                        feature_pos_list = value_dict['pos']
                        is_include_index = feature_pos_list[0]
                        operator_index = feature_pos_list[1]
                        is_sign_index = feature_pos_list[2]
                        int_value_index = feature_pos_list[3]
                        decimal_value_index = feature_pos_list[4]

                        #
                        is_include = chromosome_bits[is_include_index[0]:is_include_index[1]]
                        if not is_include:
                            continue
                        operator_bits = chromosome_bits[operator_index[0]:operator_index[1]]
                        is_sign_bit = chromosome_bits[is_sign_index[0]:is_sign_index[1]]
                        int_value_index = chromosome_bits[int_value_index[0]:int_value_index[1]]
                        decimal_value_index = chromosome_bits[decimal_value_index[0]:decimal_value_index[1]]

                        data_feature_value = feature_value_dict['feature_name']
                        solution_feature_value = compute_solution_value(is_sign_bit, int_value_index, decimal_value_index)

                        # while _2 == True:
                        #     # feature_pos_tuple ：(1,3)
                        #     for i,feature_pos_tuple in enumerate(feature_pos_list):
                        #         # detect if the feature is included, if it is not, continue to the next feature
                        #         if i == 0:
                        #             is_include = chromosome_bits[feature_pos_tuple[0], feature_pos_tuple[1]]
                        #             if not is_include:
                        #                 _2 = False
                        #         else:
                        #             operator_bits = chromosome_bits(1,3)


        pass

    def compute_m_i(self, tabu_list):
        pass



    def __str__(self):
        return self.name
