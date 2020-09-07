# Import modules
import json
import requests
import numpy as np
import pandas as pd
import tweepy
import math
import time
from datetime import datetime
def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper
# ######### FIRST PASS ##############
# Authenticate to Twitter
auth = tweepy.OAuthHandler("5ihGZy9Us9HFMB8ygBi6JmYcX", "keccPYMyGJUNRqZ6I94OnMRjDedk0v1m8tJqHgDs0pR9Pu7jLL")
auth.set_access_token("1293770516147441665-lwWaRBCCFGm06FDEcTyh6CLJEobKCd", "U4RrZcLwtYi1PNUkTbcoyWq02YskivgOhk3Db8BCSWPMH")
# Create API object
api = tweepy.API(auth)
# Pull in market data from PredictIt's API
URL = "https://www.predictit.org/api/marketdata/all/"
response = requests.get(URL)
jsondata = response.json()
# Replace null values with zero
def dict_clean(items):
    result = {}
    for key, value in items:
        if value is None:
            value = 0
        result[key] = value
        return result
        dict_str = json.dumps(jsondata)
        jsondata = json.loads(dict_str, object_pairs_hook=dict_clean)
        # Market data by contract/price in dataframe
        data = []
        market_count = 0;
        for p in jsondata['markets']:
            market_count = market_count + 1
            for k in p['contracts']:
                data.append([p['id'], p['name'], p['url'], k['id'], k['name'], k['bestBuyYesCost'], k['bestBuyNoCost'],
                             k['bestSellYesCost'], k['bestSellNoCost'], p['timeStamp'], p[$
                # Pandas dataframe named 'df'
                df = pd.DataFrame(data)
                # Update dataframe column names
                df.columns = ['Market_ID', 'Market_Name', 'Market_URL', 'Contract_ID', 'Contract_Name',
                              'bestBuyYesCost', 'bestBuyNoCost', 'BestSellYesCost', 'BestSellNoCost', 'Time_Stamp', '$
