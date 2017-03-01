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
       
# import subprocess
import os
import sys
import subprocess

def run_python(path):
    cwd = os.path.dirname(os.path.realpath(path))
    subprocess.call("python {}".format(path), shell=True, cwd = cwd)
        
        
# run AM-stock GA
# (1.) get AM-stock GA main path
code_main_folder = find_upper_level_folder_path(2)
AM_S_main__path = os.path.join(code_main_folder, 'main.py')
AM_S_main_w_parameter__path = os.path.join(code_main_folder, 'parameters', 'write_parameters.py')


#:::RUN:::
# (1.) write the AM-stock GA into json
run_python(AM_S_main_w_parameter__path)
# (2.) run AM-stock GA
run_python(AM_S_main__path)




