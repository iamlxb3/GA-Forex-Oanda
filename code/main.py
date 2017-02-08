# import from pjslib
from pjslib.general import get_upper_folder_path
from pjslib.general import accepts
from pjslib.logger import logger1
#================================================


from read_parameters import ReadParameters
from formatter import Formatter



# (1.) read parameters
reader1 = ReadParameters()
parameter_dict = reader1.read_parameters(reader1.path)
logger1.info("read parameters successful")
# (2.) put data into dict
formatter1 = Formatter(parameter_dict)
input_data_dict = formatter1.format_and_create_dict(formatter1.path, formatter1.feature_choice_list)
logger1.info("create input_data_dict successful")

