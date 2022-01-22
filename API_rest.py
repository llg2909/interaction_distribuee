from flask import Flask, request, jsonify
from stableMemory import loadJsonFile,saveData
import json

app = Flask(__name__)


### API REST COMMUNIQUANT POUR LES AGREGATS
@app.route("/sensor_configagg1", methods=["GET"])
def get_configagg1():
    sensors_id = ["Hygrometer","Thermometer"]   
    config1 = loadJsonFile('./config_sensor'+str(sensors_id[0])+'.json')
    config2 = loadJsonFile('./config_sensor'+str(sensors_id[1])+'.json')
    config1 = config1["message"]
    config2 = config2["message"]    
    return jsonify("["+config1+","+config2+"]"), 201

@app.route("/sensor_configagg2", methods=["GET"])
def get_configagg2():   
    sensors_id = ["Thermometer2","Barometer"]   
    config1 = loadJsonFile('./config_sensor'+str(sensors_id[0])+'.json')
    config2 = loadJsonFile('./config_sensor'+str(sensors_id[1])+'.json')
    config1 = config1["message"]
    config2 = config2["message"]    
    return jsonify("["+config1+","+config2+"]"), 201


@app.route("/sensor_dataagg1", methods=["GET"])
def get_dataagg1():   
    sensors_id = ["Hygrometer","Thermometer"]   
    config1 = loadJsonFile('./data_sensor'+str(sensors_id[0])+'.json')
    config2 = loadJsonFile('./data_sensor'+str(sensors_id[1])+'.json') 
    config1 = json.dumps(config1) 
    config2 = json.dumps(config2)         
    return jsonify("["+config1+","+config2+"]"), 201

@app.route("/sensor_dataagg2", methods=["GET"])
def get_dataagg2():   
    sensors_id = ["Thermometer2","Barometer"]   
    config1 = loadJsonFile('./data_sensor'+str(sensors_id[0])+'.json')
    config2 = loadJsonFile('./data_sensor'+str(sensors_id[1])+'.json') 
    config1 = json.dumps(config1) 
    config2 = json.dumps(config2)     
    return jsonify("["+config1+","+config2+"]"), 201
       


### API STOCKAGE config ENVOYER PAR LES SENSORS
@app.route("/sensor_config", methods=["POST"])
def receive_config(): 
    data = request.get_json()    
    message = data['message']
    message = json.loads(message)
    sensor_id = message["id"]
    file_config = loadJsonFile('./config_sensor'+str(sensor_id)+'.json')
    saveData('./config_sensor'+str(sensor_id)+'.json',data) 
    return "ok", 201

### API STOCKAGE data 
@app.route("/sensor_data", methods=["POST"])
def receive_data(): 
    data = request.get_json()    
    message = data['message']
    message = json.loads(message)   
    sensor_id = message["id"]
    #file_config = loadJsonFile('./data_sensor'+str(sensor_id)+'.json')
    saveData('./data_sensor'+str(sensor_id)+'.json',message) 
    return "ok", 201

### API STOCKAGE slot client
@app.route("/slot_client", methods=["POST"])
def receive_data_client(): 
    data = request.get_json()    
    message = data['message']
    print(message)
    message = json.loads(message)   
    agg_id = data['sender']
    #file_config = loadJsonFile('./slot_client'+str(agg_id)+'.json')
    saveData('./slot_client'+str(agg_id)+'.json',message) 
    return "ok", 201

@app.route("/slot_clientagg1", methods=["GET"])
def get_data_client1():
    config1 = loadJsonFile('./slot_clientagg1.json')   
    config1 = json.dumps(config1)       
    return jsonify(config1), 201

@app.route("/slot_clientagg2", methods=["GET"])
def get_data_client2():
    config1 = loadJsonFile('./slot_clientagg2.json')   
    config1 = json.dumps(config1)       
    return jsonify(config1), 201

