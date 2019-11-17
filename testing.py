from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import plotly.graph_objects as go
import mpl_finance
import matplotlib.pyplot as plt
from datetime import datetime
from time import sleep
from binance.client import Client
import keyboard
import requests
import pandas as pd
import matplotlib.dates as mdates
import statistics
import numpy as np

def fetchData():
    client = Client('jYtgkaRGbEPDtOW45CzSMHgUqP6fyOjDHf0oK0DN569s2nVfLJvbXXz4L1RLsX6R','O6XKGYLUGhviFJQRyBhVAq5EwpbTQo9BXDRSe7Pec3Lu0w1d5KQoIUQUIPHBAsje') 

    symbol= 'ETHBTC'
    quantity= '0.05'

    BTC= client.get_historical_klines(symbol=symbol, interval='1m', start_str="2 hour ago UTC")

    data=[]
    for i in range(0,len(BTC)):
            mean=0
            stdev=0
            UB=0
            LB=0

            
            if(i>20):
                closes=[]
                for j in range(i-20,i):
                    closes.append(float(data[j][4]))

                mean=statistics.mean(closes)
                stdev=statistics.stdev(closes)
                
                UB=mean+2*stdev
                LB=mean-2*stdev
            dt_object= datetime.fromtimestamp(BTC[i][0]/1000)
            data.append([dt_object,BTC[i][1],BTC[i][2],BTC[i][3],BTC[i][4],mean,stdev,UB,LB])

    
     
    df = pd.DataFrame(data, columns = ['Date', 'Open','High','Low','Close','mean','stdev','upperBolBand','LowerBolBand'])
    df=df[21:]
    fig = go.Figure(data=[go.Candlestick(x=df['Date'], open=df['Open'], high=df['High'],  low=df['Low'], close=df['Close']) ])

    fig.add_trace(go.Scatter(x=df['Date'], y=df['mean'], mode='lines', name='lines'))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['upperBolBand'], mode='lines', name='lines'))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['LowerBolBand'], mode='lines', name='lines'))


    curStatus=-1 # has to buy first
    for i in range(10,len(df)):
        if(float(df.iloc[i]['Low'])<float(df.iloc[i]['LowerBolBand']) and curStatus==-1 ):
            #y_co=(float(df.iloc[i]['Close'])+float(df.iloc[i]['Open']))/2
            fig.add_trace(go.Scatter(
                
                x=[df.iloc[i]['Date']],
                y=[df.iloc[i]['Low']],
                mode="markers+text",
                name="Markers and Text",
                text=["Buy"],
                textposition="bottom center"
                ))
            curStatus=1
        elif(float(df.iloc[i]['High'])>float(df.iloc[i]['upperBolBand']) and curStatus==1 ):
            fig.add_trace(go.Scatter(
                
                x=[df.iloc[i]['Date']],
                y=[df.iloc[i]['High']],
                mode="markers+text",
                name="Markers and Text",
                text=["Sell"],
                textposition="bottom center"
                ))
            curStatus=-1
            
        
    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.show()
    return df

df=fetchData()




