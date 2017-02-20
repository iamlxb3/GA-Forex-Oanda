oanda_url = "https://api-fxtrade.oanda.com/v3/accounts/<ACCOUNT>/orders"


import pprint as pp
import requests
import json

from optparse import OptionParser

def connect_to_stream():
    """
    Environment           <Domain>
    fxTrade               stream-fxtrade.oanda.com
    fxTrade Practice      stream-fxpractice.oanda.com
    sandbox               stream-sandbox.oanda.com
    """

    # Replace the following variables with your personal ones
    domain = 'api-fxpractice.oanda.com'
    access_token = 'b53308ebd6ec5da20475f6e5481e3b7d-b17b9d81c15d6ec435cf875bcc41f4d9'
    account_id = '101-004-5027528-001'
    instruments = "EUR_USD"
    body =  { "order": {
    "units": "100",
    "instrument": "EUR_USD",
    "timeInForce": "FOK",
    "type": "MARKET",
    "positionFill": "DEFAULT"
     }
    }

    url = "https://" + domain + "/v3/accounts/{}/orders".format(account_id)
    headers = {
        "Content-Type": "application/json",
        'Authorization' : 'Bearer ' + access_token,
              }
    response = requests.post(url, headers = headers, json = body)
    pp.pprint("response state: {}".format(response.status_code))
    print("------------------------------------------------")
    pp.pprint(response.json())

connect_to_stream()