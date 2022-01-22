from datetime import datetime
import requests
import threading
import json
import time
import os
from stableMemory import loadJsonFile, saveData
import traceback

class Agregator():
    def __init__(self,id):        
        self.aggregator_id = id
        self.database_folder = self.aggregator_id + '_database'
        os.system('mkdir ' + self.database_folder)
        self.path_sensor_metaData = './' + str(id) + '.json'
        self.sensors_list = loadJsonFile(self.path_sensor_metaData)        
        self.sensor_data_agg1 = []
        self.sensor_data_agg2 = []
        self.thread_send = threading.Thread(target=self.sendSLOT)
        self.thread_receive = threading.Thread(target=self.receiveSensor)     
        self.timer = 5

        if self.aggregator_id =="agg1":
            #create config json file aggregat
            saveData(self.database_folder+"/"+ str(id) + '.json',[
            {"name":"Hygrometer","type":"Humidity","freq":3,"unite":"%","localisation":"Rangueil"},
            {"name":"Thermometer1","type":"Heat","freq":2.6,"unite":"C°","localisation":"Rangueil"}
            ])
        elif self.aggregator_id =="agg2":
            saveData(self.database_folder+"/"+ str(id) + '.json',[
            {"name":"Thermometer2","type":"Heat","freq":1.9,"unite":"C°","localisation":"Rangueil"},
            {"name":"Barometer","type":"Air pressure","freq":0.4,"unite":"mbar","localisation":"Rangueil"}
            ])

    def receiveSensor(self):
        while True:
            try:
                url = 'http://localhost:5000/sensor_config'+str(self.aggregator_id)        
                reponse = requests.get(url) 
                sensor_info = reponse.text
                            
                if sensor_info != '': 
                    
                    try:  
                        sensor_info = json.loads(sensor_info)                    
                    except:
                        print("TEST errrrrrrrrrrrrrrrrrror")
                    
                print("Configuration des capteurs de l'agg "+str(self.aggregator_id)+ " : " + sensor_info)
                    
                    
                url = 'http://localhost:5000/sensor_data'+str(self.aggregator_id)        
                reponse = requests.get(url)
                data = reponse.text            
                if data != '':  
                    try:  
                        data = json.loads(data)
                    except:
                        print("errrrrrrrrrrrrrrrrrreeeuuuur")
                    print("Data des capteurs de l'agg "+str(self.aggregator_id)+ " : " + data) 
                    data = json.loads(data)                

                    receive_date = datetime.now().strftime("%d/%m/%Y")
                    receive_time = datetime.now().strftime("%H:%M:%S")
                    
                    data_info = {"date":receive_date,"time":receive_time,"value":data,"config":sensor_info}
                    try: 
                        if(self.aggregator_id == "agg1"):
                            self.sensor_data_agg1.append(data[0]["data"])
                            self.sensor_data_agg1.append(data[1]["data"])
                        elif(self.aggregator_id == "agg2"):
                            self.sensor_data_agg2.append(data[0]["data"])
                            self.sensor_data_agg2.append(data[1]["data"])
                    except:
                        traceback.print_exc()                    
                    saveData('./' + self.database_folder +'/'+ str(self.aggregator_id) + 'data.json', data_info)    
                        
            except:
                traceback.print_exc()    
            self.start_timer(self.timer)

    def sendSLOT(self):
        while(True):
            self.start_timer(60) # send last received data to the slot client each minute 
            if(self.aggregator_id =="agg1"):
                #ENVOI DES DONNEES A L API                                                                  
                url = 'http://localhost:5000/slot_client'
                payload = {'sender': self.aggregator_id,'message':json.dumps(self.sensor_data_agg1) ,'metadata': {}}
                headers = {'Content-Type': 'application/json'}
                requests.post(url, data=json.dumps(payload), headers=headers)
                self.sensor_data_agg1.clear()
            elif(self.aggregator_id == "agg2") :
                #ENVOI DES DONNEES A L API                                                                  
                url = 'http://localhost:5000/slot_client'
                payload = {'sender': self.aggregator_id,'message':json.dumps(self.sensor_data_agg2) ,'metadata': {}}
                headers = {'Content-Type': 'application/json'}
                requests.post(url, data=json.dumps(payload), headers=headers)       
                self.sensor_data_agg2.clear()                  
        
    def start_timer(self,t):
        time.sleep(t)   
    
    def start_threads(self):        
        self.thread_send.start()
        self.thread_receive.start()
        