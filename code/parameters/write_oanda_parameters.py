import collections
import json


#==========================================================INPUT=====================================================================
para_dict = collections.defaultdict(lambda: collections.defaultdict(lambda:{}))
para_dict['input']['raw_data_path'] = ''
para_dict['input']['raw_data_file_name'] = 'cleaned_data.txt'
para_dict['input']['feature_choice_str'] = '0,1,3,4,5,6,7,8,13,14,15,16,17,18'

#-------------------------------------------------switch bit------operator_bit------valuebit
# -------
# eg. (4,11,1), bit 4 is a sign bit
#  on/off bit    operator_bits     sign_bit     int_value_bits      decimal_bits
# (1,            2,                1,           4,                  7             )
para_dict['input']['data_pos_in_chromosome'][3] = (1, 2, 1, 3, 4) #0
para_dict['input']['data_pos_in_chromosome'][4] = (1, 2, 1, 3, 4) #1
para_dict['input']['data_pos_in_chromosome'][5] = (1, 2, 1, 3, 4) #1
para_dict['input']['data_pos_in_chromosome'][6] = (1, 2, 1, 3, 4) #1
para_dict['input']['data_pos_in_chromosome'][7] = (1, 2, 0, 14, 0) #1
para_dict['input']['data_pos_in_chromosome'][8] = (1, 2, 1, 11, 0) #1
para_dict['input']['data_pos_in_chromosome'][13] = (1, 2, 0, 6, 0) #1
para_dict['input']['data_pos_in_chromosome'][14] = (1, 2, 0, 6, 0) #1
para_dict['input']['data_pos_in_chromosome'][15] = (1, 2, 0, 6, 0) #1
#
para_dict['input']['feature_decide_bit_len'] = 4

para_dict['input']['restrict_training_date'] = True
para_dict['input']['training_date_start'] = '12/16/2015'
para_dict['input']['training_date_end'] = '11/30/2016'
para_dict['input']['training_testing_ratio'] = '8,2'
# determine the decisive feature
#  buy/sell difference indicator,    feature index
# (1,                                8)
para_dict['input']['decisive_feature'] = (1,3) # openMid_1_day_percent

# square: 0.5, bit:1
# square: 0.25, bit:2
# square: 0.125, bit:3
# square: 0.0625, bit:4
# square: 0.03125, bit:5
# square: 0.015625, bit:6
# square: 0.0078125, bit:7
# square: 0.00390625, bit:8
# square: 0.001953125, bit:9
# square: 0.0009765625, bit:10
# square: 0.00048828125, bit:11

# Feature_id: 3, max: 4.05, min: -10.05, pos_average: 0.4105023255813955, neg_average: -0.45996062992125997, zero_num: 15
# Feature_id: 4, max: 2.66, min: -7.42, pos_average: 0.3946853823814128, neg_average: -0.4124857142857142, zero_num: 23
# Feature_id: 5, max: 4.73, min: -10.05, pos_average: 0.38531738730450776, neg_average: -0.4475656565656561, zero_num: 29
# Feature_id: 6, max: 4.05, min: -10.04, pos_average: 0.4163678804855276, neg_average: -0.4639881539980254, zero_num: 22
# Feature_id: 7, max: 312154.0, min: 639.0, pos_average: 48710.65337132004, neg_average: 0, zero_num: 0
# Feature_id: 8, max: 95.22, min: -1791.94, pos_average: 38.58408752327748, neg_average: -177.91140503875943, zero_num: 0
# Feature_id: 9, max: 64.3, min: 0.1, pos_average: 3.5269230769230706, neg_average: 0, zero_num: 0
# Feature_id: 10, max: 65.5, min: 0.6, pos_average: 6.154890788224129, neg_average: 0, zero_num: 0
# Feature_id: 11, max: 110.1, min: 0.1, pos_average: 15.125593542260162, neg_average: 0, zero_num: 0
# Feature_id: 12, max: 91.2, min: 1.4, pos_average: 20.452089268755888, neg_average: 0, zero_num: 0
# Feature_id: 13, max: 98.91, min: 0.0, pos_average: 44.876269011406826, neg_average: 0, zero_num: 2
# Feature_id: 14, max: 100.0, min: 0.0, pos_average: 51.049618138424805, neg_average: 0, zero_num: 11
# Feature_id: 15, max: 99.8, min: 0.12, pos_average: 50.65399335232673, neg_average: 0, zero_num: 0
# Feature_id: 16, max: 4.222, min: -9.121, pos_average: 0.4151554116558747, neg_average: -0.45473802541544467, zero_num: 2
# Feature_id: 17, max: 5.328, min: -9.409, pos_average: 0.7411826831588963, neg_average: -0.7857015209125475, zero_num: 3
# Feature_id: 18, max: 7.644, min: -9.903, pos_average: 1.153781609195401, neg_average: -1.2432858490566057, zero_num: 2


para_dict['input']['raw_data_dict'] = {
                                        0:'Blank',
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
para_dict['input']['next_price_str'] = 'profit_1_day'
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
para_dict['SGA']['target_return_percent'] = 40
para_dict['SGA']['no_progress_generation'] = 200
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

with open('parameter.json', 'w', encoding = 'utf-8') as f:
  json.dump(para_dict, f, ensure_ascii = False, indent = 4)
