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

