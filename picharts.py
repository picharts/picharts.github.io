# Import modules
import json
import requests
import numpy as np
import pandas as pd
import tweepy
import math
import time
from datetime import datetime
from pytictoc import TicToc

import plotly.express as px

for n in range(1200):
    t = TicToc()  # create instance of class
    t.tic()
    # Pull in market data from PredictIt's API
    URL = "https://www.predictit.org/api/marketdata/all/"
    response = requests.get(URL)
    jsondata = response.json()

    now = datetime.now()
    current_time = now.strftime("%m/%d/%Y %H:%M:%S")

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

    id_list = []

    for p in jsondata['markets']:
        for k in p['contracts']:
            id_list.append(k['id'])

    ########## INITIALIZE CSVs ###################
    # k_count = 0
    # for p in jsondata['markets']:
    #     for k in p['contracts']:
    #         data = []
    #         data.append([p['id'],p['name'],p['url'],k['id'],k['name'],k['bestBuyYesCost'],k['bestBuyNoCost'],k['bestSellYesCost'],k['bestSellNoCost'],current_time,p['status']])
    #         df = pd.DataFrame(data)
    #         print(df)
    #         df.columns = ['Market_ID', 'Market_Name', 'Market_URL', 'Contract_ID', 'Contract_Name', 'bestBuyYesCost',
    #                       'bestBuyNoCost', 'BestSellYesCost', 'BestSellNoCost', 'Time_Stamp', 'Status']
    #         df.to_csv(r'./' + str(id_list[k_count]) + '.csv', sep=',', encoding='utf-8', header='true')
    #         k_count = k_count + 1

    #######################

    for q in id_list:
        try:
            presdata = pd.read_csv('./' + str(q) + '.csv')
            presdata = presdata.drop(presdata.columns[0], axis=1)
            presdata = presdata.values.tolist()
        except:
            presdata = []
        # Market data by contract/price in dataframe
        data = []
        # presdata = []
        for p in jsondata['markets']:
             for k in p['contracts']:
                 if (k['id'] == q):
                    presdata.append([p['id'], p['name'], p['url'], k['id'], k['name'], k['bestBuyYesCost'], k['bestBuyNoCost'], k['bestSellYesCost'], k['bestSellNoCost'], current_time, p['status']])
                    # Pandas dataframe named 'df'
                    presdf = pd.DataFrame(presdata)
                    # Update dataframe column names
                    presdf.columns = ['Market_ID', 'Market_Name', 'Market_URL', 'Contract_ID', 'Contract_Name',
                                      'bestBuyYesCost', 'bestBuyNoCost', 'BestSellYesCost', 'BestSellNoCost', 'Time_Stamp',
                                      'Status']
                    # Write dataframe to CSV file in working directory
                    presdf.to_csv(r'./' + str(q) + '.csv', sep=',', encoding='utf-8', header='true')

                    fig = px.line(presdf, x='Time_Stamp',
                                  y=['bestBuyYesCost', 'bestBuyNoCost', 'BestSellYesCost', 'BestSellNoCost'],
                                  title=k['name'] + ' in ' + p['name']+ ' ' + p['url'])

                    fig.update_xaxes(rangeslider_visible=True, rangeselector=dict(
                        buttons=list([
                        dict(count=1, label="1d", step="day", stepmode="backward"),
                        dict(count=7, label="7d", step="day", stepmode="backward"),
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(step="all")
                        ])))
                    fig.write_html(r'' + str(q) + '.html')

    t.toc()
    from git import Repo

    time.sleep(10)
