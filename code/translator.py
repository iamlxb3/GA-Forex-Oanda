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



class Translator:
    #feature_id_value_dict : {8:(1,'0,0','-','66.6',2),9:99.9....}
    def __init__(self, ga, feature_id_value_dict):
        self.parameter_dict = ga.parameter_dict
        self.feature_id_value_dict = feature_id_value_dict
        self.empty_chromosome_bits, self.chromosome_bits_length = ga.create_empty_chromosome_bits(ga.parameter_dict)
        self.feature_pos_dict = ga.feature_pos_dict

    @property
    def chromosome_len(self):
        return len(self.empty_chromosome_bits)

    def __str__(self):
        empty_chromosome_bits = [str(x) for x in self.empty_chromosome_bits]
        return  ''.join(empty_chromosome_bits)

    def translate_into_chromosome(self):
        for feature_id, feature_value_tuple in self.feature_id_value_dict.items():

            if feature_id == 'decisive_feature_pos':
                # feature_pos_dict: {'14':{'pos':[(26, 27), (27,29), (29,29), (29,37), (37,37)], 'name':... },'15':....}
                # get first_decisive_feature_pos
                feature_pos_num = feature_value_tuple
                first_decisive_feature_pos_list = list("{:b}".format(feature_pos_num))
                first_decisive_feature_pos_list.reverse()
                first_decisive_feature_pos_list = [int(x) for x in first_decisive_feature_pos_list]
                feature_decide_bit_len = int(self.parameter_dict['input']['feature_decide_bit_len'])
                decisive_bit_list = [0 for x in range(feature_decide_bit_len)]
                decisive_bit_list[0:len(first_decisive_feature_pos_list)] = first_decisive_feature_pos_list
                # (6.) decisive_feature bits
                self.empty_chromosome_bits[-1*feature_decide_bit_len:] = decisive_bit_list
                continue

            # get the values from the user input
            feature_pos_dict = self.feature_pos_dict
            # para_dict['input']['data_pos_in_chromosome'][8] = (1, 2, 1, 4, 4)
            chromosome_value_len_tuple = self.parameter_dict['input']['data_pos_in_chromosome'][str(feature_id)]

            is_on = [feature_value_tuple[0]]
            operator = feature_value_tuple[1].split(',')
            sign = feature_value_tuple[2]
            if sign == '-':
                sign_value = 0
            elif sign == '+':
                sign_value = 1

            para_is_sign = chromosome_value_len_tuple[2]

            int_value = int(feature_value_tuple[3].split('.')[0])

            try:
                temp_decimal_value = feature_value_tuple[3].split('.')[1]
                decimal_value = float(temp_decimal_value)/10 ** (len(temp_decimal_value))
            except IndexError:
                decimal_value = 0
            # ----------------------------------------------------------------------
            # (1.) get on/off bool, pos 1, on_off_pos: (26, 27)
            on_off_pos = feature_pos_dict[str(feature_id)]['pos'][0]
            self.empty_chromosome_bits[on_off_pos[0]:on_off_pos[1]] = is_on
            # (2.) operator
            operator_pos = feature_pos_dict[str(feature_id)]['pos'][1]
            self.empty_chromosome_bits[operator_pos[0]:operator_pos[1]] = operator
            # (3.) sign
            if para_is_sign:
                sign_pos = feature_pos_dict[str(feature_id)]['pos'][2]
                self.empty_chromosome_bits[sign_pos[0]:sign_pos[1]] = [sign_value]
            # (4.) get int_bits, pos 3
            computed_int_bits_list  = list("{0:b}".format(int_value))
            computed_int_bits_list.reverse()
            computed_int_bits_list = [int(x) for x in computed_int_bits_list]
            int_max_bit_len = chromosome_value_len_tuple[3]
            computed_int_bits_list_len = len(computed_int_bits_list)
            if computed_int_bits_list_len > int_max_bit_len:
                print ("int out of range, too big!!")
                sys.exit(0)
            else:
                int_bits_list = [0 for x in range(int_max_bit_len)]
                int_bits_list[0:computed_int_bits_list_len] = computed_int_bits_list
            int_bits_pos = feature_pos_dict[str(feature_id)]['pos'][3]
            self.empty_chromosome_bits[int_bits_pos[0]:int_bits_pos[1]] = int_bits_list
            # (5.) get decimal bits
            decimal_bits_list = [0 for i in range(chromosome_value_len_tuple[4])]
            decimal_bits_len = len(decimal_bits_list)
            binary_sqaure_list = [x+1 for x in range(decimal_bits_len)]
            #binary_sqaure_list.reverse()

            for i in binary_sqaure_list:
                decimal_loop_value = 0.5**i
                if decimal_value < decimal_loop_value:
                    continue
                elif decimal_value == decimal_loop_value:
                    decimal_bits_list[i-1] = 1
                    break
                elif decimal_value > decimal_loop_value:
                    decimal_bits_list[i-1] = 1
                    decimal_value -= decimal_loop_value
            decimal_bits_pos = feature_pos_dict[str(feature_id)]['pos'][4]
            self.empty_chromosome_bits[decimal_bits_pos[0]:decimal_bits_pos[1]] = decimal_bits_list
        return self.empty_chromosome_bits


#=============================================================================================================
# def __init__(self, ga, feature_id_value_dict):
#feature_id_value_dict : {8:(1,'0,0','-','66.6'),9:99.9....}

reader1 = ReadParameters()
parameter_dict = reader1.read_parameters(reader1.path)
formatter1 = Formatter(parameter_dict)
input_data_dict = formatter1.format_and_create_dict(formatter1.path, formatter1.feature_choice_list)
ga = GeneticAlgorithm(parameter_dict, input_data_dict)



#=======================USER_INPUT=======================
feature_id_value_dict = {}
feature_id_value_dict['decisive_feature_pos'] = 0
feature_id_value_dict[8] = (1,'1,0','+','0.6')
feature_id_value_dict[9] = (1,'0,1','+','32')
feature_id_value_dict[14] = (1,'1,1','+','52')
feature_id_value_dict[15] = (1,'0,1','+','0.25')
#=======================USER_INPUT=======================


#==========value to chromosome===========================
translator = Translator(ga, feature_id_value_dict)
print("=========Translator Ready!!============")
chromosome_list = translator.translate_into_chromosome()
print ("chromosome_list [42:46] {}".format(chromosome_list[42:46]))
translator.chromosome_len
print(translator)
#==========value to chromosome===========================

#==========chromosome to value===========================
import pprint
pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(stuff)



s = Solution()
feature_pos_dict= ga.feature_pos_dict
s.chromosome_bits = chromosome_list
s.translate_chromosome_bits(feature_pos_dict)
pp.pprint(s.feature_dict)

#==========chromosome to value===========================