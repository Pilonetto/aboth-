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
                        
            dfmm['mm15'] = dfmm['Fechamento'].rolling(15).mean()
            dfmm["mme15"] = pd.Series.ewm(dfmm["Fechamento"], span=15).mean()
            dfmm['mm45'] = dfmm['Fechamento'].rolling(45).mean()
            dfmm["mme45"] = pd.Series.ewm(dfmm["Fechamento"], span=45).mean()
            dfmm['mm70'] = dfmm['Fechamento'].rolling(70).mean()
            dfmm["mme70"] = pd.Series.ewm(dfmm["Fechamento"], span=70).mean()
            
            dfmm = dfmm.sort_values(by=['Date'], ascending=False)
            dfmm = dfmm.reset_index(drop=True)
            
            
            dfmm.to_csv(settings.workpath+'/tables/' +name +'.csv',sep=';' ,decimal= ',',index=False)
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
    
    def tendence_mme(self,settings, name):
        print('''Analyzing patterns of %s ''' % name)
        df = pd.read_csv(settings.workpath+'/tables/' +name +'.csv',sep=';' ,decimal= ',') 
        if df.empty:
            padrao = 0
            warning = ''
        else:
            TEND_NONE = 0
            TEND_ALTA1 = 1
            TEND_ALTA2 = 2
            TEND_QUEDA1 = -1
            TEND_QUEDA2 = -2
            
            df['diasqueda'] = 0
            df['diasalta'] = 0
            df['diabaixa15'] = 0
            df['diaalta15'] = 0
            df['15diff'] = abs(df['mme15'] - df['mme45'])
            df['diffal1545'] = 0
            df['diffdim1545'] = 0
            df['tendencia'] = TEND_NONE
            df['atencao'] = 'Nada a acrescentar'
            
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
                                df.tendencia.iloc[i] = TEND_ALTA1  
                            if(df['diabaixa15'][i] >= 6) & (df['diffdim1545'][i] >= 6):
                                df.tendencia.iloc[i] = TEND_ALTA2        
                    if (df['mme15'][i] > df['mme45'][i]):    
                        if (df['mme15'][i] > df['mme15'][i+1]) & (df['mme15'][i] > df['mme15'][i+2]) & (df['mme15'][i] > df['mme15'][i+3]):   # a tendencia só se confirma se o valor não estiver caindo
                            if(df['diaalta15'][i] >= 3) & (df['diffal1545'][i] >= 3):
                                df.tendencia.iloc[i] = TEND_ALTA1  
                            if(df['diffal1545'][i] >= 6) & (df['diffal1545'][i] >= 6):
                                df.tendencia.iloc[i] = TEND_ALTA2        
                            
                    
                    
                   #Queda 
                    if (df['mme15'][i] <= df['mme45'][i]):   
                        if (df['mme15'][i] < df['mme15'][i+1]) & (df['mme15'][i] < df['mme15'][i+2]) & (df['mme15'][i] < df['mme15'][i+3]):   # a tendencia só se confirma se o valor não estiver caindo
                            if(df['diabaixa15'][i] >= 3) & (df['diffal1545'][i] >= 3) :
                                df.tendencia.iloc[i] = TEND_QUEDA1  
                            if(df['diabaixa15'][i] >= 6) & (df['diffal1545'][i] >= 6):
                                df.tendencia.iloc[i] = TEND_QUEDA2         
                    if (df['mme15'][i] > df['mme45'][i]):    
                        if (df['mme15'][i] < df['mme15'][i+1]) & (df['mme15'][i] < df['mme15'][i+2]) & (df['mme15'][i] < df['mme15'][i+3]):   # a tendencia só se confirma se o valor não estiver caindo            
                            if(df['diaalta15'][i] >= 3) & (df['diffdim1545'][i] >= 3):
                                df.tendencia.iloc[i] = TEND_QUEDA1  
                            if(df['diffal1545'][i] >= 6) & (df['diffdim1545'][i] >= 6):
                                df.tendencia.iloc[i] = TEND_QUEDA2       
                            
                    if(df['diasqueda'][i] >= 3) :
                        df.atencao.iloc[i] = str(df['diasqueda'][i]) + ' dias consecutivos de queda'
                    if(df['diasalta'][i] >= 3) :
                        df.atencao.iloc[i] = str(df['diasqueda'][i]) + ' dias consecutivos de alta'               
                        
                        
                except:
                    df.tendencia.iloc[i] = TEND_NONE
                    
        padrao = df[df['Date'] == df['Date'].max()].tendencia.values[0]  
        warning = df[df['Date'] == df['Date'].max()].atencao.values[0]     
        df.to_csv(settings.workpath+'/tables/' +name +'.csv',sep=';' ,decimal= ',',index=False)
        
        return padrao,warning    
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
            

        
        
        
        