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

from tqdm import tqdm

import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.figure_factory as ff

import sys
sys.path.append("..")


import Project1.data_functions.get_data as getData
import Project1.data_functions.get_indicators as getIndicators
import Project1.performance_analysis.run_analysis as pa
import Project1.graphing_functions.testPortfolio as testPortfolio




niftyETF = getData.tickerData(symbol= "SETFNIF50.NS", interval= '1d', period= '1y')
momentumETF = getData.tickerData(symbol= "MOMOMENTUM.NS", interval= '1d', period= '1y')
goldETF = getData.tickerData(symbol= "SETFGOLD.NS", interval= '1d', period= '1y')

listOfAsset = [niftyETF, momentumETF, goldETF]


names = ["NIFTY", "MOMENTUM", "GOLD"]

daily_rets = {}


for (name, it) in zip(names, listOfAsset):
    daily_rets[name] = (it["Close"] - it["Close"].shift(1))/(it["Close"].shift(1))
    daily_rets[name] = daily_rets[name].dropna()


daily_returns = pd.DataFrame(daily_rets)

print(daily_returns)

#-- Get annualised mean returns
mus = (1+daily_returns.mean())**252 - 1
#-- Get covariances
#- Multiply by 252 to annualise it (square root time for volatility but no square root for variance)
#- Note: 252 trading days in a year
cov = daily_returns.cov()*252


print(mus)
print(cov)
print(daily_returns.corr())





#- How many assests to include in each portfolio
n_assets = 3
#-- How many portfolios to generate
n_portfolios = 1000

#-- Initialize empty list to store mean-variance pairs for plotting
mean_variance_pairs = []
portfolio_weights = []
weights_list=[]
tickers_list=[]


np.random.seed(75)
#-- Loop through and generate lots of random portfolios
for i in range(n_portfolios):
    #- Choose assets randomly without replacement
    assets = np.random.choice(list(daily_returns.columns), n_assets, replace=False)
    #- Choose weights randomly
    weights = np.random.rand(n_assets)
    #- Ensure weights sum to 1
    weights = weights/sum(weights)

    #-- Loop over asset pairs and compute portfolio return and variance
    #- https://quant.stackexchange.com/questions/43442/portfolio-variance-explanation-for-equation-investments-by-zvi-bodie
    portfolio_E_Variance = 0
    portfolio_E_Return = 0
    for i in range(len(assets)):
        portfolio_E_Return += weights[i] * mus.loc[assets[i]]
        for j in range(len(assets)):
            #-- Add variance/covariance for each asset pair
            #- Note that when i==j this adds the variance
            portfolio_E_Variance += weights[i] * weights[j] * cov.loc[assets[i], assets[j]]
            
    #-- Add the mean/variance pairs to a list for plotting
    mean_variance_pairs.append([portfolio_E_Return, portfolio_E_Variance])
    portfolio_weights.append(weights)
    
    weights_list.append(weights)
    tickers_list.append(assets)

    
data = pd.DataFrame(mean_variance_pairs)
data["Weights"] = portfolio_weights
data["sharpeRatios"] = (data.iloc[:,0])/(data.iloc[:,1]**0.5)

sharpeAndWeight = []

for it in data.index:
    sharpeAndWeight.append([data.loc[it,"sharpeRatios"], data.loc[it,"Weights"]])
    
sharpeAndWeight.sort(reverse = True)



#-- Plot the risk vs. return of randomly generated portfolios
#-- Convert the list from before into an array for easy plotting
mean_variance_pairs = np.array(mean_variance_pairs)




risk_free_rate=0.05 #-- Include risk free rate here

fig = go.Figure()
fig.add_trace(go.Scatter(x=mean_variance_pairs[:,1]**0.5, y=mean_variance_pairs[:,0], 
                      marker=dict(color=(mean_variance_pairs[:,0]-risk_free_rate)/(mean_variance_pairs[:,1]**0.5), 
                                  showscale=True, 
                                  size=7,
                                  line=dict(width=1),
                                  colorscale="RdBu",
                                  colorbar=dict(title="Sharpe<br>Ratio")
                                 ), 
                      mode='markers',
                      text=[str(np.array(data["sharpeRatios"].iloc[i])) + "<br>" + str(np.array(tickers_list[i])) + "<br>" + str(np.array(weights_list[i]).round(2)) for i in range(len(tickers_list))]))
fig.update_layout(template='plotly_white',
                  xaxis=dict(title='Annualised Risk (Volatility)'),
                  yaxis=dict(title='Annualised Return'),
                  title='Sample of Random Portfolios',
                  width=1500,
                  height=1000)
fig.update_xaxes(range=[0, 0.20])
fig.update_yaxes(range=[0.,0.5])
fig.update_layout(coloraxis_colorbar=dict(title="Sharpe Ratio"))

fig.show()




print("Hello")

portfolio = pd.DataFrame(columns=['Value'], index= niftyETF["Close"].index)

initialCash = 1e6*1.0


feesFactor = 0.05

daysBought = np.array([])
daysSold = np.array([])


print( " %s -- %.3f:%.3f:%.3f " %(sharpeAndWeight[0][0] , sharpeAndWeight[0][1][0] , sharpeAndWeight[0][1][1], sharpeAndWeight[0][1][2]))


niftyWeight = sharpeAndWeight[0][1][0]
momentumWeight = sharpeAndWeight[0][1][1]
goldWeight = sharpeAndWeight[0][1][2]



niftyWeight = sharpeAndWeight[0][1][0]
momentumWeight = sharpeAndWeight[0][1][1]
goldWeight = sharpeAndWeight[0][1][2]

niftyNum = (niftyWeight)*(initialCash/niftyETF["Close"].iloc[0])
momentumNum = (momentumWeight)*(initialCash/momentumETF["Close"].iloc[0])
goldNum = (goldWeight)*(initialCash/goldETF["Close"].iloc[0])



initialNifty = initialCash/niftyETF["Close"].iloc[0]
initialMomentum = initialCash/momentumETF["Close"].iloc[0]
initialGold = initialCash/goldETF["Close"].iloc[0]



niftyPortfolio = pd.DataFrame(columns=['Value'], index= niftyETF["Close"].index)
niftyPortfolio["Value"] = initialNifty*niftyETF["Close"]

momentumPortfolio = pd.DataFrame(columns=['Value'], index= momentumETF["Close"].index)
momentumPortfolio["Value"] = initialMomentum*momentumETF["Close"]

goldPortfolio = pd.DataFrame(columns=['Value'], index= goldETF["Close"].index)
goldPortfolio["Value"] = initialGold*goldETF["Close"]



portfolio["Value"] = niftyNum*niftyETF["Close"] + momentumNum*momentumETF["Close"] + goldNum*goldETF["Close"]

componentList = [ niftyPortfolio, goldPortfolio, momentumPortfolio ]

testPortfolio.plot([portfolio], componentList)
