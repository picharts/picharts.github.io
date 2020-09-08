# Import modules
import json
import requests
import numpy as np
import pandas as pd
import tweepy
import math
import time
from datetime import datetime

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
        data.append([p['id'],p['name'],p['url'],k['id'],k['name'],k['bestBuyYesCost'],k['bestBuyNoCost'],k['bestSellYesCost'],k['bestSellNoCost'],p['timeStamp'],p['status']])
# Pandas dataframe named 'df'
df = pd.DataFrame(data)
# Update dataframe column names
df.columns=['Market_ID','Market_Name','Market_URL','Contract_ID','Contract_Name','bestBuyYesCost','bestBuyNoCost','BestSellYesCost','BestSellNoCost','Time_Stamp','Status']


scr = str('<!DOCTYPE HTML>\n<HTML>\n	<HEAD>\n		<h1>Detailed PredictIt Charts</h1>\n	</HEAD>\n	<BODY>')


#		<A HREF="7940.html">Biden Price</A>
for p in jsondata['markets']:
    scr = str(scr + '<h3>' + p['name'] + '</h3>\n')
    for k in p['contracts']:
        scr = str(scr + '<A HREF="' + str(k['id']) + '.html">' + str(k['name']) + '</A>\n')


scr = str(scr + '\n	</BODY>\n</HTML>')

print(scr)


f = open("indexgen.txt", "w")
f.write(scr[0:23721] + scr[23723:len(scr)])
f.close()