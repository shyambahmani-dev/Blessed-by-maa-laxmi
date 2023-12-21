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



strat_name = 'dma_crossover'

tickerName = "^NSEI"
periodTested = "10y"

print("Stock analysed: %s for a period of %s \n \n" %(tickerName, periodTested))

data1 = getData.tickerData(symbol= tickerName, period= periodTested, interval= '1d')

#data1 = getData.tickerData(symbol= tickerName, interval= '5m')


dmaIntv = [3, 5, 10, 15, 25, 50, 75, 100, 150, 200, 500]
emaIntv = [3, 5, 10, 15, 25, 50, 75, 100, 150, 200, 500]

data1["Typical"] = (data1["Close"] + data1["High"] + data1["Low"])/3
data1DMA = getIndicators.getDMA(data1, dmaIntv)
data1EMA = getIndicators.getEMA(data1, emaIntv)
data1BB = getIndicators.getBB(data1)
data1RSI = getIndicators.getRSI(data1)
data1DMAslope = data1DMA.diff()


portfolio = pd.DataFrame(columns=['Value','AssetNum','Cash'], index= data1["Close"].index)

initialCash = 1e6

currCash = 1e6
currInvested = 0
assetNum = 0

feesFactor = 0.05

daysBought = np.array([])
daysSold = np.array([])


marketPortfolio = pd.DataFrame(columns=['Value', 'AssetNum'], index= data1["Close"].index)
marketPortfolio.set_index(data1.index)
marketNum = initialCash/data1["Close"].iloc[0]




#"""

for ind in data1.index:


    if(not pd.isna(data1DMA["10"].loc[ind])):

        buyPrice = data1["Typical"].loc[ind]
        sellPrice = buyPrice
        buyRatioCash = 1
        sellRatioPort = 1

        if( data1DMA["3"].loc[ind] > data1DMA["10"].loc[ind]): # and data1DMA["10"].loc[ind] > data1DMA["200"].loc[ind] ):
            
            numCanBuy = (buyRatioCash*currCash)/( buyPrice )
            currCash -= (numCanBuy*buyPrice) - min(30, (numCanBuy*(buyPrice)*feesFactor))
            assetNum += numCanBuy
            
            daysBought = np.append(daysBought, ind)
        

        
        elif( data1DMA["3"].loc[ind] < data1DMA["10"].loc[ind]): # and data1DMA["10"].loc[ind] < data1DMA["200"].loc[ind] ):

            numCanSell = (assetNum)*(sellRatioPort)
            currCash += (numCanSell*(sellPrice)) - min(30, (numCanSell*(sellPrice))*feesFactor)
            assetNum -= numCanSell
            
            daysSold = np.append(daysSold, ind)


    portfolio.loc[ind] = [currCash + assetNum*(data1["Close"].loc[ind]), assetNum, currCash]
    marketPortfolio.loc[ind] = [marketNum*(data1["Close"].loc[ind]), marketNum]


#"""



#print(portfolio.head())
#print("\n")
#print(marketPortfolio.head())



plotPortfolio.plot(data1, tickerName, periodTested, portfolio, strat_name, daysBought, daysSold, marketPortfolio)
#plotTrades.plot(data1, tickerName, periodTested, portfolio, strat_name, daysBought, daysSold, marketPortfolio)


analysis = pa.analytics(data1, tickerName, periodTested, portfolio, marketPortfolio, daysBought, daysSold)
CAGRportfolio = analysis.CAGR()
marketDev = analysis.market_dev()
AOC = analysis.AOC_comp()




print(":: CAGR analysis ::")
print("Strategy : %.3f" %(CAGRportfolio['CAGRPort']))
print("Stock : %.3f" %(CAGRportfolio['CAGRMarket']))
print("Excess : %.3f" %(CAGRportfolio['CAGRExcess']))

print("\n\n")

print("AOC analysis")
print("AOC of Portfolio = %.3f" %(AOC['portfolioAOC']) )
print("AOC of Market = %.3f" %(AOC['marketPortfolioAOC']) )
print("AOC ratio = %.3f" %(AOC['AOCRatio']) )

print("\n\n")

print("Market deviation analysis")
print("Max up from market = %.3f" %(marketDev['maxUp']) )
print("Max Down from market = %.3f" %(marketDev['maxDown']) )


#input("Done")

#code.interact(local=locals())
