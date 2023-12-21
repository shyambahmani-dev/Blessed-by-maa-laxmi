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
import Project1.graphing_functions.drawer as drawer
import Project1.graphing_functions.plotPortfolio as plotPortfolio
import Project1.performance_analysis.performance_analysis as pa



from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from lightweight_charts.widgets import QtChart

class plot(object):

    #"""
    
    def __init__(self, data1, tickerName, periodTested):

        self.data1 = data1
        self.tickerName = tickerName
        self.periodTested = periodTested
        self.dataAll = {}

        
        app = QApplication([])
        window = QMainWindow()
        layout = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(layout)

        window.resize(800, 500)
        layout.setContentsMargins(0, 0, 0, 0)


        chart = QtChart(widget, toolbox=False, inner_height=0.6)
        chart.topbar.textbox(self.tickerName)
        chart.topbar[self.tickerName].set(self.tickerName)

        chart.topbar.menu(
            'timeframe',
            ('1m', '5m', '15m', '30m', '1h', '1d', '1wk', '1mo', '3mo'),
            default='1d',
            func=self.on_timeframe_selection
        )

        chart.topbar.menu(
            'period',
            ("1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"),
            default = '1y',
            func=self.on_period_selection
        )

        chart.topbar.menu(
            'indicators',
            ('DMA', 'EMA', 'RSI', 'Bollinger Bands', 'Fibbonacci Retracement'),
            func= self.on_indicator_selection
            )

        chart.set(self.data1)

        chart2 = chart.create_subchart(toolbox=True, position='right', width=1, height=0.4, sync= True)


        layout.addWidget(chart.get_webview())

        window.setCentralWidget(widget)
        window.show()

        app.exec_()

    def get_bar_data(self, chart, symbol, timeframe = '1m', period= '1y'):
        
        if timeframe in ('1m', '5m', '15m', '30m'):
            days = 7 if timeframe == '1m' else 57
            start_date = datetime.datetime.now()-datetime.timedelta(days=days)
            
            data = yf.download(symbol, interval=timeframe, start= start_date, end= datetime.datetime.today())
        else:
            data = yf.download(symbol, interval=timeframe, period= period)

        chart.spinner(True)
        dataAll[timeframe] = data
        chart.spinner(False)

        if data.empty:
            return False
        chart.set(data)
        return True


    def on_search(self, chart, searched_string):
        if self.get_bar_data(chart, searched_string, chart.topbar['timeframe'].value):
            chart.topbar['symbol'].set(searched_string)

    def on_timeframe_selection(self, chart):
        self.get_bar_data(chart, chart.topbar[symbol].value, chart.topbar['timeframe'].value)

    def on_indicator_selection(self, chart):
        indicators.plot_indicator(chart, chart.topbar[symbol].value, chart.topbar['indicators'].value, chart.topbar['period'].value)

    def on_period_selection(self, chart):
        pass


