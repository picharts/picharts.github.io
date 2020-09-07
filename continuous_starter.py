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
        data.append([p['id'],p['name'],p['url'],k['id'],k['name'],k['bestBuyYesCost'],k['bestBuyNoCost'],k['bestSellYesCost'],k['bestSellNoCost'],p['timeStamp'],p['status']])

# Pandas dataframe named 'df'
df = pd.DataFrame(data)
# Update dataframe column names
df.columns=['Market_ID','Market_Name','Market_URL','Contract_ID','Contract_Name','bestBuyYesCost','bestBuyNoCost','BestSellYesCost','BestSellNoCost','Time_Stamp','Status']


#user input
no_sum = np.zeros(market_count)
record_high = np.zeros(market_count)
market_id = np.zeros(market_count)

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
p_count = 0

for p in jsondata['markets']:
    best_no = np.zeros(len(p['contracts']))
    number_shares = np.zeros(len(p['contracts']))
    money_lost = np.zeros(len(p['contracts']))
    money_won = np.zeros(len(p['contracts']))
    net = np.zeros(len(p['contracts']))
    k_count = 0
    k2_count = 0

    for k in p['contracts']:
        #print(k_count)
        if k['bestBuyNoCost'] != 0:
            best_no[k_count] = k['bestBuyNoCost']
            number_shares[k_count] = 800                        #note, init all at 800. can be optimized later
            money_lost[k_count] =  number_shares[k_count] * best_no[k_count]
            money_won[k_count] = (1-best_no[k_count]) * number_shares[k_count] * 0.9 #10% fee
        k_count=k_count + 1

    for k2 in p['contracts']:
        if k2['bestBuyNoCost'] != 0:
            net[k2_count] = sum(money_won) - money_won[k2_count] - money_lost[k2_count]
        k2_count = k2_count + 1

    while(max(money_lost)<849):
        if(max(net)<0.01):              #double check this assumption
            break
        #print(p['name'])
        #print(number_shares)
        #print(money_lost)
        if(np.count_nonzero(net)<1):
            break
        else:
            index_of_maximum = np.where(net == np.max(net[np.nonzero(net)]))
        number_shares[index_of_maximum] = number_shares[index_of_maximum] + 1
        k3_count = 0
        k4_count = 0
        for k3 in p['contracts']:
            #print(k3['bestBuyNoCost'])
            if k3['bestBuyNoCost'] != 0:
                money_lost[k3_count] = number_shares[k3_count] * best_no[k3_count]
                money_won[k3_count] = (1 - best_no[k3_count]) * number_shares[k3_count] * 0.9  # 10% fee
            k3_count = k3_count + 1
        for k4 in p['contracts']:
            if k4['bestBuyNoCost'] != 0:
                net [k4_count] = sum(money_won) - money_won[k4_count] - money_lost[k4_count]
            k4_count = k4_count + 1
    record_high[p_count] = min(net)
    market_id[p_count] = p['id']
    np.savetxt("record_high.csv", record_high, delimiter=",")
    np.savetxt("market_id.csv", market_id, delimiter=",")

    p_count = p_count+1
    if(max(net)>0 and min(net)>0):
        #print('NEG RISK OPPORTUNITY \n$' + str(truncate(min(net),2)) + ' minimum winning in the market:\n' + p['name'] + '\nby buying NOs in the amount' + str(number_shares) + '\n' + current_time)
        api.update_status('NEG RISK OPPORTUNITY \n$' + str(truncate(min(net),2)) + ' minimum winning in the market:\n' + p['name'] + '\nby buying NOs in the amount ' + str(number_shares) + '\n' + current_time)
