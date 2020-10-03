# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 21:09:33 2020

@author: Marlon
"""

from pandas_datareader import data as web
import pandas as pd


prices = pd.DataFrame()
tickers = ['ITUB3.SA']
for i in tickers:
    prices = web.get_data_yahoo(i,'01/01/2008')
    

df = pd.DataFrame (columns = ['Fechamento','Variação', 'Variação (%)', 'Abertura', 'Máxima', 'Mínima','Volume'])
df['Date']= pd.to_datetime(prices.index) 
df['Fechamento']= prices['Close']
df['Variação']= 0
df['Variação (%)']= 0
df['Abertura']= prices['Open']
df['Máxima']= prices['High']
df['Mínima']= prices['Low']
df['Volume']= prices['Volume']

    
prices.rename(columns ={'ITUB3.SA':'ITUB', 'BBDC3.SA':'BBDC','BBAS3.SA':'BBAS','SANB3.SA':'SANB', '^BVSP':'IBOV'},inplace = True)
prices['IBOV'] = prices['IBOV']/1000
prices.reset_index(inplace = True)
prices.dropna(subset = ['IBOV'], inplace = True)