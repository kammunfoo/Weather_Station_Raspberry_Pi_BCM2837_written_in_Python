#!/usr/bin/python3
from flask import Flask, jsonify, abort, request, make_response, url_for, render_template

import time
import datetime
import LCD1602 as LCD1602
import RPi.GPIO as GPIO
import Adafruit_BME.BME280 as BME280
import sqlite3
import sys
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
#from Adafruit_GPIO.GPIO import *

# PubNub Setup
pubconf = PNConfiguration()
pubconf.subscribe_key='sub-c-53844344-2163-11e8-be22-c2fd0b475b93'
pubconf.publish_key='pub-c-3a8a789c-c79c-4b57-9eb8-c1de665ec9f6'
pubnub = PubNub(pubconf)

# assign a channel
channel = 'Weather_Station'

# callback section
def publish_callback(envelope, status):
	# Check whether request successfully completed or not
	if not status.is_error():
		# Message successfully published to specified channel.
		print("Sensor/Actuator Data Sent To PubNub")
	else:
		# Handle message publish error. Check 'category' property to find out possible issue
		# because of which request did fail.
		# Request can be resent using: [status retry];
		print("Error Sending!")

def database(sens_temp, sens_press, dt):
	db_name = "SENSORS.db"
	table_name = "SENSORS_TABLE"
	
	sensor_id = 1
	
	conn = sqlite3.connect(db_name)
	cursor = conn.cursor()
	
	sql_column_name = "CREATE TABLE IF NOT EXISTS {0} (SENSOR_ID INTEGER, TEMPERATURE REAL, PRESSURE REAL, DATETIME TEXT);".\
		  format(table_name)
	cursor.execute(sql_column_name)
	
	sql_record = "INSERT INTO {0} (SENSOR_ID, TEMPERATURE, PRESSURE, DATETIME) VALUES ({1}, {2}, {3}, '{4}');".\
		 format(table_name, sensor_id, sens_temp, sens_press, dt)
	cursor.execute(sql_record)

	fp = open('SENSORS_LOG.txt', 'a')

	#ROWID is an SQLite3 keyword
	sql_read = "SELECT ROWID, * FROM " + table_name
	cursor.execute(sql_read)

	for row in cursor:
		#print(row)
		record = "{ Unique_Sample_ID: " + str(row[0]) + ", "
		record += "SENSOR_ID: " + str(row[1]) + ", "
		record += "TEMPERATURE: " + str(format(row[2], '.2f')) + " degC, "
		record += "PRESSURE: " + str(format(row[3], '.2f')) + " mbar, "
		record += "DATETIME: " + str(row[4]) + " }"
		
	fp.write(record + "\n")
	print("\n" + record)
		
	fp.close()
	
	pubnub.publish().channel(channel).message(record).async(publish_callback)
	
	conn.commit()
	cursor.close()
	conn.close()

def setup_LCD():
	LCD1602.init(0x27, 1)	# init(slave address, background light)
	LCD1602.write(2, 0, 'Greetings!!')
	LCD1602.write(3, 1, 'from IoT :)')
	time.sleep(2)
	LCD1602.clear()

def LCD(sens_temp, sens_press):
	LCD_temp = format(sens_temp, '.2f')
	LCD_press = format(sens_press, '.2f')
	LCD1602.write(0, 1, 'Temp ' + LCD_temp + ' degC')
	LCD1602.write(0, 0, 'Pres ' + LCD_press + ' mb')

setup_LCD()

# init flask instance
app = Flask(__name__)

# error handler 400
@app.errorhandler(400)
def not_found(error):
	return make_response(jsonify( { 'error': 'Bad Request' } ), 400)

# error handler 404
@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify( { 'error': 'Not Found' } ), 404)

# GET Request Handler
@app.route('/final/api/sensors', methods = ['GET'])
def get_sensors():
	dt=datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
	sensor = BME280.BME280()
	sens_temp = sensor.read_temperature()
	#sens_hum = sensor.read_humidity()
	sens_press = sensor.read_pressure()/100
	json_data = { 'Sensor Information': 'Sensor Readings',
		'Current Date and Time':dt,     
		'Current Temperature':format(sens_temp, '.2f') + ' degC',
		'Current Pressure':format(sens_press, '.2f') + ' mbar'
		}
	LCD(sens_temp, sens_press)
	database(sens_temp, sens_press, dt)
	return jsonify( { 'Sensors': json_data } )

# POST Request Handler
@app.route('/final/api/led/<int:toggle>', methods = ['POST'])
def set_led(toggle):
	R = 11
	G = 12
	B = 13
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(R, GPIO.OUT)
	GPIO.setup(G, GPIO.OUT)
	GPIO.setup(B, GPIO.OUT)
	time.sleep(1)
	
	#switch_status = "Off"

	if not request.json or not "toggle" in request.json:
		abort(400)
		
	toggle = request.json['toggle']
	
	if (toggle == 1):
		GPIO.output(R, GPIO.LOW)
		GPIO.output(G, GPIO.LOW)
		GPIO.output(B, GPIO.LOW)
		switch_status = "On"

		#pubnub.publish().channel(channel).message(record).async(publish_callback)
	else:
		GPIO.output(R, GPIO.HIGH)
		GPIO.output(G, GPIO.HIGH)
		GPIO.output(B, GPIO.HIGH)
		GPIO.cleanup()
		switch_status = "Off"

	dt=datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
	fp = open('SENSORS_LOG.txt', 'a')
	fp.write("LED: " + switch_status + ", " + "Datetime: " + dt + "\n")
	fp.close()
	print("\nLED: " + switch_status + ", " + "Datetime: " + dt)
	pubnub.publish().channel(channel).message("LED: " + switch_status + ", Datetime: " + dt).async(publish_callback)
	return jsonify( { 'Toggle': switch_status,
						  'Datetime': dt} )
# HTML Dashboard
@app.route('/final/api/dashboard')
def dashboard4():
	dt=datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
	
	db_name = "SENSORS.db"
	table_name = "SENSORS_TABLE"
	
	conn = sqlite3.connect(db_name)
	cursor = conn.cursor()
	
	#ROWID is an SQLite3 keyword
	sql_sample_count = "SELECT COUNT(ROWID), DATETIME FROM " + table_name
	cursor.execute(sql_sample_count)
	for row in cursor:
		count = row[0]

	print(count)

	sql_min_temp = "SELECT MIN(TEMPERATURE), DATETIME FROM " + table_name
	sql_avg_temp = "SELECT AVG(TEMPERATURE) FROM " + table_name
	sql_max_temp = "SELECT MAX(TEMPERATURE), DATETIME FROM " + table_name

	sql_min_press = "SELECT MIN(PRESSURE), DATETIME FROM " + table_name
	sql_avg_press = "SELECT AVG(PRESSURE) FROM " + table_name
	sql_max_press = "SELECT MAX(PRESSURE), DATETIME FROM " + table_name

	cursor.execute(sql_min_temp)
	for row in cursor:
		min_temp = format(row[0], '.2f')
		min_temp_dt = row[1]

	cursor.execute(sql_avg_temp)
	for row in cursor:
		avg_temp = format(row[0], '.2f')

	cursor.execute(sql_max_temp)
	for row in cursor:
		max_temp = format(row[0], '.2f')
		max_temp_dt = row[1]
	
	cursor.execute(sql_min_press)
	for row in cursor:
		min_press = format(row[0], '.2f')
		min_press_dt = row[1]
				
	cursor.execute(sql_avg_press)
	for row in cursor:
		avg_press = format(row[0], '.2f')
			
	cursor.execute(sql_max_press)
	for row in cursor:
		max_press = format(row[0], '.2f')
		max_press_dt = row[1]
	
	dashboard_data = {
		'title' : 'Weather Station Dashboard',
		'time' : dt,
		'count' : count,
		'min_temp' : min_temp,
		'min_temp_dt' : min_temp_dt,
                'avg_temp' : avg_temp,
                'max_temp' : max_temp,
                'max_temp_dt' : max_temp_dt,
                'min_press' : min_press,
                'min_press_dt' : min_press_dt,
                'avg_press' : avg_press,
                'max_press' : max_press,
                'max_press_dt' : max_press_dt
		}

	return render_template('final-kf.html', **dashboard_data)

if __name__ =='__main__':
	app.run(debug=True, host='192.168.1.200', port=8080)

