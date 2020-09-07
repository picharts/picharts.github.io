# Import modules
import json
import requests
import numpy as np
import pandas as pd
import tweepy
import math
import time
from datetime import datetime

# Authenticate to Twitter
auth = tweepy.OAuthHandler("5ihGZy9Us9HFMB8ygBi6JmYcX", "keccPYMyGJUNRqZ6I94OnMRjDedk0v1m8tJqHgDs0pR9Pu7jLL")
auth.set_access_token("1293770516147441665-lwWaRBCCFGm06FDEcTyh6CLJEobKCd", "U4RrZcLwtYi1PNUkTbcoyWq02YskivgOhk3Db8BCSWPMH")

# Create API object
api = tweepy.API(auth)


while(1==1):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    api.update_status("this works lol" + current_time)
    time.sleep(60)