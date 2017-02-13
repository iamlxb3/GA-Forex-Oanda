# import from pjslib
from pjslib.general import get_upper_folder_path
from pjslib.general import accepts
from pjslib.logger import logger1
#================================================
import os
import sys





class Solution():
    name_id = 0
    _all = []
    def __init__(self):
        self.chromosome_bits = []
        self.fitness = 0.0
        self.is_f_computed = False
        self.isSeed = False
        self.name = self.__class__.name_id
        self.__class__.name_id += 1
        self.__class__._all.append(self)

    @classmethod
    def all(cls):
        return cls._all

    @classmethod
    def _clear(cls):
        cls._all = []

    def __str__(self):
        return self.name
