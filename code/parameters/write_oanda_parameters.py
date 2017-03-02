import collections
import json


#==========================================================INPUT=====================================================================
para_dict = collections.defaultdict(lambda: collections.defaultdict(lambda:{}))
para_dict['input']['raw_data_path'] = ''
para_dict['input']['raw_data_file_name'] = 'cleaned_data.txt'
para_dict['input']['feature_choice_str'] = '0,1,3,4,5,6,7,8,9,10,11,12,13,14,15'

#-------------------------------------------------switch bit------operator_bit------valuebit
# -------
# eg. (4,11,1), bit 4 is a sign bit
#  on/off bit    operator_bits     sign_bit     int_value_bits      decimal_bits
# (1,            2,                1,           4,                  7             )
para_dict['input']['data_pos_in_chromosome'][8] = (1, 2, 1, 4, 4) #0
para_dict['input']['data_pos_in_chromosome'][9] = (1, 2, 1, 9, 1) #1
para_dict['input']['data_pos_in_chromosome'][14] = (1, 2, 0, 8, 0) #2
para_dict['input']['data_pos_in_chromosome'][15] = (1, 2, 0, 2, 4) #3
#
para_dict['input']['feature_decide_bit_len'] = 3

para_dict['input']['restrict_training_date'] = True
para_dict['input']['training_date_start'] = '1/14/2011'
para_dict['input']['training_date_end'] = '3/25/2011'
para_dict['input']['training_testing_ratio'] = '8,2'
# determine the decisive feature
#  buy/sell difference indicator,    feature index
# (1,                                8)
para_dict['input']['decisive_feature'] = (1,8)



#0  1            2                3            4           5            6          7             8            9              10
#_, USD_JPY,     01/03/2016,      -0.17,       0.46,       -0.93,       -0.84,     100140,       26.29,       1.6,           80023895,
#    11        12          13     14        15
# $16.81,    $16.58,   -1.36823,  76,    0.179856
para_dict['input']['raw_data_dict'] = {
                                        0:'_',
                                        1:'instrument',
                                        2:'time',
                                        3:'openMid_1_day_percent',
                                        4:'highMid_1_day_percent',
                                        5:'lowMid_percent',
                                        6:'closeMid_1_day_percent',
                                        7:'volume',
                                        8:'volume_1_day_percent',
                                        9:'openMid_3_day_std',
                                        10:'openMid_7_day_std',
                                        11:'volume_3_day_std',
                                        12:'volume_7_day_std',
                                        13:'real_body_percent',
                                        14:'upper_shadow_percent',
                                        15:'lower_shadow_percent',
                                        16:'profit_1_day',
                                        17:'profit_3_day',
                                        18:'profit_7_day',
                                        }
para_dict['input']['next_price_str'] = 'percent_change_next_weeks_price'
#==========================================================INPUT END==================================================================


# evolution
para_dict['evolution']['mutation']['flip_bit_num'] = 3
para_dict['evolution']['mutation']['mode'] = 'random_flip'
# cross_over, mode = 'uniform', 'multi_point', 'one_point'
para_dict['evolution']['cross_over']['mode'] = 'uniform'



# SGA
para_dict['SGA']['max_population_num'] = 60
# mode: TS-Tournament Selection, RWS-Roulette Wheel Selection, SUS-Stochastic Universal Sampling, RK-Rank Selection
para_dict['SGA']['parent_select_mode'] = 'TS'
para_dict['SGA']['TS']['TS_K'] = 3
para_dict['SGA']['intial_solution_number'] = 30
para_dict['SGA']['target_return_percent'] = 75
para_dict['SGA']['no_progress_generation'] = 50
para_dict['SGA']['buy_sell_switch'] = 1
para_dict['SGA']['multiple_return_switch'] = 0



#DSGA
# mutation rate 0.5 -> 50%
para_dict['DSGA']['M'] = 0.5
# seed radius >>> 1/11 = 0.09090909090909091, max 1
para_dict['DSGA']['IS'] = 0.095
# radius delta
para_dict['DSGA']['SD'] = 0.005
# reevalution loop count
para_dict['DSGA']['RLC'] = 1
# TODO convergence limit, is it >= or >
para_dict['DSGA']['CL'] = 4
para_dict['DSGA']['Parent_Choose'] = 'f'
para_dict['DSGA']['seed_max_ratio'] = 0.6
para_dict['DSGA']['eliminate_ratio'] = 0.25



#testing
para_dict['testing']['raw_data_file_path'] = ''

with open('oanda_parameter.json', 'w', encoding = 'utf-8') as f:
  json.dump(para_dict, f, ensure_ascii = False, indent = 4)
