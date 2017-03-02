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

import os
import json

class SubReader():
    def __init__(self, path = ''):
        if not path:
            current_folder_path = find_upper_level_folder_path(1)
            path = os.path.join(current_folder_path, 'parameters', 'parameter.json')
        self.path = path
       
    def read_parameters(self, path):
        with open(path, 'r', encoding = 'utf-8') as f:
            parameter_dict = json.load(f)
        return parameter_dict
        
    def write_json(self, path, dict):
        with open(path, 'w') as f:
          json.dump(dict, f, ensure_ascii = False, indent = 4)

