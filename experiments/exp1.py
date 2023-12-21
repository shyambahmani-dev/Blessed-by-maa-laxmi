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
import traceback

import sys
sys.path.append(".")
sys.path.append("..")


#"""

import Project1.data_functions.get_data as getData
import Project1.data_functions.get_indicators as getIndicators

import Project1.data_functions.indicators as indicators

#"""

import lightweight_charts
from lightweight_charts import Chart

dataAll = {}

def get_bar_data(chart, symbol, timeframe = '1m', period= '1y'):
    
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


def on_search(chart, searched_string):
    if get_bar_data(chart, searched_string, chart.topbar['timeframe'].value):
        chart.topbar['symbol'].set(searched_string)

def on_timeframe_selection(chart):
    get_bar_data(chart, chart.topbar[symbol].value, chart.topbar['timeframe'].value)

def on_indicator_selection(chart):
    indicators.plot_indicator(chart, chart.topbar[symbol].value, chart.topbar['indicators'].value, chart.topbar['period'].value)

def on_period_selection(chart):
    pass



if __name__ == '__main__':

    chart = Chart(toolbox=True, debug=True, inner_height=0.7)

    symbol = '^NSEI'
    
    chart.legend(True)
    chart.events.search += on_search
    chart.topbar.textbox(symbol)
    chart.topbar[symbol].set(symbol)
    chart.topbar.menu(
        'timeframe',
        ('1m', '5m', '15m', '30m', '1h', '1d', '1wk', '1mo', '3mo'),
        default='1d',
        func=on_timeframe_selection
    )

    chart.topbar.menu(
        'period',
        ("1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"),
        default = '1y',
        func=on_period_selection
    )

    chart.topbar.menu(
        'indicators',
        ('DMA', 'EMA', 'RSI', 'Bollinger Bands', 'Fibbonacci Retracement'),
        func= on_indicator_selection
    )



    chart2 = chart.create_subchart(toolbox=True, position='right', width=1, height=0.3)

    chart2.legend(True)
    chart2.events.search += on_search
    chart2.topbar.textbox(symbol)
    chart2.topbar[symbol].set(symbol)
    chart2.topbar.menu(
        'timeframe',
        ('1m', '5m', '15m', '1hr', '1d', '1wk', '1mo'),
        default='1d',
        func=on_timeframe_selection
    )


    chart.show(block=True)