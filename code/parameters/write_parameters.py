import collections
import json



para_dict = collections.defaultdict(lambda: collections.defaultdict(lambda:{}))
para_dict['input']['raw_data_path'] = ''
para_dict['input']['raw_data_file_name'] = 'cleaned_data.txt'
para_dict['input']['feature_choice_str'] = '0,1,3,4,5,6,7,8,9,10,11,12,13,14,15'
#testing
para_dict['testing']['raw_data_file_path'] = ''

#-------------------------------------------------switch bit------operator_bit------valuebit
# -------
# eg. (4,11,1), bit 4 is a sign bit
#  on/off bit    operator_bits     sign_bit     int_value_bits      decimal_bits
# (1,            2,                1,           4,                  7)
para_dict['input']['data_pos_in_chromosome'][8] = (1, 2, 1, 4, 7)
para_dict['input']['data_pos_in_chromosome'][9] = (1, 2, 1, 9, 4)
para_dict['input']['data_pos_in_chromosome'][14] = (1, 2, 0, 8, 0)
para_dict['input']['data_pos_in_chromosome'][15] = (1, 2, 0, 2, 10)


para_dict['input']['restrict_training_date'] = True
para_dict['input']['training_date_start'] = '1/14/2011'
para_dict['input']['training_date_end'] = '3/25/2011'
para_dict['input']['training_testing_ratio'] = '8,2'
# determine the decisive feature
#  buy/sell difference indicator,    feature index
# (1,                                8)
para_dict['input']['decisive_feature'] = (1,8)

#0  1       2             3      4            5        6           7          8            9           10
#1, AA,   2/25/2011,   $16.98   ,$17.15,   $15.96,   $16.68,   132981863,  -1.76678,  66.17769355,  80023895,
#    11        12          13     14        15
# $16.81,    $16.58,   -1.36823,  76,    0.179856
para_dict['input']['raw_data_dict'] = {
                                        0:'quarter',
                                        1:'stock',
                                        2:'date',
                                        3:'open',
                                        4:'high',
                                        5:'low',
                                        6:'close',
                                        7:'volume',
                                        8:'percent_change_price',
                                        9:'percent_change_volume_over_last_wek',
                                        10:'previous_weeks_volume',
                                        11:'next_weeks_open',
                                        12:'next_weeks_close',
                                        13:'percent_change_next_weeks_price',
                                        14:'days_to_next_dividend',
                                        15:'percent_return_next_dividend',
                                        }
para_dict['input']['next_price_str'] = 'percent_change_next_weeks_price'
para_dict['evolution']['mutation']['flip_bit_num'] = 3
para_dict['evolution']['mutation']['mode'] = 'random_flip'
# cross_over, mode = 'uniform', 'multi_point', 'one_point'
para_dict['evolution']['cross_over']['mode'] = 'uniform'
para_dict['SGA']['max_population_num'] = 60
#para_dict['SGA']['kept_population_num'] = 5
# mode: TS-Tournament Selection, RWS-Roulette Wheel Selection, SUS-Stochastic Universal Sampling, RK-Rank Selection
para_dict['SGA']['parent_select_mode'] = 'TS'
para_dict['SGA']['TS']['TS_K'] = 3
para_dict['SGA']['intial_solution_number'] = 30
para_dict['SGA']['target_return_percent'] = 5
para_dict['SGA']['no_progress_generation'] = 10
para_dict['SGA']['buy_sell_switch'] = 1

#DSGA
# mutation rate 0.5 -> 50%
para_dict['DSGA']['M'] = 1
# seed radius >>> 1/11 = 0.09090909090909091, max 1
para_dict['DSGA']['IS'] = 0.095
# radius delta
para_dict['DSGA']['SD'] = 0.01
# reevalution loop count
para_dict['DSGA']['RLC'] = 1
# convergence limit
para_dict['DSGA']['CL'] = 5
para_dict['DSGA']['seed_max_ratio'] = 0.6
para_dict['DSGA']['eliminate_ratio'] = 0.25

with open('parameter.json', 'w') as f:
  json.dump(para_dict, f, ensure_ascii = False, indent = 4)


#=======================================================================================================================
#=======================================================================================================================
#=====================================================TESTING===========================================================
#=======================================================================================================================
#=======================================================================================================================
testing_para_dict = collections.defaultdict(lambda: collections.defaultdict(lambda:{}))
testing_para_dict['data_file_path'] = ''
testing_para_dict['is_single_testing_data_file'] = False
testing_para_dict['chromosome_path'] = ''

with open('testing_parameter.json', 'w') as f:
  json.dump(testing_para_dict, f, ensure_ascii = False, indent = 4)