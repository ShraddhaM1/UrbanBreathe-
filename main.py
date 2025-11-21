# import the necessary packages
from flask import Flask, render_template, redirect, url_for, request,session,Response
from werkzeug import secure_filename
import os
import cv2
import pandas as pd
import sqlite3
from datetime import datetime
import json
from firebaseTest import *
from PollutionStatus import *
from threading import Thread
# import playsound
from notification import *

prevStatus = ''

# def sound_alarm(path):
# 	# play an alarm sound
# 	playsound.playsound(path)

name = ''


app = Flask(__name__)

app.secret_key = '1234'
app.config["CACHE_TYPE"] = "null"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/', methods=['GET', 'POST'])
def landing():
	return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	global name
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		con = sqlite3.connect('mydatabase.db')
		cursorObj = con.cursor()
		cursorObj.execute(f"SELECT Name from Users WHERE Email='{email}' AND password = '{password}';")
		try:
			name = cursorObj.fetchone()[0]
			return redirect(url_for('dashboard'))
		except:
			error = "Invalid Credentials Please try again..!!!"
			return render_template('login.html',error=error)
	return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
	error = None
	if request.method == 'POST':
		if request.form['sub']=='Submit':
			name = request.form['name']
			email = request.form['email']
			password = request.form['password']
			rpassword = request.form['rpassword']
			pet = request.form['pet']
			if(password != rpassword):
				error='Password dose not match..!!!'
				return render_template('register.html',error=error)
			try:
				con = sqlite3.connect('mydatabase.db')
				cursorObj = con.cursor()
				cursorObj.execute(f"SELECT Name from Users WHERE Email='{email}' AND password = '{password}';")
			
				if(cursorObj.fetchone()):
					error = "User already Registered...!!!"
					return render_template('register.html',error=error)
			except:
				pass
			now = datetime.now()
			dt_string = now.strftime("%d/%m/%Y %H:%M:%S")			
			con = sqlite3.connect('mydatabase.db')
			cursorObj = con.cursor()
			cursorObj.execute("CREATE TABLE IF NOT EXISTS Users (Date text,Name text,Email text,password text,pet text)")
			cursorObj.execute("INSERT INTO Users VALUES(?,?,?,?,?)",(dt_string,name,email,password,pet))
			con.commit()

			return redirect(url_for('login'))

	return render_template('register.html')

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
	error = None
	global name
	if request.method == 'POST':
		email = request.form['email']
		pet = request.form['pet']
		con = sqlite3.connect('mydatabase.db')
		cursorObj = con.cursor()
		cursorObj.execute(f"SELECT password from Users WHERE Email='{email}' AND pet = '{pet}';")
		
		try:
			password = cursorObj.fetchone()
			#print(password)
			error = "Your password : "+password[0]
		except:
			error = "Invalid information Please try again..!!!"
		return render_template('forgot-password.html',error=error)
	return render_template('forgot-password.html')

from flask import render_template, jsonify
from threading import Thread

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
	global name
	temp, humidity, mq2, mq3, mq7,pollution_status = readFirebase()

	# Get pollution status from AI model (you can define this function)
	#pollution_status = predict_pollution_level(temp, humidity, mq2, mq3, mq7)

	return render_template('dashboard.html',
						   name=name,
						   temp=temp,
						   humidity=humidity,
						   mq2=mq2,
						   mq3=mq3,
						   mq7=mq7,
						   pollution_status=pollution_status)


@app.route('/get_realtime_data')
def get_realtime_data():
	temp, humidity, mq2, mq3, mq7,pollution_status = readFirebase()
	return jsonify({
		'temp': temp,
		'humidity': humidity,
		'mq2': mq2,
		'mq3': mq3,
		'mq7': mq7
	})

@app.route('/get_pollution_status')
def get_pollution_status():
	global prevStatus
	print(prevStatus)
	_, _, mq2, mq3, mq7, pollution_status = readFirebase()
	if(prevStatus != pollution_status):
		prevStatus = pollution_status
		pushbullet_noti('Pollution Update','Pollution Level:'+pollution_status)

	return jsonify({'pollution_status': pollution_status})

# No caching at all for API endpoints.
@app.after_request
def add_header(response):
	# response.cache_control.no_store = True
	response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
	response.headers['Pragma'] = 'no-cache'
	response.headers['Expires'] = '-1'
	return response


if __name__ == '__main__' and run:
	app.run(host='0.0.0.0', threaded=True, debug=False)
