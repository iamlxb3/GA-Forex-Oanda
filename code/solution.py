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
        self.shard_fitness = 0.0
        self.m_i = 0.0
        self.isSeed = False
        self.classification_result_list = []
        self.name = self.__class__.name_id
        self.__class__.name_id += 1
        self.__class__._all.append(self)

    @classmethod
    def all(cls):
        return cls._all

    @classmethod
    def _clear(cls):
        cls._all = []

    @classmethod
    def compute_fitness(cls):
        all_solutions = cls._all

    def compute_distance(self, solution1, solution2):
        same_results_set = set(solution1.classification_result_list) & set(solution2.classification_result_list)
        distance = 1/same_results_set
        return distance


    def get_classification_result(self):
        pass

    def compute_m_i(self, tabu_list):
        pass



    def __str__(self):
        return self.name
