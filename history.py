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

from sklearn.cluster import KMeans


settings = Settings()
globais = Globals()


#function for ordering cluster numbers
def order_cluster(cluster_field_name, target_field_name,df,ascending):
    df_new = df.groupby(cluster_field_name)[target_field_name].mean().reset_index()
    df_new = df_new.sort_values(by=target_field_name,ascending=ascending).reset_index(drop=True)
    df_new['index'] = df_new.index
    df_final = pd.merge(df,df_new[[cluster_field_name,'index']], on=cluster_field_name)
    df_final = df_final.drop([cluster_field_name],axis=1)
    df_final = df_final.rename(columns={"index":cluster_field_name})
    return df_final


# Import CSV file into pandas dataframe
df = pd.read_csv(settings.workpath+'/tables/' +'ambev-s-a-on-ABEV3.csv',sep=';' ,decimal= ',')

df = df.head(45)

df['Fechamento'] = df['Fechamento'].astype('float32')

df = df.sort_values(by=['Date'], ascending=False)
df = df.reset_index(drop=True)
            

#apply clustering
kmeans = KMeans(n_clusters=4)
kmeans.fit(df[['Fechamento']])
df['TotalCluster'] = kmeans.predict(df[['Fechamento']])

df['TotalCluster'].describe()
#order the cluster numbers
dfclient = order_cluster('TotalCluster', 'Fechamento',df,True)


dfTest = dfclient['TotalCluster']
ax = dfTest.plot.hist(bins=12, alpha=0.5)
dfclient['TotalCluster']
dfclient['TotalCluster'] = dfclient['TotalCluster'].astype('int8')

idx = dfclient['TotalCluster'].value_counts()[dfclient['TotalCluster'].value_counts() == 23].index[0]

dfTest = dfclient[ dfclient.TotalCluster == idx]
print(df['Fechamento'].min())
print(df['Fechamento'].max())

print(dfTest['Fechamento'].min())
print(dfTest['Fechamento'].max())
