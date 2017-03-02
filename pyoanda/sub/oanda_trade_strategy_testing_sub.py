def find_upper_level_folder_path(num, path=''):
    if not path:
        path = os.path.dirname(os.path.abspath(__file__))
    else:
        path = os.path.dirname(path)
    num -= 1
    if num > 0:
        return find_upper_level_folder_path(num, path=path)
    else:
        return path


# import subprocess
import os
import sys
import re
import subprocess
import collections


def run_python(path):
    cwd = os.path.dirname(os.path.realpath(path))
    subprocess.call("python {}".format(path), shell=True, cwd=cwd)


pyoanda_path = find_upper_level_folder_path(2)
chosen_chromosome_path = os.path.join(pyoanda_path, 'best_chromosome', 'chosen_chromosome.txt')
chosen_chromosome_dict = collections.defaultdict(lambda:[])
# chromosome_combo_list = [(1_c1, 3_c1, 7_c1), (1_c2, 3_c2, 7_c2), ...]
chromosome_combo_list = []
chromosome_in_use_list = [(True, True, True), (True, True, False), (True, False, True),
                          (False, True, True), (True, False, False), (False, True, False),
                          (False, False, True)
                          ]
# read the chosen chromosome of 1,3,7 days
with open(chosen_chromosome_path, 'r', encoding = 'utf-8') as f:
    for line in f:
        day = re.findall(r'#([0-9]+)#', line)[0]
        chromosome = re.findall(r'#([0-9\,]+)#END#', line)[0]
        chromosome_list = chromosome.split(',')
        chosen_chromosome_dict[day].append(chromosome_list)

print (chosen_chromosome_dict)

for chromosome_1 in chosen_chromosome_dict['1']:
    for chromosome_3 in chosen_chromosome_dict['3']:
        for chromosome_7 in chosen_chromosome_dict['7']:
            chromosome_combo = (chromosome_1, chromosome_3, chromosome_7)
            print(chromosome_combo)
            chromosome_combo_list.append(chromosome_combo)

# # create path for python folder and files
# # (1.) reader
# code_read_forex_data_folder = find_upper_level_folder_path(2)
# code_read_forex_data__path = os.path.join(code_read_forex_data_folder, 'read_forex_data.py')
#
# #:::RUN:::
# # (1.) read_forex_data
# run_python(code_read_forex_data__path)



