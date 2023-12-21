for ind in self.data1.index:


    if(not pd.isna(self.data1EMA["%s" %(max(longSignalBuy, longSignalSell, shortSignalBuy, shortSignalSell))].loc[ind])):

        buyPrice = self.data1["Close"].loc[ind]
        sellPrice = buyPrice
        buyRatioCash = 1
        sellRatioPort = 1

        if( self.data1EMAslope["%s" %(longSignalBuy)].loc[ind] > 0):
            
            numCanBuy = (buyRatioCash*longCurrCash)/( buyPrice )
            longCurrCash -= (numCanBuy*buyPrice) - min(30, (numCanBuy*(buyPrice)*feesFactor))
            longAssetNum += numCanBuy
            
            daysBought = np.append(daysBought, ind)
        

        
        elif( self.data1EMAslope["%s" %(longSignalSell)].loc[ind] < 0):

            numCanSell = (longAssetNum)*(sellRatioPort)
            longCurrCash += (numCanSell*(sellPrice)) - min(30, (numCanSell*(sellPrice))*feesFactor)
            longAssetNum -= numCanSell
            
            daysSold = np.append(daysSold, ind)

        

        if( self.data1EMAslope["%s" %(shortSignalBuy)].loc[ind] < 0 and shortAssetNum == 0):
            
            numCanBuy = (buyRatioCash*shortCurrCash)/( buyPrice )
            shortCurrCash += (numCanBuy*buyPrice) - min(30, (numCanBuy*(buyPrice)*feesFactor))
            shortAssetNum -= numCanBuy
            
            daysSold = np.append(daysSold, ind)
        

        
        elif( self.data1EMAslope["%s" %(shortSignalSell)].loc[ind] > 0):

            numCanSell = (-1*shortAssetNum)*(sellRatioPort)
            shortCurrCash -= (numCanSell*(sellPrice)) - min(30, (numCanSell*(sellPrice))*feesFactor)
            shortAssetNum = 0
            
            daysBought = np.append(daysBought, ind)


    portfolio.loc[ind] = [longCurrCash + longAssetNum*(self.data1["Close"].loc[ind]) + shortCurrCash + shortAssetNum*(self.data1["Close"].loc[ind]), longAssetNum + shortAssetNum, longCurrCash + shortCurrCash]
    marketPortfolio.loc[ind] = [marketNum*(self.data1["Close"].loc[ind]), marketNum]

