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

for n in range(120):
    # Pull in market data from PredictIt's API
    URL = "https://www.predictit.org/api/marketdata/all/"
    response = requests.get(URL)
    jsondata = response.json()

    now = datetime.now()
    current_time = now.strftime("%m/%d/%Y %H:%M:%S")
    t = TicToc()  # create instance of class

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
    t.tic()
    for p in jsondata['markets']:
        for k in p['contracts']:
            id_list.append(k['id'])
    t.toc()

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
    t.tic()
    for q in id_list:
        presdata = pd.read_csv('./' + str(q) + '.csv')
        presdata = presdata.drop(presdata.columns[0], axis=1)
        presdata = presdata.values.tolist()
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
                                  title='market' + str(q))

                    fig.update_xaxes(rangeslider_visible=True)
                    fig.write_html(r'' + str(q) + '.html')

    t.toc()
    from git import Repo

    PATH_OF_GIT_REPO = r'C:\Users\lundj\AppData\Roaming\JetBrains\PyCharmCE2020.1\scratches\.git'  # make sure .git folder is properly configured
    COMMIT_MESSAGE = 'comment from new python script'

    def git_push():
            repo = Repo(PATH_OF_GIT_REPO)
            repo.git.add(update=True)
            repo.index.commit(COMMIT_MESSAGE)
            origin = repo.remote(name='origin')
            origin.push()
    print('flag1')
    t.tic()
    git_push()
    print('flag2')
    t.toc()
    time.sleep(300)
