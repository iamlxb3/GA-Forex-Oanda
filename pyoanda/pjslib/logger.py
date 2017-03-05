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
oanda_logger = logging.getLogger('oanda_logger')
# set level
oanda_logger.setLevel(logging.INFO)
# save to file
hdlr_1 = logging.FileHandler('logging/oanda_logging.log')
hdlr_1.setFormatter(formatter)
# command line
# add ch to logger
oanda_logger.addHandler(ch)
oanda_logger.addHandler(hdlr_1)

# create logger
strategy_logger = logging.getLogger('strategy_logger')
# set level
strategy_logger.setLevel(logging.INFO)
# save to file
hdlr_2 = logging.FileHandler('logging/strategy_logging.log')
hdlr_2.setFormatter(formatter)
# command line
# add ch to logger
strategy_logger.addHandler(ch)
strategy_logger.addHandler(hdlr_2)

