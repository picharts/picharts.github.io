# Import modules
import json
import requests
import pandas as pd
import math
from datetime import datetime



def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper


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
k_count = 0
for p in jsondata['markets']:
     for k in p['contracts']:
         data = []
         data.append([p['id'],p['name'],p['url'],k['id'],k['name'],k['bestBuyYesCost'],k['bestBuyNoCost'],k['bestSellYesCost'],k['bestSellNoCost'],current_time,p['status']])
         df = pd.DataFrame(data)
         print(df)
         df.columns = ['Market_ID', 'Market_Name', 'Market_URL', 'Contract_ID', 'Contract_Name', 'bestBuyYesCost',
                       'bestBuyNoCost', 'BestSellYesCost', 'BestSellNoCost', 'Time_Stamp', 'Status']
         df.to_csv(r'./' + str(id_list[k_count]) + '.csv', sep=',', encoding='utf-8', header='true')
         k_count = k_count + 1

