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



baseUrl = '''https://br.advfn.com/bolsa-de-valores/bovespa/%s/historico/mais-dados-historicos?current=%d&Date1=%d/%d/%d&Date2=%d/%d/20'''


settings = Settings()
globais = Globals()

print('''Hello %s, I am the MA scraper robot''' % (settings.yourname))


chromedriver = settings.workpath+'/chromedriver_linux64/chromedriver.exe'

options = webdriver.ChromeOptions()
options.add_argument('headless')

today = datetime.now()
driver = webdriver.Chrome(executable_path=chromedriver, options=options)

dfs = pd.read_csv(settings.planpath,sep=';' ,decimal= ',')


print('''Updated all tables ''')
for index, row in dfs.iterrows(): 
    action_name = row['table_code']
    
    print('''Updated data of: %s''' % (row['empresa']) )
    if (os.path.exists(settings.workpath+'/tables/' + action_name + '.csv')):
        df = pd.read_csv(settings.workpath+'/tables/' + action_name + '.csv',sep=';' ,decimal= ',')
        if df.empty:
            lastday = 1
            lastmonth = 1
            lastyear = 2018
        else:
            df['Date'] = pd.to_datetime(df.Data)
            mxDate = df['Date'].max()
            lastday = mxDate.day
            lastmonth = mxDate.month
            lastyear = mxDate.year -2000 # year in two digits
            imax = len(df)
    else:
        df = pd.DataFrame (columns = ['Data',	'Fechamento','Variação', 'Variação (%)', 'Abertura', 'Máxima', 'Mínima','Volume'])
        imax = 0
    
    for page in range(9):
        print('Looking for page: ' + str(page))
        driver.get(baseUrl % (action_name,page, lastday,lastmonth,lastyear, today.day, today.month ))    
        baseTable = driver.find_elements_by_class_name("result");    
        for td in baseTable:
            arr = td.text.split(' ')
            dte = globais.fmt_date(arr[0], arr[1], arr[2])
            new_row = pd.Series({"Data": dte,  'Fechamento' : arr[3] ,'Variação': arr[4], 'Variação (%)' : arr[5], 'Abertura': arr[6] , 'Máxima': arr[7], 'Mínima': arr[8],'Volume': arr[9]})
            df.loc[imax] = new_row
            imax += 1
        if len(baseTable) == 0:
            break
        
    df = df.drop_duplicates()
    df = df.reset_index()
    df.to_csv(settings.workpath+'/tables/' + action_name + '.csv',sep=';' ,decimal= ',',index=False)      


def update(tempo):
    baseUrldia = '''https://www.google.com/search?q=%s&rlz=1C1CHBD_pt-PTBR875BR875&oq=%s&aqs=chrome..69i57j0l7.1615j0j7&sourceid=chrome&ie=UTF-8'''
    df = pd.read_csv(settings.planpath,sep=';' ,decimal= ',')
    
    time.sleep(tempo)

    print('''  ''')    
    print('''  ''')    
    print('''  ''')    
    print('''These are your companies with updated values''')
    print('''  ''')      
    for index, row in df.iterrows(): 
        driver.get(baseUrldia % (row['empresa'],row['empresa']))
        data= driver.find_elements_by_xpath('//g-card-section/span')
        print((row['empresa'] + ': ' + data[0].text + ' -. Adic. Info: ' + data[1].text))
              
        df.loc[df['empresa'] == row['empresa'], 'vl_atual'] = float(str(data[0].text).replace(',','.').replace(' BRL',''))
    
    
    
    if (row['status'] == 0):
        df['profit'] = df['vl_atual']  - df['vl_pago']  
        
    print('''  ''')    
    print('''  ''')    
    print('''  ''')    
    print(''' let's see what steps to take ''')
    print('''  ''')    
    for index, row in df.iterrows():
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
            
    df.to_csv(settings.planpath,sep=';' ,decimal= ',',index=False)  
    
while True:
    update(settings.interval)      