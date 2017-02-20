import collections
import json

# parameters_dict for trading
# ======================================================================================
t_parameters_dict = collections.defaultdict(lambda: collections.defaultdict(lambda:{}))
# trading
t_parameters_dict['trading']['order']['default_stop_loss'] = 500 #500 small pips
t_parameters_dict['trading']['order']['default_stop_profit'] = 5000 #5000 small pips
t_parameters_dict['trading']['order']['timeInForce'] = 'GTC' 
t_parameters_dict['trading']['order']['type'] = 'LIMIT'
t_parameters_dict['trading']['order']['postion_fill'] = 'DEFAULT'
t_parameters_dict['trading']['strategy']['is_1_day_include'] = True
t_parameters_dict['trading']['strategy']['is_3_day_include'] = True
t_parameters_dict['trading']['strategy']['is_5_day_include'] = False


# general
t_parameters_dict['general']['refresh_time'] = 15 #15 mins

# data
t_parameters_dict['data']['path'] = ''
# ======================================================================================
# parameters_dict for processing data 


#curl -X GET "https://api-fxtrade.oanda.com/v1/candles?instrument=EUR_USD&count=2&candleFormat=midpoint&granularity=D&dailyAlignment=0&alignmentTimezone=America%2FNew_York"


# data
p_data_parameters_dict['data_path'] = ''
p_data_parameters_dict['mode'] = 'testing' # testing, trading
p_data_parameters_dict['start_date'] = ''
p_data_parameters_dict['end_date'] = ''
p_data_parameters_dict['instruments'] = ['USD_CAD']
p_data_parameters_dict['canleFormat'] = 'midpoint'
p_data_parameters_dict['granularity'] = 'D'
p_data_parameters_dict['alignmentTimezone'] = 'America'

# writing to json
with open('trading_parameter.json', 'w') as f:
  json.dump(parameters_dict, f, ensure_ascii = False, indent = 4)

