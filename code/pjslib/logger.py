import logging
import os

def get_upper_folder_path(num, path = ''):
    if not path:
        path = os.path.dirname(os.path.abspath(__file__))
    else:
        path = os.path.dirname(path)
    num -= 1
    if num > 0:
        return get_upper_folder_path(num, path = path)
    else:
        return path

code_folder_path = get_upper_folder_path(2)







# create formatter
#=====================Formatter==================================
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#=====================Formatter==================================

#=====================Command Line===============================
# create console handler and set level to debug
ch = logging.StreamHandler()
# DEBUG, INFO, WARNING, ERROR, CRITICAL
#ch.setLevel(logging.DEBUG)
# add formatter to ch
ch.setFormatter(formatter)
#================================================================

# :::logger1
# create logger
logger1 = logging.getLogger('logger1')
# set level
logger1.setLevel(logging.ERROR)
# save to file
hdlr_1 = logging.FileHandler(os.path.join(code_folder_path, 'logging', 'logging.log'))
hdlr_1.setFormatter(formatter)
# command line
# add ch to logger

if not logger1.handlers:
    logger1.addHandler(ch)
    logger1.addHandler(hdlr_1)


# :::logger_s
# create logger
logger_s = logging.getLogger('logger_s')
# set level
logger_s.setLevel(logging.INFO)
# save to file
hdlr_s = logging.FileHandler(os.path.join(code_folder_path, 'logging', 'logging_seed.log'))
hdlr_s.setFormatter(formatter)
# command line
# add ch to logger
if not logger_s.handlers:
    logger_s.addHandler(ch)
    logger_s.addHandler(hdlr_s)







#:::logger2

# create logger
logger2 = logging.getLogger('logger2')
# set level
logger2.setLevel(logging.ERROR)
# save to file

hdlr_2 = logging.FileHandler(os.path.join(code_folder_path, 'logging', 'testing_logging.log'))
hdlr_2.setFormatter(formatter)
# command line
# add ch to logger
if not logger2.handlers:
    logger2.addHandler(ch)
    logger2.addHandler(hdlr_2)

#:::logger3

# create logger
logger3 = logging.getLogger('logger3')
# set level
logger3.setLevel(logging.INFO)
# save to file
hdlr_3 = logging.FileHandler(os.path.join(code_folder_path, 'testing', 'code_testing_logging.log'))
hdlr_3.setFormatter(formatter)
# command line
# add ch to logger
if not logger3.handlers:
    logger3.addHandler(ch)
    logger3.addHandler(hdlr_3)


# create logger
logger_t = logging.getLogger('logger_temp')
# set level
logger_t.setLevel(logging.INFO)
# save to file

hdlr_t = logging.FileHandler(os.path.join(code_folder_path, 'logging', 'temp_logging.log'))
hdlr_t.setFormatter(formatter)
# command line
# add ch to logger
if not logger_t.handlers:
    logger_t.addHandler(ch)
    logger_t.addHandler(hdlr_t)

# create logger
logger_bg = logging.getLogger('logger_bg')
# set level
logger_bg.setLevel(logging.INFO)
# save to file
hdlr_bg = logging.FileHandler(os.path.join(code_folder_path, 'logging', 'bg_logging.log'))
hdlr_bg.setFormatter(formatter)
# command line
# add ch to logger
if not logger_bg.handlers:
    logger_bg.addHandler(ch)
    logger_bg.addHandler(hdlr_bg)
    logger_bg.progagate = False

# # =========================================
# # create logger
# oanda_logger = logging.getLogger('oanda_logger')
# # set level
# oanda_logger.setLevel(logging.INFO)
# # save to file
# hdlr_1 = logging.FileHandler('logging/oanda_logging.log')
# hdlr_1.setFormatter(formatter)
# # command line
# # add ch to logger
# oanda_logger.addHandler(ch)
# oanda_logger.addHandler(hdlr_1)