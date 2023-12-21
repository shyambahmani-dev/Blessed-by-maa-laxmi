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


strat_name = 'EMA Slope Strategy - Long and Short'

# most optimised value for ^NSEI at interval = 1h, longSignalBuy = 15, longSignalSell = 75, shortSignalSell = 15, shortSignalBuy = 75
# most optimised value for VOO at interval = 1h, longSignalBuy = 25, longSignalSell = 100, shortSignalSell = 100, shortSignalBuy = 5


interval = '1h'

longSignalBuy = 25
longSignalSell = 100

shortSignalSell = 75
shortSignalBuy = 5


buyAbove = 0
sellBelow = 0

tickerName = "VOO"
periodTested = "1y"

#"""
if( os.path.isfile( r".\database\%s-%s-%s-%s.csv" %(tickerName, periodTested, (str)(datetime.datetime.today().date()), interval ) ) ):
    data1 = pd.read_csv( r".\database\%s-%s-%s-%s.csv" %(tickerName, periodTested, (str)(datetime.datetime.today().date()), interval ), index_col = [0] )
    data1.index = pd.to_datetime(data1.index)
else:
    data1 = getData.tickerData(symbol= tickerName, period= periodTested, interval= interval)
    data1.to_csv( r".\database\%s-%s-%s-%s.csv" %(tickerName, periodTested, (str)(datetime.datetime.today().date()), interval  ) )
#"""

#data1 = getData.tickerData(symbol= tickerName, period = periodTested, interval= interval)

relDel = relativedelta(data1.index[-1], data1.index[0])
strat_years = float(relDel.years) + ( (float)(relDel.months)/12.0 ) +  (float)(relDel.days)/(365.25)

print("\n\n")
print("Strategy %s applied on %s at interval of %s for %.3f years from %s to %s \n \n" %(strat_name, tickerName, interval, strat_years, data1.index[0].date(), data1.index[-1].date()))



dmaIntv = [3, 5, 10, 15, 25, 50, 75, 100, 150, 200, 500]
emaIntv = [3, 5, 10, 15, 25, 50, 75, 100, 150, 200, 500]

data1DMA = getIndicators.getDMA(data1, dmaIntv)
data1EMA = getIndicators.getEMA(data1, emaIntv)
data1BB = getIndicators.getBB(data1)
data1RSI = getIndicators.getRSI(data1)
data1DMAslope = data1DMA.diff()
data1EMAslope = data1EMA.diff()


portfolio = pd.DataFrame(columns=['Value','AssetNum','Cash'], index= data1["Close"].index)

initialCash = (1.0)*(1e6)

longCurrCash = (5.0)*(1e5)
longCurrInvested = 0
longAssetNum = 0

shortCurrCash = (5.0)*(1e5)
shortCurrInvested = 0
shortAssetNum = 0


feesFactor = 0.05

daysBought = np.array([])
daysSold = np.array([])


marketPortfolio = pd.DataFrame(columns=['Value', 'AssetNum'], index= data1["Close"].index)
marketPortfolio.set_index(data1.index)
marketNum = initialCash/data1["Close"].iloc[0]




#"""

for ind in data1.index:


    if(not pd.isna(data1EMA["%s" %(max(longSignalBuy, longSignalSell, shortSignalBuy, shortSignalSell))].loc[ind])):

        buyPrice = data1["Close"].loc[ind]
        sellPrice = buyPrice
        buyRatioCash = 1
        sellRatioPort = 1

        if( data1EMAslope["%s" %(longSignalBuy)].loc[ind] > 0):
            
            numCanBuy = (buyRatioCash*longCurrCash)/( buyPrice )
            longCurrCash -= (numCanBuy*buyPrice) - min(30, (numCanBuy*(buyPrice)*feesFactor))
            longAssetNum += numCanBuy
            
            daysBought = np.append(daysBought, ind)
        

        
        elif( data1EMAslope["%s" %(longSignalSell)].loc[ind] < 0):

            numCanSell = (longAssetNum)*(sellRatioPort)
            longCurrCash += (numCanSell*(sellPrice)) - min(30, (numCanSell*(sellPrice))*feesFactor)
            longAssetNum -= numCanSell
            
            daysSold = np.append(daysSold, ind)

        

        if( data1EMAslope["%s" %(shortSignalSell)].loc[ind] < 0 and shortAssetNum == 0):
            
            numCanBuy = (buyRatioCash*shortCurrCash)/( buyPrice )
            shortCurrCash += (numCanBuy*buyPrice) - min(30, (numCanBuy*(buyPrice)*feesFactor))
            shortAssetNum -= numCanBuy
            
            daysSold = np.append(daysSold, ind)
        

        
        elif( data1EMAslope["%s" %(shortSignalBuy)].loc[ind] > 0):

            numCanSell = (-1*shortAssetNum)*(sellRatioPort)
            shortCurrCash -= (numCanSell*(sellPrice)) - min(30, (numCanSell*(sellPrice))*feesFactor)
            shortAssetNum = 0
            
            daysBought = np.append(daysBought, ind)


    portfolio.loc[ind] = [longCurrCash + longAssetNum*(data1["Close"].loc[ind]) + shortCurrCash + shortAssetNum*(data1["Close"].loc[ind]), longAssetNum + shortAssetNum, longCurrCash + shortCurrCash]
    marketPortfolio.loc[ind] = [marketNum*(data1["Close"].loc[ind]), marketNum]


#"""



#print(portfolio)
#print("\n")
#print(marketPortfolio)



analysis = pa.analytics(data1, tickerName, periodTested, interval, portfolio, marketPortfolio, daysBought, daysSold)
totalReturns = analysis.portfolio_returns()
CAGRportfolio = analysis.CAGR()
marketDev = analysis.market_dev()
AUC = analysis.AUC_comp()
sharpeRatio = analysis.sharpe_ratio()
drawdown = analysis.drawdown()





print(":: Total Returns :: \n")
print("Strategy : %.3f" %(totalReturns['portfolioReturns']))
print("Benchmark : %.3f" %(totalReturns['benchmarkReturns']))
print("Excess : %.3f" %(totalReturns['excessReturns']))

print("\n\n")

print(":: CAGR analysis :: \n")
print("Strategy : %.3f" %(CAGRportfolio['CAGRPort']))
print("Market : %.3f" %(CAGRportfolio['CAGRMarket']))
print("Excess : %.3f" %(CAGRportfolio['CAGRExcess']))

print("\n\n")

print(":: AUC analysis :: \n")
print("AUC of Portfolio = %.3f" %(AUC['portfolioAUC']) )
print("AUC of Market = %.3f" %(AUC['marketPortfolioAUC']) )
print("AUC ratio = %.3f" %(AUC['AUCRatio']) )

print("\n\n")

print(":: Market deviation analysis :: \n")
print("Max up from market = %.3f" %(marketDev['maxUp']) )
print("Max Down from market = %.3f" %(marketDev['maxDown']) )
print("Average Up from market = %.3f" %(marketDev['averageUp']) )

print("\n\n")

print(":: Sharpe Ratio analysis :: \n")
print("Sharpe Ratio of Portfolio = %.3f" %(sharpeRatio['sharpeRatioPortfolio']))
print("Sharpe Ratio of Benchmark = %.3f" %(sharpeRatio['sharpeRatioBenchmark']))

print("\n\n")

print(":: Drawdown analysis :: \n")
print("Max Drawdown of Portfolio = %.3f" %(drawdown['drawdownPortfolio']))
print("Max Drawdown of Benchmark = %.3f" %(drawdown['drawdownBenchmark']))






plotPortfolio.plot(data1, tickerName, periodTested, portfolio, strat_name, daysBought, daysSold, marketPortfolio)
#plotTrades.plot(data1, tickerName, periodTested, portfolio, strat_name, daysBought, daysSold, marketPortfolio)



#input("Done")
#code.interact(local=locals())
