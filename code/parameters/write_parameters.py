import collections
import json



para_dict = collections.defaultdict(lambda: collections.defaultdict(lambda:{}))
para_dict['input']['raw_data_path'] = ''
para_dict['input']['raw_data_file_name'] = 'cleaned_data.txt'
para_dict['input']['feature_choice_str'] = '0,1,3,4,5,6,7,8,9,10,11,12,13,14,15'

#-------------------------------------------------switch bit------operator_bit------valuebit
# -------
# eg. (4,11,1), bit 4 is a sign bit
#  on/off bit    operator_bits     sign_bit     int_value_bits      decimal_bits
# (1,            2,               (1,           4,                  7))
para_dict['input']['data_pos_in_chromosome'][8] = (1, 2, (1, 4, 7))
para_dict['input']['data_pos_in_chromosome'][9] = (1, 2, (1, 8, 4))
para_dict['input']['data_pos_in_chromosome'][14] = (1, 2, (0, 7, 0))
para_dict['input']['data_pos_in_chromosome'][15] = (1, 2, (0, 2, 10))
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
para_dict['evolution']['mutation']['flip_bit_num'] = 1
para_dict['evolution']['mutation']['mode'] = 'random_flip'
# cross_over, mode = 'uniform', 'multi_point', 'one_point'
para_dict['evolution']['cross_over']['mode'] = 'uniform'
para_dict['SGA']['max_population_num'] = 9
#para_dict['SGA']['kept_population_num'] = 5
# mode: TS-Tournament Selection, RWS-Roulette Wheel Selection, SUS-Stochastic Universal Sampling, RK-Rank Selection
para_dict['SGA']['parent_select_mode'] = 'TS'
para_dict['SGA']['TS']['TS_K'] = 3



with open('parameter.json', 'w') as f:
  json.dump(para_dict, f, ensure_ascii = False, indent = 4)
