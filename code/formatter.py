# import from pjslib
from pjslib.general import get_upper_folder_path
from pjslib.general import accepts
from pjslib.logger import logger1
#================================================
import os
import datetime, time
import json
from collections import namedtuple, defaultdict



#print ("aaa;", os.path.dirname(__file__))






class Formatter():
    def __init__(self, parameter_dict):
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
        self.feature_choice_list = [int(x) for x in feature_choice_list]
        self.raw_data_dict = parameter_dict['input']['raw_data_dict']
        
    def output_dict(self, target_dict):
        pass
        
    def format_and_create_dict(self, path, feature_choice_list):
        def create_namedtuple(raw_data_dict, feature_choice_list):
            tuple_str_list = [raw_data_dict[str(x)] + ' ' for x in feature_choice_list]
            tuple_str = ''.join(tuple_str_list)
            tuple_str = tuple_str.strip()
            Feature_namedtuple = namedtuple('Feature', tuple_str)
            return Feature_namedtuple
    
        Feature_namedtuple = create_namedtuple(self.raw_data_dict, self.feature_choice_list)
        print (Feature_namedtuple._fields)
        #--------------------:::format_and_create_dict:::------------------
        with open(path, 'r', encoding = 'utf-8') as f:
            input_data_dict = defaultdict(lambda: defaultdict(lambda: []))
            for line in f:
                try:
                    line_list = line.strip().split(',')
                    # get stock
                    stock = line_list[1]
                    # date pos is fixed to 2
                    date_str = line_list[2]
                    # convert date_str to date object
                    date = time.strptime(date_str,'%m/%d/%Y')
                    date = datetime.datetime(*date[:3])
                    date = datetime.date(year = date.year, month = date.month, day = date.day)
                    feature_chosen_tuple__date_key = Feature_namedtuple._make([line_list[x] for x in feature_choice_list])
                    input_data_dict[date][stock].append(feature_chosen_tuple__date_key)
                except UnicodeEncodeError:
                    pass
            print (input_data_dict)
        return input_data_dict

# formatter1 = Formatter()
# path = formatter1.path
# feature_choice_list = [x for x in range(15)]
# feature_choice_list = feature_choice_list[1:]
# formatter1.format_and_create_dict(path, feature_choice_list)
            

