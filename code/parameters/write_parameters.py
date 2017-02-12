import collections
import json



para_dict = collections.defaultdict(lambda: collections.defaultdict(lambda:{}))
para_dict['input']['raw_data_path'] = ''
para_dict['input']['raw_data_file_name'] = 'cleaned_data.txt'
para_dict['input']['feature_choice_str'] = '0,1,3,4,5,6,7,8,9,10,11,12,13,14,15'
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
                                        9:'percent_chagne_volume_over_last_wek',
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





with open('parameter.json', 'w') as f:
  json.dump(para_dict, f, ensure_ascii = False, indent = 4)
