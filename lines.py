# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 17:02:40 2020

@author: marlon
"""


import pandas as pd
import numpy as np
import yfinance
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = [12, 7]

plt.rc('font', size=14)

dffull = pd.read_csv('D:/aboth-/tables/banco-do-brasil-on-BBAS3.csv',sep=';' ,decimal= ',')

df = pd.DataFrame()

df['Date'] = dffull['Date']
df['Open'] = dffull['Abertura']
df['High'] = dffull['Máxima']
df['Low'] = dffull['Mínima']
df['Close'] = dffull['Fechamento']

df['Open'] = df['Open'].astype('float32')
df['High'] = df['High'].astype('float32')
df['Low'] = df['Low'].astype('float32')
df['Close'] = df['Close'].astype('float32')



def isSupport(df,i):
  support = df['Low'][i] < df['Low'][i-1]  and df['Low'][i] < df['Low'][i+1] \
  and df['Low'][i+1] < df['Low'][i+2] and df['Low'][i-1] < df['Low'][i-2]

  return support

def isResistance(df,i):
  resistance = df['High'][i] > df['High'][i-1]  and df['High'][i] > df['High'][i+1] \
  and df['High'][i+1] > df['High'][i+2] and df['High'][i-1] > df['High'][i-2] 

  return resistance

levels = []
for i in range(2,df.shape[0]-2):
  if isSupport(df,i):
    levels.append((i,df['Low'][i]))
  elif isResistance(df,i):
    levels.append((i,df['High'][i]))
    

def plot_all():
  fig, ax = plt.subplots()

  candlestick_ohlc(ax,df.values,width=0.6, \
                   colorup='green', colordown='red', alpha=0.8)

  date_format = mpl_dates.DateFormatter('%d %b %Y')
  ax.xaxis.set_major_formatter(date_format)
  fig.autofmt_xdate()

  fig.tight_layout()

  for level in levels:
    plt.hlines(level[1],xmin=df['Date'][level[0]],\
               xmax=max(df['Date']),colors='blue')
  fig.show()   
  
plot_all()