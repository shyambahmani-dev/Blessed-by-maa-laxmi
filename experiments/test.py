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
import Project1.main.plot_stock_qt as plotStock



strat_name = 'ema_crossover'

tickerName = "SBIN.NS"
periodTested = "10y"

data1 = getData.tickerData(symbol= tickerName, period= periodTested)

#data1 = getData.tickerData(symbol= tickerName, interval= '5m')

plotStock.plot(data1, tickerName, periodTested)

#input("Waiting")

#code.interact(local=locals())
