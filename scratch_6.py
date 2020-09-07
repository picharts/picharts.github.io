# Import modules
import json
import requests
import numpy as np
import pandas as pd
import tweepy
import math
import time
from datetime import datetime

# Market data by contract/price in dataframe
array1 = np.array([1, 2, 3])
array2 = np.array([4, 5, 6])
data = []
data.append(array1)
data.append(array2)

# Pandas dataframe named 'df'
df = pd.DataFrame(data)
# Update dataframe column names

# Write dataframe to CSV file in working directory
df.to_csv(r'./testcsv.csv', sep=',', encoding='utf-8')


df1 = pd.read_csv(r'./testcsv.csv', sep=',', encoding='utf-8')



a = np.array([1,2,3])
np.savetxt("foo.csv", a, delimiter=",")
my_data = np.genfromtxt('foo.csv', delimiter=",")
print(my_data)