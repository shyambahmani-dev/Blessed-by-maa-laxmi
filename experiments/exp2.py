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
import Project1.graphing_functions.drawer as drawer
import Project1.graphing_functions.plotPortfolio as plotPortfolio
import Project1.performance_analysis.performance_analysis as pa



from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from lightweight_charts.widgets import QtChart

class plot(object):

    #"""
    
    def __init__(self, data1, tickerName, periodTested, portfolio, strat_name, daysBought, daysSold, marketPortfolio):

        self.data1 = data1
        self.tickerName = tickerName
        self.periodTested = periodTested
        self.portfolio = portfolio
        self.strat_name = strat_name
        self.daysBought = daysBought
        self.daysSold = daysSold
        self.marketPortfolio = marketPortfolio
        
        app = QApplication([])
        window = QMainWindow()
        layout = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(layout)

        window.resize(800, 500)
        layout.setContentsMargins(0, 0, 0, 0)



        chart = QtChart(widget, toolbox=False, inner_height=0.6)

        portfolioLine = chart.create_line("Value", color= 'darkgreen')
        portfolioLine.set(self.portfolio)


        marketPortfolioLine = chart.create_line("Value", color= 'sienna')
        marketPortfolioLine.set(self.marketPortfolio)

        chart2 = chart.create_subchart(toolbox=True, position='right', width=1, height=0.4, sync= True)
        chart2.set(self.data1)




        layout.addWidget(chart.get_webview())

        window.setCentralWidget(widget)
        window.show()

        app.exec_()


