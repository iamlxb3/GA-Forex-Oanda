# ==================================================================
def find_upper_level_folder_path(num, path = ''):
    if not path:
        path = os.path.dirname(os.path.abspath(__file__))
    else:
        path = os.path.dirname(path)
    num -= 1
    if num > 0:
        return find_upper_level_folder_path(num, path = path)
    else:
        return path
# ==================================================================
       
# import subprocess
import os
import sys
import getopt
import subprocess
from sub_reader import SubReader
from sub_cmd import sub_cmd


def run_python(path):
    cwd = os.path.dirname(os.path.realpath(path))
    subprocess.call("python {}".format(path), shell=True, cwd = cwd)
        

# GET PATH
# (1.) get AM-stock GA main path (training)
code_main_folder = find_upper_level_folder_path(2)
AM_S_main__path = os.path.join(code_main_folder, 'main.py')
AM_S_main_w_parameter__path = os.path.join(code_main_folder, 'parameters', 'write_parameters.py')
AM_S_main_parameter_json__path = os.path.join(code_main_folder, 'parameters', 'parameter.json')
# (2.) get AM-stock GA testing path
AM_S_testing_path = os.path.join(code_main_folder, 'ga_testing.py')
# (3.) get data_path
data_parent_folder_path = find_upper_level_folder_path(3)
AM_S_data_path = os.path.join(data_parent_folder_path, 'data', 'cleaned_data.txt')
# =====================================================================================================



#:::RUN:::
# (0.) sub_cmd get the train/test 
is_test, is_train = sub_cmd()

# (1.) write the AM-stock GA into json
run_python(AM_S_main_w_parameter__path)

# (2.) adjust parameters and write new json file
sub_reader = SubReader()
parameter_dict = sub_reader.read_parameters(AM_S_main_parameter_json__path)
parameter_dict['input']['raw_data_path'] = AM_S_data_path
sub_reader.write_json(AM_S_main_parameter_json__path, parameter_dict)

# (3.) run AM-stock GA
if is_test:
    run_python(AM_S_main__path)
elif is_train:
    run_python(AM_S_testing_path)




