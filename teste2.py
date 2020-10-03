# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 14:58:47 2020

@author: marlon
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 14:25:38 2020

@author: marlon
"""

# import libraries
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from cfg import Settings
from utils import Globals



settings = Settings()
globais = Globals()


# Import CSV file into pandas dataframe
df = pd.read_csv(settings.workpath+'/tables/' +'magazine-luiza-on-MGLU3.csv',sep=';' ,decimal= ',')

if df.empty:
    print('Sem dados para análisar')
else:
    df = df[df['Date'] == df['Date'].max()]  
    padrao = df.iloc[0].tendencia
    analise = ''
    if padrao == -2:
        tend = 'Forte Queda'
    elif padrao == -1:
        tend = 'Queda'
    elif padrao == 0:
        tend = 'Normal'
    elif padrao == 1:
        tend = 'Alta'
    elif padrao == 2:
        tend = 'Forte Alta'
    
    analise = padrao + '\n'
    if df.iloc[0].diaalta15 > 0:
        analise += '''Os preços médios em um período menor estão maiores que os preços médios de um período maior, isso já vem ocorrendo à %d dias. \n ''' % (df.iloc[0].diaalta15)
        if df.iloc[0].diffal1545 > 0:
            analise += '''Além disso, a diferença da média menor para a média maior está aumentando à %d dia(s). Isso indica que os preços recentes estão mais altos! \n ''' % (df.iloc[0].diffal1545)
        if df.iloc[0].diffdim1545 > 0:
            analise += '''Porém, a diferença da média menor para a média maior está diminuindo à %d dia(s). Isso indica que os preços recentes estão mais baixos! \n''' % (df.iloc[0].diffdim1545)
    if df.iloc[0].diabaixa15 > 0:
        analise = '''Os preços médios em um período menor estão menores que os preços médios de um período maior, isso já vem ocorrendo à %d dias \n''' % (df.iloc[0].diaalta15)
        if df.iloc[0].diffal1545 > 0:
            analise += '''Além disso, a diferença da média menor para a média maior está aumentando à %d dia(s). Isso indica que os preços recentes estão mais baixos! \n''' % (df.iloc[0].diffal1545)
        if df.iloc[0].diffdim1545 > 0:
            analise += '''Porém, a diferença da média menor para a média maior está diminuindo à %d dia(s). Isso indica que os preços recentes estão mais altos! \n''' % (df.iloc[0].diffdim1545)
            
    if df.iloc[0].diasqueda > 0:
        analise += ''' Ainda é importante destacar que os preços estão fechando em queda à %d dia(s) \n ''' % (df.iloc[0].diasqueda)
    if df.iloc[0].diasalta > 0:
        analise += ''' Ainda é importante destacar que os preços estão fechando em alta à %d dia(s) \n ''' % (df.iloc[0].diasalta)            
        
    analise += 'Espero ter te ajudado'
            
globais.save_mme(settings,'aes-tiete-TIET11')


df = pd.read_csv(settings.workpath+'/tables/' +'magazine-luiza-on-MGLU3.csv',sep=';' ,decimal= ',')
#df = df.head(70)

df['diasqueda'] = 0
df['diasalta'] = 0
df['diabaixa15'] = 0
df['diaalta15'] = 0
df['15diff'] = df['mme15'] - df['mme45']
df['diffal1545'] = 0
df['diffdim1545'] = 0
df['tendencia'] = 'Sem tendência'

for i in range(len(df)):
    dias = 0  
    dias2 = 0 
    dias3 = 0 
    
    if (df['mme15'][i] <= df['mme45'][i] ):        
        for j in range(i,len(df)):
            if(df['mme15'][j] <= df['mme45'][j] ):
               dias += 1               
            else:                
                df.diabaixa15.iloc[i] = dias  
                dias = 0
                break
    dias = 0      
    if (df['mme15'][i] >= df['mme45'][i] ):        
        for j in range(i,len(df)):
            if(df['mme15'][j] >= df['mme45'][j] ):
               dias += 1               
            else:                
                df.diaalta15.iloc[i] = dias  
                dias = 0
                break        
            
    for j in range(i,len(df)-1):
        if(df['15diff'][j] > df['15diff'][j+1] ):
            dias += 1               
        else:                
            df.diffal1545.iloc[i] = dias  
            dias = 0
            break   
             
        
    for j in range(i,len(df)-1):
        if(df['15diff'][j] <= df['15diff'][j+1] ):
            dias += 1               
        else:                
            df.diffdim1545.iloc[i] = dias  
            dias = 0
            break       
        
    for j in range(i,len(df)-1):        
        if(df['Fechamento'][j] > df['Fechamento'][j+1] ):
            dias2 += 1               
        else:                
            df.diasalta.iloc[i] = dias2  
            dias2 = 0
            break   
    for j in range(i,len(df)-1):          
        if(df['Fechamento'][j] <= df['Fechamento'][j+1] ):
            dias3 += 1               
        else:                
            df.diasqueda.iloc[i] = dias3  
            dias3 = 0
            break   
    try: 
        #alta          
        if (df['mme15'][i] <= df['mme45'][i]):   
            if (df['mme15'][i] > df['mme15'][i+1]) & (df['mme15'][i] > df['mme15'][i+2]) & (df['mme15'][i] > df['mme15'][i+3]):   # a tendencia só se confirma se o valor não estiver caindo
                if(df['diabaixa15'][i] >= 3) & (df['diffdim1545'][i] >= 3) :
                    df.tendencia.iloc[i] = 'Fraca tendência de alta - 01'  
                if(df['diabaixa15'][i] >= 6) & (df['diffdim1545'][i] >= 6):
                    df.tendencia.iloc[i] = 'Forte tendência de alta  - 01'         
        if (df['mme15'][i] > df['mme45'][i]):    
            if (df['mme15'][i] > df['mme15'][i+1]) & (df['mme15'][i] > df['mme15'][i+2]) & (df['mme15'][i] > df['mme15'][i+3]):   # a tendencia só se confirma se o valor não estiver caindo
                if(df['diaalta15'][i] >= 3) & (df['diffal1545'][i] >= 3):
                    df.tendencia.iloc[i] = 'Fraca tendência de alta - 02'  
                if(df['diffal1545'][i] >= 6) & (df['diffal1545'][i] >= 6):
                    df.tendencia.iloc[i] = 'Forte tendência de alta  - 02'        
                
        if(df['diasqueda'][i] >= 3) :
            df.tendencia.iloc[i] = str(df['diasqueda'][i]) + ' dias consecutivos de queda'
        
       #Queda 
        if (df['mme15'][i] <= df['mme45'][i]):   
            if (df['mme15'][i] < df['mme15'][i+1]) & (df['mme15'][i] < df['mme15'][i+2]) & (df['mme15'][i] < df['mme15'][i+3]):   # a tendencia só se confirma se o valor não estiver caindo
                print('caindo a 3 dias',i)
                if(df['diabaixa15'][i] >= 3) & (df['diffal1545'][i] >= 3) :
                    df.tendencia.iloc[i] = 'Fraca tendência de queda - 01'  
                if(df['diabaixa15'][i] >= 6) & (df['diffal1545'][i] >= 6):
                    df.tendencia.iloc[i] = 'Forte tendência de queda  - 01'         
        if (df['mme15'][i] > df['mme45'][i]):    
            if (df['mme15'][i] < df['mme15'][i+1]) & (df['mme15'][i] < df['mme15'][i+2]) & (df['mme15'][i] < df['mme15'][i+3]):   # a tendencia só se confirma se o valor não estiver caindo
                print('caindo a 3 dias')
                if(df['diaalta15'][i] >= 3) & (df['difdim1545'][i] >= 3):
                    df.tendencia.iloc[i] = 'Fraca tendência de queda - 02'  
                if(df['diffal1545'][i] >= 6) & (df['difdim1545'][i] >= 6):
                    df.tendencia.iloc[i] = 'Forte tendência de queda  - 02'        
                
        if(df['diasqueda'][i] >= 3) :
            df.tendencia.iloc[i] = str(df['diasqueda'][i]) + ' dias consecutivos de queda'            
            
            
    except:
        df.tendencia.iloc[i] = 'Sem tendencia'

dffinal = df[['Date', 'tendencia']].head(200)    