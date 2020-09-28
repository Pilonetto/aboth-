import configparser

class Settings:
    def __init__(self):        
        config =  configparser.ConfigParser()
        config.read("bothoptions.ini")
        
        dConfig = config.__dict__['_sections'].copy()
        
        
        try:
            self.planpath = dConfig['general']['planpath']
            
            #self.plantath = self.plantath.replace('\\' , '//')
        except:
            self.planpath = ''


        try:
            self.workpath = dConfig['general']['workpath']
            
            #self.plantath = self.plantath.replace('\\' , '//')
        except:
            self.workpath = ''
            
        try:
            self.interval = int(dConfig['general']['interval'])
        except:
            self.interval = 30      
            
        try:
            self.yourname = str(dConfig['general']['yourname'])
        except:
            self.yourname = 'Strange'      
            
