import requests
import json
import time
import threading
class Client() : 
    def __init__(self,client_id):       
        self.sensor_id = client_id
        self.thread_get = threading.Thread(target=self.get_slot)
    def get_slot(self):        
        while True:
                time.sleep(60)                
                try:
                    url = 'http://localhost:5000/slot_clientagg1'        
                    reponse = requests.get(url) 
                    data = reponse.text                   
                    data_agg1 = json.dumps(data)

                    url = 'http://localhost:5000/slot_clientagg2'        
                    reponse = requests.get(url) 
                    data = reponse.text                   
                    data_agg2 = json.dumps(data)                                  
                    
                    print("Data de l'agg1 : ",str(data_agg1))
                    print("\nData de l'agg2 : ",str(data_agg2))
                except Exception as e:
                    print(e)
                
    def start_thread(self):        
        self.thread_get.start()    