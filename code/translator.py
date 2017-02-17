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
import sys



class translator:
    #feature_id_value_dict : {8:(1,'0,0','-','66.6'),9:99.9....}
    def __init__(self, ga, feature_id_value_dict):
        self.parameter_dict = ga.parameter_dict
        self.feature_id_value_dict = feature_id_value_dict
        self.empty_chromosome_bits, self.chromosome_bits_length = ga.create_empty_chromosome_bits(ga.parameter_dict)
        self.feature_pos_dict = ga.create_feature_pos_dict(ga.parameter_dict)

    def translate_into_chromosome(self):
        for feature_id, feature_value_tuple in self.feature_id_value_dict.items():
            # feature_pos_dict: {'14':{'pos':[(26, 27), (27,29), (29,29), (29,37), (37,37)], 'name':... },'15':....}
            # get the values from the user input
            feature_pos_dict = self.feature_pos_dict
            # para_dict['input']['data_pos_in_chromosome'][8] = (1, 2, 1, 4, 4)
            chromosome_value_len_tuple = self.parameter_dict['input']['data_pos_in_chromosome'][feature_id]

            is_on = [feature_value_tuple[0]]
            operator = feature_value_tuple[1].split(',')
            sign = feature_value_tuple[2]
            if sign == '-':
                user_is_sign = 1
                sign_value = -1
            elif sign == '+':
                user_is_sign = 0
                sign_value = 1
            para_is_sign = chromosome_value_len_tuple[2]
            if user_is_sign == para_is_sign:
                pass
            else:
                print ("Check your input, {}'s value should not be negative".format(feature_id))
                sys.exit(0)

            int_value = int(feature_value_tuple[3].split('.')[0])
            temp_decimal_value = feature_value_tuple[3].split('.')[1]
            decimal_value = float(temp_decimal_value)/(len(temp_decimal_value) * 10)
            # ----------------------------------------------------------------------
            # (1.) get on/off bool, pos 1, on_off_pos: (26, 27)
            on_off_pos = feature_pos_dict[str(feature_id)]['pos'][0]
            self.empty_chromosome_bits[on_off_pos[0]:on_off_pos[1]] = is_on
            # (2.) operator
            operator_pos = feature_pos_dict[str(feature_id)]['pos'][1]
            self.empty_chromosome_bits[operator_pos[0]:operator_pos[1]] = operator
            # (3.) sign
            sign_pos = feature_pos_dict[str(feature_id)]['pos'][2]
            self.empty_chromosome_bits[sign_pos[0]:sign_pos[1]] = chromosome_value_len_tuple[2]
            # (4.) get int_bits, pos 3
            int_bits_list  = list("{0:b}".format(int_value))
            int_max_bit_len = chromosome_value_len_tuple[3]
            int_bits_len = len(int_bits_list)
            if int_bits_len > int_max_bit_len:
                print ("int out of range, too big!!")
                sys.exit(0)
            else:
                int_bits_list = [0 for x in int_max_bit_len]
                int_bits_list[0:len(int_bits_list)] = int_bits_list
            int_bits_pos = feature_pos_dict[str(feature_id)]['pos'][3]
            self.empty_chromosome_bits[int_bits_pos[0]:int_bits_pos[1]] = int_bits_list
            # (5.) get decimal bits
            decimal_empty_list = [0 for i in range(chromosome_value_len_tuple[4])]
            decimal_bits_len = len(decimal_empty_list)
            binary_sqaure_list = [x+1 for x in range(decimal_bits_len)]
            #binary_sqaure_list.reverse()
            for i in binary_sqaure_list:
                decimal_loop_value = 0.5**i
                if decimal_value < decimal_loop_value:
                    continue
                elif decimal_value == decimal_loop_value:
                    decimal_empty_list[i-1] = 1
                    break
                elif decimal_value > decimal_loop_value:
                    decimal_empty_list[i-1] = 1
                    decimal_value -= decimal_loop_value





        pass

