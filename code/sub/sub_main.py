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
        
        
# create path for python folder and files 
# (1.) formatter
code_main_folder = find_upper_level_folder_path(2)
formatter__path = os.path.join(code_main_folder, 'formatter.py')
main__path = os.path.join(code_main_folder, 'main.py')




#:::RUN:::
#(1.) formatter
run_python(main__path)




