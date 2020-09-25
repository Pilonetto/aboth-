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


from sklearn.cluster import KMeans


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
df = pd.read_csv('D:/aboth-/tables/banco-do-brasil-on-BBAS3.csv',sep=';' ,decimal= ',')

df = df.head(75 + 12)

df['Mínima'] = df['Mínima'].astype('float32')


#apply clustering
kmeans = KMeans(n_clusters=4)
kmeans.fit(df[['Mínima']])
df['TotalCluster'] = kmeans.predict(df[['Mínima']])

df['TotalCluster'].describe()
#order the cluster numbers
dfclient = order_cluster('TotalCluster', 'Mínima',df,True)


dfTest = df[df['TotalCluster'] == 0]

print(dfTest['Mínima'].min())
