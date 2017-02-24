#============================================================
# import from pjslib
from pjslib.general import get_upper_folder_path
from pjslib.general import accepts
from pjslib.logger import oanda_logger
#================================================
import os
import requests
import collections
import re
from read_parameters import ReadParameters




class ReadForexData:
    """read the up-to-date forex data via oanda API"""
    def __init__(self, parameters_dict):
        self.mode = parameters_dict['mode']
        self.instruments_list = ['EUR_USD', 'USD_JPY', 'USD_CAD', 'GBP_USD', 'USD_CHF','AUD_USD']
        self.granularity = parameters_dict['granularity']
        self.candle_format = parameters_dict['candle_format']
        self.date_range = parameters_dict['date_range']
        self.url = "https://api-fxtrade.oanda.com/v1/candles?" \
                   "instrument=#instrument&" \
                   "count={date_range}&" \
                   "candleFormat={candle_format}&" \
                   "granularity={granularity}&" \
                   "dailyAlignment=0&" \
                   "alignmentTimezone=America%2FNew_York".format(date_range = self.date_range,
                                                                 candle_format = self.candle_format,
                                                                 granularity = self.granularity)
        # set the data output path
        parent_folder = os.path.join(get_upper_folder_path(2), 'data')
        data_folder = os.path.join(parent_folder, 'oanda')
        if self.mode == 'testing':
            self.file_path = os.path.join(data_folder, 'oanda_forex_testing_data.txt')
        elif self.mode == 'trading':
            self.file_path = os.path.join(data_folder, 'oanda_forex_trading_data.txt')
        self.forex_data_dict = collections.defaultdict(lambda :[])

    def write_forex_dict_to_file(self):
        path = self.file_path
        #self.forex_data_dict : {'EUR_USD':[('AUD_USD', '2014-9-9', 0.77157, 0.772, 0.767955, 0.76851, 0.76, 0.11, 0.14), ...]}
        with open (path, 'w', encoding = 'utf-8') as f:
            for instrument, days_feature_list in self.forex_data_dict.items():
                for day_features in days_feature_list:
                    day_features = [str(x) for x in day_features]
                    feature_str = ','.join(day_features)
                    f.write(feature_str)
                    f.write('\n')


    def format_forex_data_file_into_new_feature(self):
        # TODO
        pass

    def read_onanda_data(self):
        '''read oanda data via online api to dict with several features'''
        for instrument in self.instruments_list:
            url = self.url.replace("#instrument", instrument)
            response = requests.get(url)
            response_status_code = response.status_code
            print("response_status_code: ", response_status_code)
            day_forex_list = dict(response.json())['candles']

            for day_forex_dict in day_forex_list:
                time = day_forex_dict['time']
                time = re.findall(r'([0-9]+-[0-9]+-[0-9]+)', time)[0]
                openMid = day_forex_dict['openMid']
                highMid = day_forex_dict['highMid']
                lowMid = day_forex_dict['lowMid']
                closeMid = day_forex_dict['closeMid']
                volume = day_forex_dict['volume']
                # custom feature
                real_body_percent = float("{:.2f}".format(abs((openMid - closeMid) / (highMid - lowMid))))
                upper_shadow_percent = float("{:.2f}".format(abs((highMid - openMid) / (highMid - lowMid))))
                lower_shadow_percent = float("{:.2f}".format(abs((closeMid - lowMid) / (highMid - lowMid))))
                day_forex_tuple = (instrument, time, openMid, highMid, lowMid, closeMid,
                                   real_body_percent, upper_shadow_percent, lower_shadow_percent)
                self.forex_data_dict[instrument].append(day_forex_tuple)



