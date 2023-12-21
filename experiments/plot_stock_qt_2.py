import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.widgets as mplw
from matplotlib.backends.backend_pdf import PdfPages, FigureCanvasPdf
import yfinance as yf
import datetime
import csv
import os
import code
import time
from dateutil.relativedelta import relativedelta
from pandas import ExcelWriter
import inline
import traceback

import os
import sys

sys.path.append("..")
import code


import Project1.data_functions.get_data as getData
import Project1.data_functions.get_indicators as getIndicators
import Project1.data_functions.indicators as indicators
import Project1.performance_analysis.run_analysis as pa



from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from lightweight_charts.widgets import QtChart

class plot(object):

    #"""
    
    def __init__(self, dataAll, tickerName):

        self.dataAll = dataAll
        self.tickerName = tickerName

        
        app = QApplication([])
        window = QMainWindow()
        layout = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(layout)

        window.resize(800, 500)
        layout.setContentsMargins(0, 0, 0, 0)


        chart = QtChart(widget, toolbox=False)
        chart.topbar.textbox(self.tickerName)
        chart.topbar[self.tickerName].set(self.tickerName)

        chart.topbar.menu(
            'timeframe',
            ('1m', '5m', '15m', '30m', '1h', '1d', '1wk', '1mo', '3mo'),
            default='1d',
            func=self.on_timeframe_selection
        )

        chart.topbar.menu(
            'indicators',
            ('DMA', 'EMA', 'RSI', 'Bollinger Bands', 'Fibbonacci Retracement'),
            func= self.on_indicator_selection
            )
        

        layout.addWidget(chart.get_webview())

        window.setCentralWidget(widget)
        window.show()

        app.exec_()


    def get_bar_data(self, chart, tickerName, timeframe = '1d'):
        
        if( not (str(tickerName + '-' + timeframe) in self.dataAll) ):

            if timeframe in ('1m', '5m', '15m', '30m'):
                
                days = 7 if timeframe == '1m' else 57
                start_date = datetime.datetime.now()-datetime.timedelta(days=days)
                
                self.dataAll[tickerName + '-' + timeframe] = getData.tickerData(tickerName, startdate= start_date, enddate= datetime.datetime.today(), interval= timeframe)
            
            else:
                
                self.dataAll[tickerName + '-' + timeframe] = getData.tickerData(tickerName, period= 'max', interval= timeframe)
            

        if self.dataAll[tickerName + '-' + timeframe].empty:
            return False
        chart.set(self.dataAll[tickerName + '-' + timeframe])
        return True


    def on_timeframe_selection(self, chart):
        
        self.get_bar_data(chart, chart.topbar[self.tickerName].value, chart.topbar['timeframe'].value)
        #self.plot_indicator(chart, chart.topbar[self.tickerName].value, chart.topbar['indicators'].value, chart.topbar['period'].value)

    def on_indicator_selection(self, chart):

        plot_indicator(self.dataAll, self.tickerName, self.chart, chart.topbar['indicators'].value)


class plot_indicator(plot):

    def __init__(self, dataAll, tickerName, chart, indicatorName):

        super().__init__(dataAll, tickerName)

        self.chart = chart
        self.indicatorName = indicatorName
        self.lines = {}

        if(self.indicatorName == 'DMA'):
            self.plot_DMA(self.chart)

    def nullIndicator(self):

        pass

    def plot_DMA(self,chart):
            
            dmaIntv = [3, 5, 10, 25, 50, 100, 200, 500]

            data1DMA = pd.DataFrame()

            for it in dmaIntv:

                data1DMA["DMA%d" %(it)] = self.data["Close"].rolling(it).mean()

            data1DMA.rename(columns={'Date':'time'})

            #"""
            for it in dmaIntv:

                print(data1DMA["%d" %(it)])
                self.lines["%d" %(it)] = self.chart.create_line(name='DMA%d' %(it))
                self.lines["%d" %(it)].set(data1DMA)
            #"""

    




tickerName = "SBIN.NS"
timeframe = '1d'

dataAll = {}

dataAll[tickerName + '-' + timeframe] = getData.tickerData(symbol= tickerName, period= 'max', interval= timeframe)

plotStock = plot(dataAll, tickerName)

