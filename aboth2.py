# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 15:50:49 2020

@author: marlon
"""

from selenium import webdriver
import time
import pandas as pd
import base64
import os
import numpy as np 
from datetime import datetime
from sqlalchemy import create_engine
from random import randint
from cfg import Settings
from utils import Globals
from telbot import TelBot
from pandas_datareader import data as web
import schedule



baseUrl = '''https://br.advfn.com/bolsa-de-valores/bovespa/%s/historico/mais-dados-historicos?current=%d&Date1=%d/%d/%d&Date2=%d/%d/20'''

        

settings = Settings()
globais = Globals()
telbot = TelBot()

print('''Hello Sir, I am TAT - the action trader robot''' )

chromedriver = settings.workpath+'/chromedriver_linux64/chromedriver.exe'

options = webdriver.ChromeOptions()
options.add_argument('headless')

today = datetime.now()

#dfs = pd.read_csv(settings.planpath,sep=';' ,decimal= ',')


def create_table(name, action_name):
    print('''Getting data of: %s''' % (name) )
    prices = pd.DataFrame()
    tickers = [name+ '.SA']
        #tickers = ['KLBN3' + '.SA']
    for i in tickers:
        prices = web.get_data_yahoo(i,'01/01/2018')
            
    prices.rename(columns ={'Close':'Fechamento', 'Open':'Abertura','High':'Máxima','Low':'Mínima'},inplace = True)
    prices['Date'] = pd.to_datetime(prices.index) 
    prices = prices.reset_index(drop=True)
    prices.to_csv(settings.workpath+'/tables/' + action_name + '.csv',sep=';' ,decimal= ',',index=False)   
    

    
def create_cols(df):
    cols = ['empresa','qtde','vl_pago','vl_atual','lucro_des','al_comprar','al_vender','status','profit',
            'table_code', 'mme5', 'mme15', 'mme30','fxmin45','fxmax45', 'fxminrg','fxmaxrg', 'aberturadia',
            'minimadia', 'maximadia','stsmme','obsmme', 'dtacompra', 'bloqueada',
            'stoploss','notsl', 'stopgainpart', 'notsgp', 'stopgaintot', 'notsgt','analisys']
    
    for col in cols:        
        if col not in df.columns:
            df[col] = 0
            
    return df
    
def refresh_tables(dfs):
    print('''Refresh tables ''')    
    for index, row in dfs.iterrows(): 
        
        action_name = row['table_code']   
        if (os.path.exists(settings.workpath+'/tables/' + action_name + '.csv')):             
            df = pd.read_csv(settings.workpath+'/tables/' +action_name +'.csv',sep=';' ,decimal= ',') 
        else:
            df = pd.DataFrame()
            
        if df.empty:
            create_table(row['empresa'], action_name)
        else:
            print('''Refreshing data of: %s''' % (row['empresa']) )       
            mx = df[df['Date'] == df['Date'].max()].Date.values[0] 
            prices = web.get_data_yahoo(row['empresa']+ '.SA',mx)
            #prices = web.get_data_yahoo('CIEL3'+ '.SA',mx)
            prices.rename(columns ={'Close':'Fechamento', 'Open':'Abertura','High':'Máxima','Low':'Mínima'},inplace = True)
            prices['Date'] = pd.to_datetime(prices.index) 
            df['Date'] = pd.to_datetime(df['Date'] )
            prices = prices.reset_index(drop=True)            
            df = pd.concat([df, prices], axis=0, join='outer', ignore_index=True, keys=None,
                          levels=None, names=None, verify_integrity=False, copy=True)    
            df = df.drop_duplicates(subset=['Date'], keep='first')
            df = df.sort_values(by=['Date'], ascending=False)
            df = df.reset_index(drop=True)  
            df.to_csv(settings.workpath+'/tables/' + action_name + '.csv',sep=';' ,decimal= ',',index=False)   
            mx_ = pd.to_datetime(df[df['Date'] == df['Date'].max()].Date.values[0])
            mx__ = pd.to_datetime(datetime.today())
            if mx__.strftime("%m/%d/%Y") == mx_.strftime("%m/%d/%Y"):
                idx = df[df['Date'] == df['Date'].max()].index[0]                
                dfs.loc[dfs['empresa'] == row['empresa'], 'vl_atual'] = df['Fechamento'][idx]
                dfs.loc[dfs['empresa'] == row['empresa'], 'aberturadia'] = df['Abertura'][idx]
                dfs.loc[dfs['empresa'] == row['empresa'], 'maximadia'] = df['Máxima'][idx]
                dfs.loc[dfs['empresa'] == row['empresa'], 'minimadia'] = df['Mínima'][idx]     
    
    return dfs    

def new_update_tables(dfs):
    print('''Updated all tables ''')
    for index, row in dfs.iterrows(): 
        create_table(row['empresa'], row['table_code'] )
        
          

def update():
    
    df = pd.read_csv(settings.planpath,sep=';' ,decimal= ',')
    
    df = create_cols(df)
    
    df['status'] = df['status'].astype('int32')    
    df['qtde'] = df['qtde'].astype('int32')
    

    print('''  ''')    
    print('''  ''')    
    print('''  ''')    
    print('''These are your companies with updated values''')
    print('''  ''')      
    df = refresh_tables(df)
#    for index, row in df.iterrows(): 
#        try:                            
#            driver.get(baseUrldia % (row['empresa'],row['empresa']))
#            data= driver.find_elements_by_xpath('//g-card-section/span')
#            print((row['empresa'] + ': ' + data[0].text + ' -. Adic. Info: ' + data[1].text))                  
#            df.loc[df['empresa'] == row['empresa'], 'vl_atual'] = float(str(data[0].text).replace(',','.').replace(' BRL',''))
            
#            precos = driver.find_elements_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "iyjjgb", " " ))]')
#            df.loc[df['empresa'] == row['empresa'], 'aberturadia'] = float(str(precos[0].text).replace(',','.'))
#            df.loc[df['empresa'] == row['empresa'], 'maximadia'] = float(str(precos[1].text).replace(',','.'))
#            df.loc[df['empresa'] == row['empresa'], 'minimadia'] = float(str(precos[2].text).replace(',','.'))             
#            
#        except:
#            print('''Error on update data of %s''' % (row['empresa']) )
    
    
    
        
    print('''  ''')    
    print('''  ''')    
    print('''  ''')    
    print(''' let's see what steps to take ''')
    print('''  ''')    
    for index, row in df.iterrows():
        try:
            if (row['qtde'] > 0):
                df.loc[df['empresa'] == row['empresa'], 'status'] = 0  
                
            if (int(row['status']) == 0):
                if (row['qtde'] == 0):                 
                    df.loc[df['empresa'] == row['empresa'], 'profit'] = 0
                else:
                    df.loc[df['empresa'] == row['empresa'], 'profit'] = row['vl_atual']  - row['vl_pago'] 
            else:            
                df.loc[df['empresa'] == row['empresa'], 'profit'] = 0    
            
            if (row['status'] == 0):
                if (row['profit'] > 0):
                    print(row['empresa'] + ': current profit R$' + str(row['profit'] * row['qtde']))
                #else:
                #    print(row['empresa'] + ': is in harm')
                if (row['al_comprar'] > 0):
                    if (row['vl_atual'] <=  row['al_comprar']):
                        print(row['empresa'] + ': This with indicative of purchase with the value: R$' + str(row['vl_atual']))
                        
                        
                if(row['al_vender'] > 0):
                    if (row['vl_atual'] >=  row['al_vender']):
                        print(row['empresa'] + ': This with sales call with the value: R$' + str(row['vl_atual']))
            else:
                if (row['al_comprar'] > 0):
                    if (row['vl_atual'] <=  row['al_comprar']):
                        print(row['empresa'] + ': This with indicative of purchase with the value: R$' + str(row['vl_atual']))            
                        
            
            globais.save_mme(settings, row['table_code'])    
            padrao, atencao = globais.tendence_mme(settings, row['table_code']) 
            analisys = globais.bot_analisys(settings, row['table_code'])
            df.loc[df['empresa'] == row['empresa'], 'analisys'] = analisys
            
            if (True): # Executar sómente quando executa a primeira vez
                if (row['stsmme'] != padrao):
                    telbot.send(''' %s mudou o padrão de %s para %s''' % (row['empresa'],globais.padrao_to_str(row['stsmme']),globais.padrao_to_str(padrao) ));  
                      
                if (row['obsmme'] != atencao):
                    telbot.send('''Observação sobre %s, %s''' % (row['empresa'],atencao )); 
            if (row['qtde'] > 0):    
                dif = 100 -((row['vl_pago'] * 100) / row['vl_atual'])
            
                if (dif < -2.5):
                    df.loc[df['empresa'] == row['empresa'], 'stoploss'] = 1
                    if df.loc[df['empresa'] == row['empresa']].notsl.values[0] == 0:
                        df.loc[df['empresa'] == row['empresa'], 'notsl'] = 1    
                        telbot.send('''Stop Loss para %s ''' % (row['empresa'])); 
                        #telbot.send('''Silenciando notificações de Stop Loss para %s ''' % (row['empresa'])); 
                else:
                    df.loc[df['empresa'] == row['empresa'], 'stoploss'] = 0
                    df.loc[df['empresa'] == row['empresa'], 'notsl'] = 0                 
                    #telbot.send('''Reiniciando notificações de Stop Loss para %s ''' % (row['empresa'])); 
                
                if (dif >= 2.5) & (dif < 10):
                    df.loc[df['empresa'] == row['empresa'], 'stopgainpart'] = 1
                    if df.loc[df['empresa'] == row['empresa']].notsgp.values[0] == 0:
                        df.loc[df['empresa'] == row['empresa'], 'notsgp'] = 1                        
                        telbot.send('''Saída parcial para %s ''' % (row['empresa'])); 
                else:
                    df.loc[df['empresa'] == row['empresa'], 'stopgainpart'] = 0
                    df.loc[df['empresa'] == row['empresa'], 'notsgp'] = 0  
                    
                if (dif >= 10):
                    df.loc[df['empresa'] == row['empresa'], 'stopgaintot'] = 1
                    if df.loc[df['empresa'] == row['empresa']].notsgt.values[0] == 0:
                        df.loc[df['empresa'] == row['empresa'], 'notsgt'] = 1                        
                        telbot.send('''Saída total para %s ''' % (row['empresa'])); 
                else:
                    df.loc[df['empresa'] == row['empresa'], 'stopgaintot'] = 0
                    df.loc[df['empresa'] == row['empresa'], 'notsgt'] = 0                  
                    
            df.loc[df['empresa'] == row['empresa'], 'stsmme'] = padrao
            df.loc[df['empresa'] == row['empresa'], 'obsmme'] = atencao
            
            #df.loc[df['empresa'] == row['empresa'], 'mme5'] = globais.performs_mme(settings, row['table_code'], 17)
            #df.loc[df['empresa'] == row['empresa'], 'mme15'] = globais.performs_mme(settings, row['table_code'], 72)
            #df.loc[df['empresa'] == row['empresa'], 'mme30'] = globais.performs_mme(settings, row['table_code'], 200)
            #fxmin45,fxmax45, fxminrg,fxmaxrg = globais.performs_hitory(settings, row['table_code'])    
            df.loc[df['empresa'] == row['empresa'], 'fxmin45'] = 0#fxmin45
            df.loc[df['empresa'] == row['empresa'], 'fxmax45'] = 0#fxmax45
            df.loc[df['empresa'] == row['empresa'], 'fxminrg'] = 0#fxminrg
            df.loc[df['empresa'] == row['empresa'], 'fxmaxrg'] = 0#fxmaxrg
        except:
            print('Falha ao processar alguns dados')
            continue

    
    #sincroniza os dfs
    dfupdates = pd.read_csv(settings.planpath,sep=';' ,decimal= ',')            
    dfupdates = create_cols(dfupdates)
    for index, row in dfupdates.iterrows():        
        if row['empresa'] not in pd.Series(df['empresa']).values:
            df = df.append(row, ignore_index=True) 
        df.loc[df['empresa'] == row['empresa'], 'qtde'] = row['qtde']
        df.loc[df['empresa'] == row['empresa'], 'vl_pago'] = row['vl_pago']
        df.loc[df['empresa'] == row['empresa'], 'dtacompra'] = row['dtacompra']
        
        if (df.loc[df['empresa'] == row['empresa']].dtacompra.values[0] == '0') | (df.loc[df['empresa'] == row['empresa']].dtacompra.values[0] == 0):
            df.loc[df['empresa'] == row['empresa'], 'bloqueada'] = False
        else:
            try:
                mx_ = pd.to_datetime(df.loc[df['empresa'] == row['empresa']].dtacompra.values[0])
                mx__ = pd.to_datetime(datetime.today())
                df.loc[df['empresa'] == row['empresa'], 'bloqueada'] = mx__.strftime("%m/%d/%Y") == mx_.strftime("%m/%d/%Y")
            except:
                df.loc[df['empresa'] == row['empresa'], 'bloqueada'] = False
                print('Falha ao converter data')
     
    for index, row in df.iterrows():
         if row['empresa'] not in pd.Series(dfupdates['empresa']).values:
             df = df[df.empresa != row['empresa']]
         
        
    
    df.to_csv(settings.planpath,sep=';' ,decimal= ',',index=False)  
    
df = pd.read_csv(settings.planpath,sep=';' ,decimal= ',')    
new_update_tables(df)

def open_market():    
    telbot.send('Bom diaaa! O mercado já vai abrir ;)''');

def close_market():
    telbot.send('O mercado fechou! Bom descanso :)''');                
    
    

schedule.every().day.at("09:55").do(open_market)
schedule.every().day.at("17:01").do(close_market)
#schedule.every(15).minutes.do(update)   
while True:
    schedule.run_pending()
    time.sleep(1)
    update() 
    #firstExec = False     