# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 19:21:37 2020

@author: Marlon
"""
import requests

class TelBot:
    def telegram_bot_sendtext(self,bot_message):
        
        bot_token = '1317694242:AAH2RSWgayEpN0KZiTvKkl6rtahmIFtCzaM'
        bot_chatID = ['1234652974','1239460976']
        for idd in bot_chatID:
            send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + idd + '&parse_mode=Markdown&text=' + bot_message
            response = requests.get(send_text)
    
        return response.json()
    
    
    def send(self,message):        
        self.telegram_bot_sendtext(message)
        print(message)
