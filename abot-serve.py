# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 20:00:18 2020

@author: Marlon
"""

from flask_cors import CORS
from flask_restful import Resource, Api
from flask import Flask, redirect, url_for, request
import json
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
import threading



def f(tempo):    
        
    time.sleep(tempo)

      
    x = threading.Thread(target=f, args=(interval,)) 
    x.start()        
    
interval = 300 # 5 minutos
#x = threading.Thread(target=f, args=(interval,)) 
#x.start()



class BotEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(BotEncoder, self).default(obj)
        
settings = Settings()
app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/empresas',methods = ['GET'])
def empresas():
    if request.method == 'GET':        
        try:            
            df = pd.read_csv(settings.planpath,sep=';' ,decimal= ',')
            df = df['empresa']
            return json.dumps(df.to_json(orient = 'index'), cls=BotEncoder) 
              
          
        except:
            return  json.dumps({'test':False})          


@app.route('/addativo/<nome>',methods = ['GET'])
def addativo(nome):
    if request.method == 'GET':        
        try:                   
            df = pd.read_csv(settings.planpath,sep=';' ,decimal= ',')
            dic = {'empresa': nome,'qtde':0,'vl_pago':0,'vl_atual':0,'lucro_des':0,'al_comprar':0,'al_vender':0,'status':0,'profit':0,
            'table_code':nome, 'mme5':0, 'mme15':0, 'mme30':0,'fxmin45':0,'fxmax45':0, 'fxminrg':0,'fxmaxrg':0, 'aberturadia':0, 'minimadia':0, 'maximadia':0,'stsmme':0}
            
            df = df.append(dic, ignore_index=True) 
            
            df.to_csv(settings.planpath,sep=';' ,decimal= ',',index=False)  
            
            return json.dumps({'test':True})
        except:
            return  json.dumps({'test':False})
        
@app.route('/addqtde/<nome>/<qtde>/<preco>',methods = ['GET'])
def addqtde(nome, qtde,preco):
    if request.method == 'GET':        
        try:                   
            df = pd.read_csv(settings.planpath,sep=';' ,decimal= ',')
            
            qt = df.loc[df['empresa'] == nome].qtde.values[0]
            vl = df.loc[df['empresa'] == nome].vl_pago.values[0]
            
            vl = vl * qt
            vl2 = float(preco) * int(qtde)
            
            vl = (vl + vl2) / (qt + int(qtde))
                        
            df.loc[df['empresa'] == nome, 'qtde'] = (qt + int(qtde))
            df.loc[df['empresa'] == nome, 'vl_pago'] = vl
            df.loc[df['empresa'] == nome, 'dtacompra'] = pd.to_datetime(datetime.today())        
                        
            
            df.to_csv(settings.planpath,sep=';' ,decimal= ',',index=False)  
            
            return json.dumps({'test':True})
        except:
            return  json.dumps({'test':False})
        
        
@app.route('/mediamovel/<empresa>',methods = ['GET'])
def mediamovel(empresa):
    if request.method == 'GET':        
        try:            
            df = pd.read_csv(settings.planpath,sep=';' ,decimal= ',')
            
            code = df.loc[df['empresa'] == empresa].table_code.values[0]

            dfdados = pd.read_csv(settings.workpath+'/tables/' + code + '.csv',sep=';' ,decimal= ',')

            dfdados = dfdados[['Date', 'mme15','mme45', 'mme70']]
            
            dfdados = dfdados.head(200)

            return json.dumps(dfdados.to_json(orient = 'index'), cls=BotEncoder) 
              
          
        except:
            return  json.dumps({'test':False})          


@app.route('/cotacoes',methods = ['GET'])
def cotacoes():
    if request.method == 'GET':        
        try:            
            df = pd.read_csv(settings.planpath,sep=';' ,decimal= ',')   
            df['qtde'] = df['qtde'].astype('float32')
            df = df.sort_values(by=['qtde'], ascending=False)
            df = df.reset_index(drop=True)
            return json.dumps(df.to_json(orient = 'index'), cls=BotEncoder) 
              
          
        except:
            return  json.dumps({'test':False}) 
        


@app.route('/test',methods = ['GET'])
def test():
    if request.method == 'GET':        
        try:            
          return json.dumps({'test':True})  
              
          
        except:
            return  json.dumps({'test':False})          
    
if __name__ == '__main__':
   app.run(port = 4321,host='0.0.0.0',threaded=True)

