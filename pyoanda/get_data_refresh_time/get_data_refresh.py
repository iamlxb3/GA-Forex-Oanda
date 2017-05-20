import requests
import time
import datetime
import re
import sys
import schedule

previous_date = None
now_date = None



def get_data_refresh():
    url = "https://api-fxtrade.oanda.com/v1/candles?instrument=EUR_USD&"\
          "count=1&candleFormat=midpoint&granularity=D&"\
          "dailyAlignment=0&alignmentTimezone=America%2FNew_York"
    response = requests.get(url)
    response_status_code = response.status_code
    print("response_status_code: ", response_status_code)
    day_forex_dict = dict(response.json())['candles'][0]
    time1 = day_forex_dict['time']
    date = re.findall(r'[0-9]+-[0-9]+-[0-9]+', time1)[0]

    date_object_temp = time.strptime(date, '%Y-%m-%d')
    date_object = datetime.datetime(*date_object_temp[:3]).date()
    #print("time: ", time)
    #print ("date: ", date)
    print("date_obejct: ", date_object)
    return date_object

def get_shift_time(previous_date):
    time_now = datetime.datetime.today()
    print ("time now: ", time_now)
    now_date = get_data_refresh()
    if previous_date is None:
        previous_date = now_date
    print("now_date: ", now_date)
    print("previous_date: ", previous_date)
    if previous_date != now_date:
        print ("shifting time: {}".format(time_now))
        sys.exit(0)


schedule.every(60).seconds.do(get_shift_time, previous_date)
#schedule.every().day.at("11:52").do(get_shift_time, previous_date)


while 1:
    schedule.run_pending()
