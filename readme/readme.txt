*Read Me*
How to train and test on the forex data
*Read Me*

# =========================================================================================================================
【0.] download the testing/trading data  4
# =========================================================================================================================
【PYTHON】 C:\Users\JIASHU\Desktop\forex_main\pyoanda\read_history_forex_data.py
"""
parameter_dict['mode'] = 'testing'  |  parameter_dict['mode'] = 'trading'
"""
modify how many days to download: "C:\Users\JIASHU\Desktop\forex_main\pyoanda\parameters", set ["date_range": 1000,]
modify the GA parameters in "C:\Users\JIASHU\Desktop\forex_main\code\main.py"
# =========================================================================================================================


# =========================================================================================================================
[1.0] training
# =========================================================================================================================
[PYTHON] C:\Users\JIASHU\Desktop\forex_main\pyoanda\sub\oanda_sub.py -m train
"""
parameter_dict['input']['training_date_start'] = '03/19/2014' # split date for training and testing
parameter_dict['input']['training_date_end'] = '08/02/2016' # split date for training and testing
parameter_dict['SGA']['buy_sell_switch'] = 0 # when training, set to train buy or sell
parameter_dict['input']['next_price_str'] = 'profit_3_day' # set the profit indicator
"""
The chromosome will be saved to "C:\Users\JIASHU\Desktop\forex_main\code\chromosome"
# =========================================================================================================================


# =========================================================================================================================
1.5 write_conserved_chromosome
# =========================================================================================================================
[PYTHON] C:\Users\JIASHU\Desktop\forex_main\code\chromosome\write_conserved_chromosome.py

convert "conserved_best_chromosome.txt" into "c_buy_chromosome.txt" and "c_sell_chromosome.txt" for testing, be ready for 
examining all conseverd chromosome.
# =========================================================================================================================


# =========================================================================================================================
[2.0] testing
# =========================================================================================================================
[PYTHON] C:\Users\JIASHU\Desktop\forex_main\pyoanda\sub\oanda_sub.py -m test
"""
parameter_dict['input']['training_date_start'] = '03/19/2014' # split date for training and testing
parameter_dict['input']['training_date_end'] = '08/02/2016' # split date for training and testing
parameter_dict['input']['next_price_str'] = 'profit_3_day' # set the profit indicator
"""

The output will be save to "C:\Users\JIASHU\Desktop\forex_main\code\test_data_result"
Manually check the result, the good ones should be added to "conserved_best_chromosome.txt", and the best should go into 
"C:\Users\JIASHU\Desktop\forex_main\pyoanda\chromosome_strategy_chosen.txt"
# =========================================================================================================================



