# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 01:41:51 2020

@author: Jean Louis
"""
from dotmap import DotMap
import RPi.GPIO as GPIO
#import the RPi.GPIO module to allow us use the board GPIO pins.
import pyrebase        
#import the pyrebase module which allows us to communicate with the firebase servers.
from time import sleep
import Adafruit_DHT

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

dhtpin = 4
ledPin = 18
BtnPin = 12


sleepTime = 5
Led_status= 1
dht = Adafruit_DHT.DHT11

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


def configure_pi():
    '''set up GPIO pins and in/out values'''
    pass

def connect_db():
    '''connect to firebase'''
    pass

#print(plant.sensors)
def read_sensors_data():
    '''loops through the sensor gpio pins and sets the sensors values'''
    pass
def get_sensor_threshholds():
    '''pulls the current sensor threshhold value for the given plant'''
    pass
def check_thresholds():
    '''compare the datbase thresholds to the current sensor reading'''
    pass
def update_plant_status():
    '''update the plant status'''
    pass
def compare_reading():
    '''determin if a significante change in sensor readings have occured'''
    pass
def post_sensor_data():
    '''post sensor data to firebase'''
    pass
def write_actuators_data():
    pass



#initail testing of Pi 
def handel_btn():
    print("button pushed")
    global Led_status
    Led_status = not Led_status
    GPIO.output(ledPin, Led_status)
    
def test_led():
    print("testing LED")
    GPIO.setup(ledPin,GPIO.OUT)
    GPIO.output(ledPin,GPIO.HIGH)
    sleep(1)
    GPIO.output(ledPin,GPIO.LOW)
def test_dht():
    humidity, temperature = Adafruit_DHT.read_retry(dht, dhtpin)
    print('temp',temperature)
    print('humidity',humidity)
    

def run():
    read_sensors_data()
    get_sensor_threshholds()
    check_thresholds()
    update_plant_status()
    compare_reading()
    post_sensor_data()
    write_actuators_data()
    


def loop():
    GPIO.add_event_detect(BtnPin, GPIO.FALLING, callback=handel_btn, bouncetime=200)
    while True:
        run()
        sleep(1)   # Don't do anything


if __name__ == '__main__':
    configure_pi()
    test_led()
    test_dht()
    try:
        loop()
    except KeyboardInterrupt:  # 'Ctrl+C' is pressed
        print('exiting')

'''
step 1: get pi working with test led and test dht function
step 2: complete run sub function with dht sensor localy
step 3: connect dht version to firebase
step 4: re write sub functions for all the sensors
step 5: test reading and writing all sensor data to firebase 
step 6: update function to work with full firebase json and optimize

'''



#test
'''
plant =DotMap(plant)

print(plant.name)
print(plant.sensors)
print(plant.sensor.temp)
print(plant.sensors.led.type)
print(plant)

for s in plant.sensors:
    print(plant.sensors.s.type)
'''    