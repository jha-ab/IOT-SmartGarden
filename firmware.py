# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 01:41:51 2020

@author: Abhishek Jha
"""
from dotmap import DotMap
from sense_hat import SenseHat
import RPi.GPIO as GPIO
import pyrebase  
import serial, string, time      
#import the pyrebase module which allows us to communicate with the firebase servers.
from time import sleep
import config

ser = serial.Serial('/dev/ttyACM0', 9600, 8, 'N', 1, timeout=None)
config = config.db_config
ser.flush()


user ="user1"
plant ='p1'
status = 0;
plant={'name':plant,
       'owner':user,
       'status':'good',
       'sensors':{
           'humidity':{'name':'humidity','pin':1,'value':0,'type':'s'},
            'temp':{'name':'temp','pin':2,'value':0,'type':'s'},
            'led':{'name':'led','pin':3,'value':0,'type':'a'}           
           }       
       }

threshholds ={'plant':'p1',
            'sensors':{
               'humidity':{'min':1,'max':2},
               'temp':{'min':3,'max':5},
               'led':{'min':0,'max':0}          
           }    
    }

lastSensorvals={}


def connect_db():
    '''connect to firebase'''
    
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    return db


def read_sensors_data():
    '''loops through the sensor gpio pins and sets the sensors values'''
    sense=SenseHat()
    #sense.clear()   
    pressure = sense.get_pressure()
    temp=sense.get_temperature()
    humidity = sense.get_humidity()
    #return round(pressure,3), round(temp,3), round(humidity,3)
    return int(pressure), int(temp), int(humidity)


def senseSoilMoisture():
    '''get soil moisture values from ADC converter'''
    ser.flush()
    soil_moisture = ser.readline()
    while(soil_moisture == ""):
        soil_moisture = ser.readline()
    if soil_moisture < 0:
        soil_moisture = 0
    return int(soil_moisture)


def get_sensor_threshholds(db):
    '''pulls the current sensor threshhold value for the given plant'''
    humid_min = db.child('users').child(user).child('plants').child('p1').child('thresh').child('humidity').child('min').get().val()
    humid_max = db.child('users').child(user).child('plants').child('p1').child('thresh').child('humidity').child('max').get().val()  

    soil_min = db.child('users').child(user).child('plants').child('p1').child('thresh').child('soilmoisture').child('min').get().val()
    soil_max = db.child('users').child(user).child('plants').child('p1').child('thresh').child('soilmoisture').child('max').get().val()

    temp_min = db.child('users').child(user).child('plants').child('p1').child('thresh').child('temp').child('min').get().val()
    temp_max = db.child('users').child(user).child('plants').child('p1').child('thresh').child('temp').child('max').get().val()

    return  humid_min, humid_max, temp_min, temp_max, soil_min, soil_max


def check_thresholds(temp, humidity, soil_moisture, humid_min, humid_max, temp_min, temp_max, soil_min, soil_max):
    '''compare the datbase thresholds to the current sensor reading'''
    status_t, status_h, status_s = 0,0,0

    if temp > temp_min and temp < temp_max:
        status_t = 1
    
    if humidity > humid_min and humidity < humid_max:
        status_h = 1

    if soil_moisture > soil_min and soil_moisture < soil_max:
        status_s = 1

    if status_t and status_h and status_s:
        return "good"
    else:
        return "bad"


def update_plant_status(status):
    '''update the plant status'''
    db.child('users').child(user).child('plants').child('p1').update({"status": status})
    


def post_sensor_data(db, temp, humidity, soil_moisture):
    '''post sensor data to firebase'''

    db.child('users').child(user).child('plants').child('p1').child('sensors').update({"humidity": humidity})
    db.child('users').child(user).child('plants').child('p1').child('sensors').update({"temp": temp})
    db.child('users').child(user).child('plants').child('p1').child('sensors').update({"soilmoisture": soil_moisture})

    if soil_moisture>=-100 and soil_moisture<22:
        soil_condition = "arid"
    elif soil_moisture>=22 and soil_moisture<40:
        soil_condition = "dry"
    elif soil_moisture>=40 and soil_moisture<58:
        soil_condition = "moderate"
    elif soil_moisture>=58 and soil_moisture<76:
        soil_condition = "damp"
    else:
        soil_condition = "wet"

    db.child('users').child(user).child('plants').child('p1').child('sensors').update({"soilcondition": soil_condition})
    

def write_actuators_data(db, soil_moisture, soil_min):
    '''activate motor after condition check'''
    
    #check from db for motor activation----stream_listner to get manual watering option

    if(soil_moisture<soil_min):

        db.child('users').child(user).child('plants').child('p1').child('sensors').update({"motor": "on"})
        print("write motor")
        
    else:
        db.child('users').child(user).child('plants').child('p1').child('sensors').update({"motor": "off"})

    #status_listener = set_listener()


def set_listener():

    status_stream = db.child('users').child(user).child('plants').child('p1').child('sensors').child('motor').stream(stream_handler)

    return status_stream


def stream_handler(message):
    # sleep(1)
    #print("The status of this plant is now: ")
    #print(message["event"]) # put
    #print(message["data"])
    sense=SenseHat()
    if message["data"] == "on":
        #sense=SenseHat()
        r = 0
        g = 0
        b = 200
        sense.clear((r, g, b))
        print("now here")
    elif message["data"] == "off":
        sense.clear()
    else:
        print(message["data"])
        

def run(db, pressure_old, temp_old, humidity_old, soil_moisture_old):

    pressure, temp, humidity = read_sensors_data()
    soil_moisture = senseSoilMoisture()
    soil_moisture = float(soil_moisture)
    print("pressure = {}, temp = {}, humidity = {}, soil_moisture = {}\n".format(pressure, temp, humidity, soil_moisture))

    humid_min, humid_max, temp_min, temp_max, soil_min, soil_max = get_sensor_threshholds(db)
    print("Thresholds: \n temp = {}, {},\n humidity = {}, {},\n soil_moisture = {},{},\n\n".format(
        temp_min, temp_max, humid_min, humid_max, soil_min, soil_max))

    status = check_thresholds(temp, humidity, soil_moisture, humid_min, humid_max, temp_min, temp_max, soil_min, soil_max)
    print("status = {}".format(status))

    update_plant_status(status)

    # compare_reading()
    if temp != temp_old or humidity != humidity_old or soil_moisture != soil_moisture_old:
       post_sensor_data(db, temp, humidity, soil_moisture)
    
    write_actuators_data(db, soil_moisture, soil_min)

    return pressure, temp, humidity, soil_moisture    


def loop(db):
    """ loop until interrupted """
    pressure_old, temp_old, humidity_old, soil_moisture_old = 0.0, 0.0, 0.0, 0.0
    while True:
        pressure_old, temp_old, humidity_old, soil_moisture_old = run(db, pressure_old, temp_old, humidity_old, soil_moisture_old)
        sleep(1)   # Don't do anything


if __name__ == '__main__':
    db = connect_db()
    try:
        status_listener = set_listener()
        loop(db)
    except KeyboardInterrupt:  # 'Ctrl+C' is pressed
        print('exiting')
        GPIO.cleanup()
        ser.close()



