# https://web-api.coinmarketcap.com/v1/cryptocurrency/listings/historical?convert=USD,BTC&date=2020-04-28&limit=5000&start=201

# get Cryptocurrency Historical Data Snapshot
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from datetime import timedelta 
 

 
base_url="https://coinmarketcap.com/historical/"

day_zeroa=20130428
day_zero=20200427
url= base_url+str(day_zero)

#print(base_url+str(day_zero))

def next_day(day):
    day=str(day)
    y,m,d = day[:4],day[4:6],day[6:]
    return datetime.datetime(int(y), int(m), int(d)) + timedelta(days = 1)

def get_data_table(url):
    table_MN = pd.read_html(url)
    df = table_MN[2]
    print(df.describe())


    # print("1\n",table_MN)
    # print("2\n\n\n\n",f'Total tables: {len(table_MN)}')


get_data_table(url)

#     Rank       Name Symbol         Market Cap       Price Circulating Supply    % 1h  % 24h   % 7d  Unnamed: 9
#    Rank        Name Symbol        Market Cap      Price    Circulating Supply     Volume (24h)    % 1h   % 24h    % 7d  Unnamed: 10
