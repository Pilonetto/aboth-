# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 17:02:40 2020

@author: marlon
"""


import pandas as pd
import numpy as np
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt
from cfg import Settings
from utils import Globals


settings = Settings()
globais = Globals()

plt.rcParams['figure.figsize'] = [12, 7]

plt.rc('font', size=14)

dffull = pd.read_csv(settings.workpath+'/tables/' +'banco-do-brasil-on-BBAS3.csv',sep=';' ,decimal= ',')

df = pd.DataFrame()

dffull["Date"] = pd.to_datetime(dffull["Date"]).dt.strftime('%Y-%m-%d')

dffull["Date"] = pd.to_datetime(dffull["Date"])

dffull['Date'] = pd.to_datetime(dffull["Date"])
dffull['Date'] = dffull['Date'].apply(mpl_dates.date2num)


dffull = dffull[~dffull.Volume.isin(['0'])]

#dffull.drop('level_0', axis=1, inplace=True)
#dffull.drop('index', axis=1, inplace=True)
df = df.drop_duplicates()

dffull = dffull.reset_index(drop=True)


#df['Data'] = dffull['Data']
df['Date'] = dffull['Date']
df['Open'] = dffull['Abertura']
df['High'] = dffull['Máxima']
df['Low'] = dffull['Mínima']
df['Close'] = dffull['Fechamento']

df['Open'] = df['Open'].astype('float32')
df['High'] = df['High'].astype('float32')
df['Low'] = df['Low'].astype('float32')
df['Close'] = df['Close'].astype('float32')

df = df.sort_values(by=['Date'], ascending=False)

df = df.head(150)


def isSupport(df,i):
  support = df['Low'][i] < df['Low'][i-1]  and df['Low'][i] < df['Low'][i+1] \
  and df['Low'][i+1] < df['Low'][i+2] and df['Low'][i-1] < df['Low'][i-2]

  return support

def isResistance(df,i):
  resistance = df['High'][i] > df['High'][i-1]  and df['High'][i] > df['High'][i+1] \
  and df['High'][i+1] > df['High'][i+2] and df['High'][i-1] > df['High'][i-2] 

  return resistance

levels = []
levelsr = []
for i in range(2,df.shape[0]-2):
  if isSupport(df,i):
    levels.append((i,df['Low'][i]))
  elif isResistance(df,i):
    levelsr.append((i,df['High'][i]))
    

def plot_all():
  fig, ax = plt.subplots()

  candlestick_ohlc(ax,df.values,width=0.6, \
                   colorup='green', colordown='red', alpha=0.8)

  date_format = mpl_dates.DateFormatter('%d %b %Y')
  ax.xaxis.set_major_formatter(date_format)
  fig.autofmt_xdate()

  fig.tight_layout()

#  for level in levels:
#    plt.hlines(level[1],xmin=df['Date'][level[0]],\
#               xmax=max(df['Date']),colors='blue')
    
  for level in levelsr:
    plt.hlines(level[1],xmin=df['Date'][level[0]],\
               xmax=max(df['Date']),colors='orange')    
  fig.show()   
  
plot_all()



