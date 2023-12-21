import numpy as np
import pandas as pd
import yfinance as yf
import datetime
import csv
import os
import code
from dateutil.relativedelta import relativedelta
import traceback

import sys
sys.path.append("..")


import Project1.data_functions.get_data as getData
import Project1.data_functions.get_indicators as getIndicators

import Project1.performance_analysis.run_analysis as pa



from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton

from lightweight_charts.widgets import QtChart

class plot(object):

    #"""
    
    def __init__(self, portfolio, componentList):

        self.portfolio = portfolio
        self.componentList = componentList
        
        app = QApplication([])
        window = QMainWindow()
        layout = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(layout)

        window.resize(800, 500)
        layout.setContentsMargins(0, 0, 0, 0)

        chart = QtChart(widget, toolbox=False)





        portfolioLines = {}

        indx = 0
        portColList = ["forestgreen", "limegreen", "darkgreen", "green", "lime", "seagreen", "springgreen", "chartreuse"]

        for comp in self.portfolio:
            col = portColList[indx]
            portfolioLines[indx] = chart.create_line("Value", color = "%s" %(col))
            portfolioLines[indx].set(comp)
            indx += 1






        componentLines = {}

        indx = 0
        compColList = ["tomato", "darksalmon", "coral", "sienna", "chocolate", "saddlebrown", "peru", "darkorange"]

        for comp in self.componentList:
            col = compColList[indx]
            componentLines[indx] = chart.create_line("Value", color = "%s" %(col))
            componentLines[indx].set(comp)
            indx += 1






        layout.addWidget(chart.get_webview())
        window.setCentralWidget(widget)

        window.show()

        app.exec_()


