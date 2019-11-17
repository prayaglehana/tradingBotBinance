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
quantity= '0.05'

def getCurPrice():
    req=requests.get(url='https://api.binance.com/api/v3/ticker/price?symbol='+symbol)
    req = json.loads(req.text)
    return float(req['price'])
def getMaxAmount():
    txt=webdriver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div/div[2]/div[2]/div[2]/div/div[3]/div[1]/form/div[1]/div/div').text
    lst=txt.split(' ')
    amnt=float(lst[1])
    return amnt
    


options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

chromedriver_path = 'C:\WareHouse\Installed Apps\chromeDriver\chromedriver.exe'
webdriver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
sleep(1)
webdriver.get('https://www.binance.com/en/usercenter/wallet/balances')
username = webdriver.find_element_by_xpath('//*[@id="login_input_email"]')
username.send_keys('prayag.lehana02@gmail.com')
password = webdriver.find_element_by_xpath('//*[@id="login_input_password"]')
password.send_keys('%Pri545xxx')


button_login = webdriver.find_element_by_xpath('//*[@id="login_input_login"]')
button_login.click()
input("Press Enter to continue...")
webdriver.get('https://www.binance.com/en/trade/pro/'+wsymbol)

amountField=webdriver.find_element_by_xpath('//*[@id="FormRow-BUY-quantity"]')
amountField.send_keys(str(getCurPrice()))


