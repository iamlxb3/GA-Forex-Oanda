# import from pjslib
from pjslib.general import get_upper_folder_path
from pjslib.general import accepts
from pjslib.logger import logger1
#================================================
import os
import sys





class Solution():
    name_id = 0
    def __init__(self):
        self.chromosome_bits = []
        self.fitness = 0.0
        self.isSeed = False
        self.name = self.__class__.name_id
        self.__class__.name_id += 1

    def __str__(self):
        return self.name
