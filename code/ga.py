# import from pjslib
from pjslib.general import get_upper_folder_path
from pjslib.general import accepts
from pjslib.logger import logger1
#================================================
import os
import sys
import re
import collections

class GeneticAlgorithm():
    def __init__(self):
        self.result_dict = collections.defaultdict(lambda :0)