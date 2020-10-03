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

dffull = pd.read_csv(settings.workpath+'/tables/' +'irb-brasil-on-IRBR3.csv',sep=';' ,decimal= ',')

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

df = dffull

#df['Date'] = df['Date'].apply(mpl_dates.date2num)

df['Abertura'] = df['Abertura'].astype('float32')
df['Máxima'] = df['Máxima'].astype('float32')
df['Mínima'] = df['Mínima'].astype('float32')
df['Fechamento'] = df['Fechamento'].astype('float32')

df['suporte'] = False
df['resistencia'] = False


df = df.sort_values(by=['Date'], ascending=False)

df = df.head(150)

df = df.reset_index(drop=True)


def isSupport(df,i):
  support = df['Mínima'][i] < df['Mínima'][i-1]  and df['Mínima'][i] < df['Mínima'][i+1] \
  and df['Mínima'][i+1] < df['Mínima'][i+2] and df['Mínima'][i-1] < df['Mínima'][i-2]

  return support

def isResistance(df,i):
  resistance = df['Máxima'][i] > df['Máxima'][i-1]  and df['Máxima'][i] > df['Máxima'][i+1] \
  and df['Máxima'][i+1] > df['Máxima'][i+2] and df['Máxima'][i-1] > df['Máxima'][i-2] 

  return resistance

levels = []
levelsr = []
for i in range(2,df.shape[0]-2):
  if isSupport(df,i):
    df['suporte'][i] = True  
    levels.append((i,df['Mínima'][i]))
  elif isResistance(df,i):
    levelsr.append((i,df['Máxima'][i]))
    df['resistencia'][i] = True
    

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
    
#  for level in levelsr:
#    plt.hlines(level[1],xmin=df['Date'][level[0]],\
#               xmax=max(df['Date']),colors='orange')    
  fig.show()   
  
plot_all()



