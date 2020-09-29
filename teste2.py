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
df = pd.read_csv(settings.workpath+'/tables/' +'aes-tiete-TIET11.csv',sep=';' ,decimal= ',')

globais.save_mme(settings,'aes-tiete-TIET11')


df = pd.read_csv(settings.workpath+'/tables/' +'aes-tiete-TIET11.csv',sep=';' ,decimal= ',')
#df = df.head(70)

df['diasqueda'] = 0
df['diasalta'] = 0
df['diabaixa15'] = 0
df['diaalta15'] = 0
df['15diff'] = df['mme15'] - df['mme45']
df['diffal1545'] = 0
df['diffdim1545'] = 0


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