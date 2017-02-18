import logging

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


# create logger
logger1 = logging.getLogger('logger1')
# set level
logger1.setLevel(logging.ERROR)
# save to file
hdlr_1 = logging.FileHandler('logging.log')
hdlr_1.setFormatter(formatter)
# command line
# add ch to logger
logger1.addHandler(ch)
logger1.addHandler(hdlr_1)


#:::logger2

# create logger
logger2 = logging.getLogger('logger2')
# set level
logger2.setLevel(logging.INFO)
# save to file
hdlr_2 = logging.FileHandler('testing_logging.log')
hdlr_2.setFormatter(formatter)
# command line
# add ch to logger
logger2.addHandler(ch)
logger2.addHandler(hdlr_2)

#:::logger3

# create logger
logger3 = logging.getLogger('logger3')
# set level
logger3.setLevel(logging.INFO)
# save to file
hdlr_3 = logging.FileHandler('testing/code_testing_logging.log')
hdlr_3.setFormatter(formatter)
# command line
# add ch to logger
logger3.addHandler(ch)
logger3.addHandler(hdlr_3)


# create logger
logger_t = logging.getLogger('logger_temp')
# set level
logger_t.setLevel(logging.INFO)
# save to file
hdlr_t = logging.FileHandler('temp_logging.log')
hdlr_t.setFormatter(formatter)
# command line
# add ch to logger
logger_t.addHandler(ch)
logger_t.addHandler(hdlr_t)