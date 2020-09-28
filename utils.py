import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.cluster import KMeans

class Globals:
    def order_cluster(self,cluster_field_name, target_field_name,df,ascending):
        df_new = df.groupby(cluster_field_name)[target_field_name].mean().reset_index()
        df_new = df_new.sort_values(by=target_field_name,ascending=ascending).reset_index(drop=True)
        df_new['index'] = df_new.index
        df_final = pd.merge(df,df_new[[cluster_field_name,'index']], on=cluster_field_name)
        df_final = df_final.drop([cluster_field_name],axis=1)
        df_final = df_final.rename(columns={"index":cluster_field_name})
        return df_final
    
    def month_name_to_num(self,month):
        if month == 'Jan':
            return '01'
        elif month == 'Fev':
            return '02'
        elif month == 'Mar':
            return '03'
        elif month == 'Abr':
            return '04'
        elif month == 'Mai':
            return '05'
        elif month == 'Jun':
            return '06'
        elif month == 'Jul':
            return '07'
        elif month == 'Ago':
            return '08'
        elif month == 'Set':
            return '09'
        elif month == 'Out':
            return '10'
        elif month == 'Nov':
            return '11'        
        else:
           return '12'
            
    def fmt_date(self, day, month, year):
        return self.month_name_to_num(month)+ '/'+ day  + '/'+ year
    
    def fmt_float(self, value):
        return value.replace(',','.')

    def save_mme(self,settings, name):
        
        dfmm = pd.read_csv(settings.workpath+'/tables/' +name +'.csv',sep=';' ,decimal= ',') 
        if dfmm.empty:
            print('No data')
        else:
            dfmm = dfmm.sort_values(by=['Date'], ascending=True)
            dfmm = dfmm.reset_index(drop=True)
                        
            dfmm['mme15'] = dfmm['Fechamento'].rolling(15).mean()
            dfmm['mme45'] = dfmm['Fechamento'].rolling(45).mean()
            dfmm['mme70'] = dfmm['Fechamento'].rolling(70).mean()
            dfmm = dfmm.sort_values(by=['Date'], ascending=False)
            dfmm = dfmm.reset_index(drop=True)
            
            
            dfmm.to_csv(settings.workpath+'/tables/' +name +'.csv',sep=';' ,decimal= ',')
        return
    
    def performs_mme(self,settings, name, window):
        
        dfmm = pd.read_csv(settings.workpath+'/tables/' +name +'.csv',sep=';' ,decimal= ',') 
        if dfmm.empty:
            res = 0
        else:
            dfmm = dfmm.sort_values(by=['Date'], ascending=True)
            dfmm = dfmm.reset_index(drop=True)
                        
            dfmm['mme'] = dfmm['Fechamento'].rolling(window).mean()
            dfmm = dfmm.sort_values(by=['Date'], ascending=False)
            dfmm = dfmm.reset_index(drop=True)
            dfmm = dfmm.iloc[[0]]
            res = dfmm['mme'].values[0]
            
        return res
    
    def analisys_mme(self,settings, name):
        res = 0
        dfmm = pd.read_csv(settings.workpath+'/tables/' +name +'.csv',sep=';' ,decimal= ',') 
        if dfmm.empty:
            res = 0
        else:
            dfmm = dfmm.sort_values(by=['Date'], ascending=False)
            dfmm = dfmm.reset_index(drop=True)
            
            ltmmm1 = dfmm[dfmm['Date'] == dfmm['Date'].max()].mme15.values[0]            
            ltmmm2 = dfmm[dfmm['Date'] == dfmm['Date'].max()].mme45.values[0]  
            ltmmm3 = dfmm[dfmm['Date'] == dfmm['Date'].max()].mme70.values[0]  
            
            if ltmmm1 < ltmmm2:
                if ltmmm2 < ltmmm3:
                    res = 0 #queda
                else:
                    res = 1 # assumir neutro por enquanto
            if ltmmm1 > ltmmm2:
                if ltmmm2 > ltmmm3:
                    res = 2 #Alta
                else:
                    res = 1 # assumir neutro por enquanto
            
            
        return res
    def performs_hitory(self,settings, name):
        df = pd.read_csv(settings.workpath+'/tables/' +name +'.csv',sep=';' ,decimal= ',') 
        if df.empty:
            return  0,0,0,0
        else:
            df = df.head(45)
            df['Fechamento'] = df['Fechamento'].astype('float32')
            df = df.sort_values(by=['Date'], ascending=False)
            df = df.reset_index(drop=True)
            #apply clustering
            #kmeans = KMeans(n_clusters=4)
            kmeans = KMeans(algorithm='auto', copy_x=True, init='k-means++', max_iter=300,
                   n_clusters=3, n_init=10, n_jobs=None, precompute_distances='auto',
                   random_state=0, tol=0.0001, verbose=0)
            kmeans.fit(df[['Fechamento']])
            df['TotalCluster'] = kmeans.predict(df[['Fechamento']])
            
            #order the cluster numbers
            dfclient = self.order_cluster('TotalCluster', 'Fechamento',df,True)
            
            
            idx = dfclient['TotalCluster'].value_counts()[dfclient['TotalCluster'].value_counts() == dfclient['TotalCluster'].value_counts().max()].index[0]

            dfTest = dfclient[ dfclient.TotalCluster == idx]            
            
            return df['Fechamento'].min(),df['Fechamento'].max(), dfTest['Fechamento'].min(), dfTest['Fechamento'].max()
            

        
        
        
        