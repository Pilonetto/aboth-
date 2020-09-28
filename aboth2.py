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


baseUrl = '''https://br.advfn.com/bolsa-de-valores/bovespa/%s/historico/mais-dados-historicos?current=%d&Date1=%d/%d/%d&Date2=%d/%d/20'''


settings = Settings()
globais = Globals()
telbot = TelBot()

telbot.send('''Hello Sir, I am TAT - the action trader robot''' )


chromedriver = settings.workpath+'/chromedriver_linux64/chromedriver.exe'

options = webdriver.ChromeOptions()
options.add_argument('headless')

today = datetime.now()
driver = webdriver.Chrome(executable_path=chromedriver, options=options)

dfs = pd.read_csv(settings.planpath,sep=';' ,decimal= ',')

def update_all_tables():
    telbot.send('''Updated all tables ''')
    for index, row in dfs.iterrows(): 
        if row['empresa'] != 'SBSP3':
            continue
        action_name = row['table_code']
        
        telbot.send('''Updated data of: %s''' % (row['empresa']) )
        if (os.path.exists(settings.workpath+'/tables/' + action_name + '.csv')):
            df = pd.read_csv(settings.workpath+'/tables/' + action_name + '.csv',sep=';' ,decimal= ',')
            if df.empty:
                telbot.send('''%s table aready exist but is empty''' % (row['empresa']))
                lastday = 1
                lastmonth = 1
                lastyear = 18
            else:
                df['Date'] = pd.to_datetime(df.Data)
                mxDate = df['Date'].max()
                telbot.send('''%s table aready exist and max date is %s''' % (row['empresa'], mxDate))
                lastday = mxDate.day
                lastmonth = mxDate.month
                lastyear = mxDate.year -2000 # year in two digits
                imax = len(df)
        else:
            telbot.send('''Creating new table for %s ''' % (row['empresa']))
            df = pd.DataFrame (columns = ['Data',	'Fechamento','Variação', 'Variação (%)', 'Abertura', 'Máxima', 'Mínima','Volume'])
            imax = 0
            lastday = 1
            lastmonth = 1
            lastyear = 18
        okay = False;
        lastdt = ''
        for page in range(9):
            if (okay == True):
                telbot.send('Already acted, leaving out')
                break
            telbot.send('Looking for page: ' + str(page))
            
            driver = webdriver.Chrome(executable_path=chromedriver, options=options)            
            
            driver.get(baseUrl % (action_name,page, lastday,lastmonth,lastyear, today.day, today.month ))    
            baseTable = driver.find_elements_by_class_name("result");    
            for td in baseTable:
                arr = td.text.split(' ')
                dte = globais.fmt_date(arr[0], arr[1], arr[2])
                print(dte)
                print(lastdt)
                print('-------------')
                #if (dte == lastdt):
                #    okay = True
                #    break
                new_row = pd.Series({"Data": dte,  'Fechamento' : globais.fmt_float(arr[3]) ,'Variação': globais.fmt_float(arr[4]), 'Variação (%)' : globais.fmt_float(arr[5]), 'Abertura': globais.fmt_float(arr[6]) , 'Máxima': globais.fmt_float(arr[7]), 'Mínima': globais.fmt_float(arr[8]),'Volume': arr[9]})
                df.loc[imax] = new_row
                lastdt = dte
                imax += 1
            driver.stop_client()
            driver.close()    
            if len(baseTable) == 0:
                break
            
        df['Date'] = pd.to_datetime(df.Data)    
        df = df.drop_duplicates()
        df = df.reset_index(drop=True)
        df.to_csv(settings.workpath+'/tables/' + action_name + '.csv',sep=';' ,decimal= ',',index=False)      

def create_cols(df):
    cols = ['empresa','qtde','vl_pago','vl_atual','lucro_des','al_comprar','al_vender','status','profit','table_code', 'mme5', 'mme15', 'mme30','fxmin45','fxmax45', 'fxminrg','fxmaxrg']
    
    for col in cols:        
        if col not in df.columns:
            df[col] = 0
            
    return df
    
def update(tempo):
    driver = webdriver.Chrome(executable_path=chromedriver, options=options)
    
    baseUrldia = '''https://www.google.com/search?q=%s&rlz=1C1CHBD_pt-PTBR875BR875&oq=%s&aqs=chrome..69i57j0l7.1615j0j7&sourceid=chrome&ie=UTF-8'''
    df = pd.read_csv(settings.planpath,sep=';' ,decimal= ',')
    
    df = create_cols(df)
    
    df['status'] = df['status'].astype('int32')    
    #time.sleep(tempo)

    telbot.send('''  ''')    
    telbot.send('''  ''')    
    telbot.send('''  ''')    
    telbot.send('''These are your companies with updated values''')
    telbot.send('''  ''')      
    for index, row in df.iterrows(): 
        try:                            
            driver.get(baseUrldia % (row['empresa'],row['empresa']))
            data= driver.find_elements_by_xpath('//g-card-section/span')
            telbot.send((row['empresa'] + ': ' + data[0].text + ' -. Adic. Info: ' + data[1].text))
                  
            df.loc[df['empresa'] == row['empresa'], 'vl_atual'] = float(str(data[0].text).replace(',','.').replace(' BRL',''))
        except:
            telbot.send('''Error on update data of %s''' % (row['empresa']) )
    
    
    
        
    telbot.send('''  ''')    
    telbot.send('''  ''')    
    telbot.send('''  ''')    
    telbot.send(''' let's see what steps to take ''')
    telbot.send('''  ''')    
    for index, row in df.iterrows():
        
        if (int(row['status']) == 0):
            if (row['qtde'] == 0):                 
                df.loc[df['empresa'] == row['empresa'], 'profit'] = 0
            else:
                df.loc[df['empresa'] == row['empresa'], 'profit'] = row['vl_atual']  - row['vl_pago'] 
        else:            
            df.loc[df['empresa'] == row['empresa'], 'profit'] = 0    
        
        if (row['status'] == 0):
            if (row['profit'] > 0):
                telbot.send(row['empresa'] + ': current profit R$' + str(row['profit'] * row['qtde']))
            #else:
            #    telbot.send(row['empresa'] + ': is in harm')
            if (row['al_comprar'] > 0):
                if (row['vl_atual'] <=  row['al_comprar']):
                    telbot.send(row['empresa'] + ': This with indicative of purchase with the value: R$' + str(row['vl_atual']))
                    
                    
            if(row['al_vender'] > 0):
                if (row['vl_atual'] >=  row['al_vender']):
                    telbot.send(row['empresa'] + ': This with sales call with the value: R$' + str(row['vl_atual']))
        else:
            if (row['al_comprar'] > 0):
                if (row['vl_atual'] <=  row['al_comprar']):
                    telbot.send(row['empresa'] + ': This with indicative of purchase with the value: R$' + str(row['vl_atual']))            
                    
                    
        
        df.loc[df['empresa'] == row['empresa'], 'mme5'] = globais.performs_mme(settings, row['table_code'], 17)
        df.loc[df['empresa'] == row['empresa'], 'mme15'] = globais.performs_mme(settings, row['table_code'], 72)
        df.loc[df['empresa'] == row['empresa'], 'mme30'] = globais.performs_mme(settings, row['table_code'], 200)
        fxmin45,fxmax45, fxminrg,fxmaxrg = globais.performs_hitory(settings, row['table_code'])    
        df.loc[df['empresa'] == row['empresa'], 'fxmin45'] = fxmin45
        df.loc[df['empresa'] == row['empresa'], 'fxmax45'] = fxmax45
        df.loc[df['empresa'] == row['empresa'], 'fxminrg'] = fxminrg
        df.loc[df['empresa'] == row['empresa'], 'fxmaxrg'] = fxmaxrg
        
        
    df.to_csv(settings.planpath,sep=';' ,decimal= ',',index=False)  
    driver.stop_client()
    driver.close()
#update_all_tables()
    
while True:
    update(settings.interval)      