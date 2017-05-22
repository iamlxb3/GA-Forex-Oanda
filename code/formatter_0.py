def get_upper_folder_path(num, path = ''):
    if not path:
        path = os.path.dirname(os.path.abspath(__file__))
    else:
        path = os.path.dirname(path)
    num -= 1
    if num > 0:
        return get_upper_folder_path(num, path = path)
    else:
        return path


# =================================================
import sys
import os
# import from pjslib
parent_folder = get_upper_folder_path(1)
sys.path.append(os.path.join(parent_folder, 'pjslib'))
sys.path.append(os.path.join(parent_folder))





# import from pjslib
from general import get_upper_folder_path
from general import accepts
from logger import logger1
#================================================
import os
import sys
import datetime, time
import json
import pprint
import collections
pp = pprint.PrettyPrinter(indent=4)
from collections import namedtuple, defaultdict



#print ("aaa;", os.path.dirname(__file__))






class Formatter():
    def __init__(self, parameter_dict, path = ''):
        self.parameter_dict = parameter_dict
        if not path:
            path = parameter_dict['input']['raw_data_path']
        file_name = parameter_dict['input']['raw_data_file_name']
        feature_choice_list = parameter_dict['input']['feature_choice_str'].split(',')
        
        #LOGGING
        if (not path) and (not file_name):
            logger1.error("Parameter error, no file name and path!!")
            sys.exit(0)
            
        elif not path:
            path_now = path = os.path.abspath(__file__)
            folder_path = get_upper_folder_path(2, path_now)
            folder_path = os.path.join(folder_path, 'data')
            path = os.path.join(folder_path, file_name)
            
        self.path = path
        # testing_path, if not customize file_path, assign the training path to testing path
        self.testing_file_path =parameter_dict['testing']['raw_data_file_path']
        self.testing_file_path = self.path



        self.feature_choice_list = [int(x) for x in feature_choice_list]
        self.raw_data_dict = parameter_dict['input']['raw_data_dict']
        # set a span of the training date
        self.restrict_training_date = parameter_dict['input']['restrict_training_date']
        if self.restrict_training_date:
            self.training_date_start = parameter_dict['input']['training_date_start']
            self.training_date_end = parameter_dict['input']['training_date_end']

    def compute_chosen_feature_value_range(self):

        def write_feature_pos_list_to_file(feature_value_dict):
            with open('feature_range/feature_range.txt', 'w', encoding = 'utf-8') as f:
                json.dump(feature_value_dict, f, indent = 4)

        path = self.path
        feature_value_dict = collections.defaultdict(lambda: {})
        feature_pos_list = list(self.parameter_dict['input']['data_pos_in_chromosome'].keys())
        feature_pos_list = [int(x) for x in feature_pos_list]
        feature_id_name_dict = self.parameter_dict['input']['raw_data_dict']
        for pos in feature_pos_list:
            feature_value_dict[pos]['name'] = feature_id_name_dict[str(pos)]
            feature_value_dict[pos]['value_list'] = []

        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line_list = line.strip().split(',')
                print ("line_list: ", line_list)
                for pos in feature_pos_list:
                    feature_value_dict[pos]['value_list'].append(float(line_list[pos]))

        # compute max, min, average,
        import numpy as np
        for feature, value_dict in feature_value_dict.items():
            value_list = value_dict['value_list']
            var = np.var(value_list)
            max_value = max(value_list)
            min_value = min(value_list)
            pos_value_list = [x for x in value_list if x>=0]
            neg_value_list = [x for x in value_list if x < 0]
            pos_average = 0.0
            neg_average = 0.0
            if pos_value_list:
                pos_average = sum(pos_value_list) / float(len(pos_value_list))
            if neg_value_list:
                neg_average = sum(neg_value_list) / float(len(neg_value_list))

            feature_value_dict[feature]['var'] = var
            feature_value_dict[feature]['max_value'] = max_value
            feature_value_dict[feature]['min_value'] = min_value
            feature_value_dict[feature]['pos_average'] = pos_average
            feature_value_dict[feature]['neg_average'] = neg_average
            feature_value_dict[feature].pop('value_list')




        #write_feature_pos_list_to_file
        write_feature_pos_list_to_file(feature_value_dict)


        #for pos in feature_pos_list:



        pass


    def output_dict(self, target_dict):
        pass
        
    def format_and_create_dict(self, path, feature_choice_list, testing = False):
        def create_namedtuple(raw_data_dict, feature_choice_list):
            tuple_str_list = [raw_data_dict[str(x)] + ' ' for x in feature_choice_list]
            tuple_str = ''.join(tuple_str_list)
            tuple_str = tuple_str.strip()
            Feature_namedtuple = namedtuple('Feature', tuple_str)
            return Feature_namedtuple

        # date_str: '%m/%d/%Y', '1/14/2011'
        def convert_date_str_to_date_object(date_str):
            date = time.strptime(date_str, '%m/%d/%Y')
            date = datetime.datetime(*date[:3])
            date = datetime.date(year=date.year, month=date.month, day=date.day)
            return date

        Feature_namedtuple = create_namedtuple(self.raw_data_dict, self.feature_choice_list)
        print (Feature_namedtuple._fields)
        #--------------------:::format_and_create_dict:::------------------
        if testing == True:
            path = self.testing_file_path
        # encoding back-off
        encoding = 'utf-8'
        try:
            open(path, 'r', encoding = encoding).read()
        except UnicodeDecodeError:
            encoding = 'gbk'
        #
        print ("path: ", path)
        with open(path, 'r', encoding = encoding) as f:
            input_data_dict = defaultdict(lambda: defaultdict(lambda: tuple))
            for line in f:
                try:
                    line_list = line.strip().split(',')
                    # get stock
                    stock = line_list[1]
                    # date pos is fixed to 2
                    date_str = line_list[2]
                    # convert date_str to date object
                    date = convert_date_str_to_date_object(date_str)
                    # if the date is not in the span, continue to read the next line
                    if self.restrict_training_date:
                        training_date_start = convert_date_str_to_date_object(self.training_date_start)
                        training_date_end = convert_date_str_to_date_object(self.training_date_end)
                        if testing == False:
                            if not (training_date_start <= date <= training_date_end):
                                continue
                        else:
                            if not (date > training_date_end):
                                continue
                    #
                    feature_chosen_tuple__date_key = Feature_namedtuple._make([line_list[x] for x in feature_choice_list])
                    input_data_dict[date][stock] = feature_chosen_tuple__date_key
                except UnicodeEncodeError:
                    pass
            #pp.pprint (input_data_dict)
        return input_data_dict

# formatter1 = Formatter()
# path = formatter1.path
# feature_choice_list = [x for x in range(15)]
# feature_choice_list = feature_choice_list[1:]
# formatter1.format_and_create_dict(path, feature_choice_list)
            

