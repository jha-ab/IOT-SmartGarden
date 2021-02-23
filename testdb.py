# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 14:24:20 2020

@author: jean louis
"""
import pyrebase
import config
from time import sleep 

config = config.db_config


def configure_db():
    '''return db ref'''
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    return db

def get_thresh(db):
    return db.child("test-DHT").child('thresh').get().val()
def get_sensors(db):
    return db.child("test-DHT").child('sensors').get().val()
def get_status(db):
    return db.child("test-DHT").child('status').get().val()

def set_status(db,val):
    val = str(val)
    db.child("test-DHT").update({"status":val})

def write_LED(val):
    db.child("test-DHT").update({"led":val})
    
def write_sensor_db(db, json):
    db.child("test-DHT").child("sensors")
	
def write_actu():
    pass

def set_listener():
	status_stream = db.child("test-DHT").child('status').stream(stream_handler)
	sleep(1)
	return status_stream


def stream_handler(message):
	sleep(1)
	print("The status of this plant is now: ")
	#print(message["event"]) # put
	print(message["data"]) # {'title': 'Pyrebase', "body": "etc..."}






if __name__ == '__main__':
	db = configure_db()
	thresh = get_thresh(db)
	print(thresh)
	status_listener = set_listener()
	status = get_status(db)
	print('db status says: ',status)
	set_status(db, "danger")
	status = get_status(db)
	print(status)
	sleep(4)
	set_status(db, "good")
	print(get_sensors(db))
	write_LED('on')
	sleep(4)
	write_LED('off')
	status_listener.close()
	
#https://github.com/thisbejim/Pyrebase

    