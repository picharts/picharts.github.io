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

for x in range(4000):

    # Authenticate to Twitter
    auth = tweepy.OAuthHandler("4j363Uq4fbur6EfKaeVgutO2l", "zw2XE6dkWU5ILbWpovenX8SuGp6Eor2jqVWgplzXghwenxlCka")
    auth.set_access_token("1299821812315021317-XTJXnZqbGTOuVECvPcA7ZxeLHN0Edm", "SfsZ7efh6ekpAtN7uTdKSU43Yncij1OkZ0ZeXJDmlrbJD")

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
                value = 1000
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

    threshold = np.zeros(market_count)
    market_id = np.zeros(market_count)
    p_count = 0
    for p in jsondata['markets']:
        market_id[p_count] = p['id']
        threshold[p_count] = 5
        p_count = p_count + 1
    time.sleep(120)


    # second
    # Pull in market data from PredictIt's API
    URL = "https://www.predictit.org/api/marketdata/all/"
    response2 = requests.get(URL)
    jsondata2 = response2.json()

    # Replace null values with zero

    def dict_clean2(items):
        result = {}
        for key, value in items:
            if value is None:
                value = 0
            result[key] = value
        return result
    dict_str = json.dumps(jsondata2)
    jsondata2 = json.loads(dict_str, object_pairs_hook=dict_clean2)

    # Market data by contract/price in dataframe
    data2 = []
    market_count = 0;
    for p in jsondata2['markets']:
        market_count = market_count + 1
        for k in p['contracts']:
            data2.append([p['id'],p['name'],p['url'],k['id'],k['name'],k['bestBuyYesCost'],k['bestBuyNoCost'],k['bestSellYesCost'],k['bestSellNoCost'],p['timeStamp'],p['status']])


    #user input
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    p_count = 0
    k_count = 0
    for p in jsondata['markets']:
        for k in p['contracts']:
            if(np.abs(k['bestBuyNoCost']-data2[k_count][6]) > threshold[p_count] and np.abs(k['bestBuyNoCost']-data2[k_count][6]) < .97):
                #api.update_status( '$' + str(truncate((data2[k_count][6] - k['bestBuyNoCost']), 2)) + ' change in NO for \n' + p['name'] + k['name'] + '\n' + current_time)
                print('$' + str(truncate((data2[k_count][6] - k['bestBuyNoCost']), 2)) + ' change in NO for \n' + p['name'] + k['name'] + '\n' + current_time)
                #api.update_status( '$', 'change in NO for \n', p['name'], k['name'] + '\n' + current_time)
                #api.update_status('debugging new program.')
                threshold[p_count] = threshold[p_count] + 8
                time.sleep(5)
            if(np.abs(k['bestBuyYesCost'] - data2[k_count][5]) > threshold[p_count] and np.abs(k['bestBuyYesCost'] - data2[k_count][5]) < .97):
                #api.update_status('$' + str(truncate((data2[k_count][5] - k['bestBuyYesCost']), 2)) + ' change in YES for \n' + p['name'] + k['name'] + '\n' + current_time)
                print('$' + str(truncate((data2[k_count][5] - k['bestBuyYesCost']), 2)) + ' change in YES for \n' + p['name'] + k['name'] + '\n' + current_time)
                #api.update_status('debugging new program.' + current_time)
                threshold[p_count] = threshold[p_count] + 8
                time.sleep(5)
            #print(k['bestBuyNoCost'])
            #print(data2[k_count][6])

            #print(k['bestBuyYesCost'])
            #print(data2[k_count][5])



            k_count=k_count + 1
        p_count = p_count + 1

    if (now.minute == 0 or now.minute == 1):
        a_count=0
        for a in range(market_count):
            if(threshold[a_count]>5):
                threshold[a_count] = threshold[a_count] - 1
            a_count = a_count + 1


