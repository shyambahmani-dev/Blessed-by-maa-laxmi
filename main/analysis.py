import numpy as np
import pandas as pd
import yfinance as yf
import datetime
import csv
import os
import code
from dateutil.relativedelta import relativedelta
import traceback
import warnings
warnings.filterwarnings("ignore")

import sys
sys.path.append("..")



import Project1.data_functions.get_data as getData
import Project1.data_functions.get_indicators as getIndicators
import Project1.performance_analysis.run_analysis as pa
import Project1.graphing_functions.plotPortfolio as plotPortfolio
import Project1.graphing_functions.plotTrades as plotTrades


strat_name = 'data_analysis'

niftyList = [ "ADANIENT.NS", "ADANIPORTS.NS", "APOLLOHOSP.NS", "ASIANPAINT.NS", "AXISBANK.NS", 
             "BAJAJ-AUTO.NS", "BAJFINANCE.NS", "BAJAJFINSV.NS", "BPCL.NS", "BHARTIARTL.NS", 
             "BRITANNIA.NS", "CIPLA.NS", "COALINDIA.NS", "DIVISLAB.NS", "DRREDDY.NS", "EICHERMOT.NS", 
             "GRASIM.NS", "HCLTECH.NS", "HDFCBANK.NS", "HDFCLIFE.NS", "HEROMOTOCO.NS", "HINDALCO.NS", 
             "HINDUNILVR.NS", "ICICIBANK.NS", "ITC.NS", "INDUSINDBK.NS", "INFY.NS", "JSWSTEEL.NS", 
             "KOTAKBANK.NS", "LTIM.NS", "LT", "M&M.NS", "MARUTI.NS", "NTPC.NS", "NESTLEIND.NS", 
             "ONGC.NS", "POWERGRID.NS", "RELIANCE.NS", "SBILIFE.NS", "SBIN.NS", "SUNPHARMA.NS", "TCS.NS", 
             "TATACONSUM.NS", "TATAMOTORS.NS", "TATASTEEL.NS", "TECHM.NS", "TITAN.NS", "UPL.NS", "ULTRACEMCO.NS", "WIPRO.NS"]





nifty = getData.tickerData(symbol= "^NSEI", interval= '1d', period= '1y')
momomentum = getData.tickerData(symbol= "MOMOMENTUM.NS", interval= '1d', period= '1y')
SBINiftyETF = getData.tickerData(symbol= "SETFNIF50.NS", interval= '1d', period= '1y')
UTINiftyETF = getData.tickerData(symbol= "UTINIFTETF.NS", interval= '1d', period= '1y')
HDFCGoldETF = getData.tickerData(symbol= "HDFCMFGETF.NS", interval= '1d', period= '1y')

names = ["NIFTY", "MOMENTUM", "GOLD"]

listOfAsset = [nifty["Close"], momomentum["Close"], HDFCGoldETF["Close"]]
daily_rets = {}


niftyRet = (nifty - nifty.shift(1))/(nifty.shift(1))

for (name, it) in zip(names, listOfAsset):
    daily_rets[name] = (it - it.shift(1))/(it.shift(1))
    daily_rets[name] = daily_rets[name].dropna()


daily_returns = pd.DataFrame(daily_rets)
daily_returns.to_csv(r'D:\Projects\Efficient-Frontier-Python-main\daily_returns2.csv')


code.interact(local=locals())
