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
import json

symbol='ETHBTC'
wsymbol='ETH_BTC'
quantity= 0.06
thresh=0.0002

client = Client('jYtgkaRGbEPDtOW45CzSMHgUqP6fyOjDHf0oK0DN569s2nVfLJvbXXz4L1RLsX6R','O6XKGYLUGhviFJQRyBhVAq5EwpbTQo9BXDRSe7Pec3Lu0w1d5KQoIUQUIPHBAsje') 


def getMaxAmount():
    txt=webdriver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div/div[2]/div[2]/div[2]/div/div[3]/div[1]/form/div[1]/div/div').text
    lst=txt.split(' ')
    amnt=lst[1]
    return amnt

def getCurPrice():
    req=requests.get(url='https://api.binance.com/api/v3/ticker/price?symbol='+symbol)
    req = json.loads(req.text)
    return float(req['price'])

def fetchData():
 try :
    client = Client('jYtgkaRGbEPDtOW45CzSMHgUqP6fyOjDHf0oK0DN569s2nVfLJvbXXz4L1RLsX6R','O6XKGYLUGhviFJQRyBhVAq5EwpbTQo9BXDRSe7Pec3Lu0w1d5KQoIUQUIPHBAsje') 


    BTC= client.get_historical_klines(symbol=symbol, interval='1h', start_str="3 day ago UTC")

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
    #print(df)
    fig = go.Figure(data=[go.Candlestick(x=df['Date'], open=df['Open'], high=df['High'],  low=df['Low'], close=df['Close']) ])

    fig.add_trace(go.Scatter(x=df['Date'], y=df['mean'], mode='lines', name='lines'))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['upperBolBand'], mode='lines', name='lines'))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['LowerBolBand'], mode='lines', name='lines'))


  
    fig.update_layout(xaxis_rangeslider_visible=False)
    #fig.show()
    return df
 except:
    data=[]
    data.append([0,0,0,0,0,0,0,0,0])
    df = pd.DataFrame(data, columns = ['Date', 'Open','High','Low','Close','mean','stdev','upperBolBand','LowerBolBand'])
    return df
fetchData()
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

chromedriver_path = 'C:\WareHouse\Installed Apps\chromeDriver\chromedriver.exe'
webdriver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
sleep(1)
webdriver.get('https://www.binance.com/en/usercenter/wallet/balances')
username = webdriver.find_element_by_xpath('//*[@id="login_input_email"]')
username.send_keys('')
password = webdriver.find_element_by_xpath('//*[@id="login_input_password"]')
password.send_keys('')


button_login = webdriver.find_element_by_xpath('//*[@id="login_input_login"]')
button_login.click()
input("Press Enter to continue...")
webdriver.get('https://www.binance.com/en/trade/pro/'+wsymbol)

curStatus='sold' 
LastBuyAt=0

while(True):
  df=fetchData()
  if(len(df)>1):
    #print(df)
    curPrice=getCurPrice()
    if( curPrice<float(df.iloc[len(df)-1]['LowerBolBand']) and curStatus=='sold' ):
            
            LastBuyAt=curPrice
            
            priceField=webdriver.find_element_by_xpath('//*[@id="FormRow-BUY-price"]')
            
            priceField.send_keys(Keys.CONTROL + "a")
            priceField.send_keys(Keys.DELETE)
            
            priceField.send_keys(str(curPrice))
            
            amountField=webdriver.find_element_by_xpath('//*[@id="FormRow-BUY-total"]')
            
            amountField.send_keys(Keys.CONTROL + "a")
            amountField.send_keys(Keys.DELETE)
            
            
            amountField.send_keys(getMaxAmount())

            buyButton = webdriver.find_element_by_xpath('//*[@id="orderForm-button-exchangelimitBuy"]')
            buyButton.click()
            
            print('Buy at ',curPrice)
            curStatus='bought'

            
            
    elif( curPrice>float(df.iloc[len(df)-1]['upperBolBand'])and (curPrice-LastBuyAt)>thresh and curStatus=='bought'):
        
            priceField=webdriver.find_element_by_xpath('//*[@id="FormRow-SELL-price"]')
            
            priceField.send_keys(Keys.CONTROL + "a")
            priceField.send_keys(Keys.DELETE)
            
            priceField.send_keys(str(curPrice))
            
            amountField=webdriver.find_element_by_xpath('//*[@id="FormRow-SELL-quantity"]')
            
            amountField.send_keys(Keys.CONTROL + "a")
            amountField.send_keys(Keys.DELETE)
            
            amountField.send_keys(str(quantity))

            sellButton = webdriver.find_element_by_xpath('//*[@id="orderForm-button-exchangelimitSell"]')
            sellButton.click()
            
            print('Sell at ',curPrice)
            curStatus='sold'
    
  #x=client.get_open_orders(symbol=symbol)
  #print(x)
  sleep(15)
  webdriver.refresh()
  sleep(10)
            


