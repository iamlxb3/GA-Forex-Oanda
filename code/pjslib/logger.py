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
