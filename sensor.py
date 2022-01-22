import threading
import time
from random import uniform
import json
import requests


class VirtualSensor() : 
    def __init__(self,sensor_id,data_type,sensor_rate,measurement_unit,geolocalisation):
       
        self.sensor_id = sensor_id
        self.data_type =data_type
        self.sensor_rate = sensor_rate # rate (Hz)
        self.measurement_unit = measurement_unit       
        self.geolocalisation = geolocalisation       
        self.thread_send = threading.Thread(target=self.send)
    def send(self):
        sensor_info = json.dumps({'id':self.sensor_id,'type':self.data_type,'rate':self.sensor_rate,'unit':self.measurement_unit,'geolocalisation':self.geolocalisation})
        while True:                
                try:
                    #ENVOI DES DONNEES A L API                                                                  
                    url = 'http://localhost:5000/sensor_config'
                    payload = {'sender': self.sensor_id,'message':sensor_info ,'metadata': {}}
                    headers = {'Content-Type': 'application/json'}
                    requests.post(url, data=json.dumps(payload), headers=headers)                   
                    time.sleep(1)
                   
                    self.data = ''                    
                    value = str(self.dataAcquisition())
                    data = {'id':self.sensor_id, 'data':value}
                    data = json.dumps(data)
                    #ENVOI DES DONNEES A L API                                                                  
                    url = 'http://localhost:5000/sensor_data'
                    payload = {'sender': self.sensor_id,'message':data ,'metadata': {}}
                    headers = {'Content-Type': 'application/json'}
                    requests.post(url, data=json.dumps(payload), headers=headers)                   
                    time.sleep(1)                   
                    
                except Exception as e:
                    print(e)
                self.start_timer()
        

    def start_timer(self):
        time.sleep(1/self.sensor_rate)     

    def start_threads(self):        
        self.thread_send.start()        

    def dataAcquisition(self):
        #print(self.data_type)
        if self.data_type == 'Humidity':
            data = round(uniform(80,86),2) 
        elif self.data_type == 'Heat':
            data = round(uniform(10,13),2)
        elif self.data_type == 'Air pressure':
            data = round(uniform(1015,1020),2)
        return data
