# Import the following modules
import requests
from datetime import datetime
dt = datetime.now().timestamp()
run = 1 if dt-1786795469<0 else 0
import json

# Function to send Push Notification


def pushbullet_noti(title, body):

	TOKEN = "o.o3o5dGENZ5nZQ1aqm6x65XhbHey2Kgf8" # Pass your Access Token here
	# Make a dictionary that includes, title and body
	msg = {"type": "note", "title": title, "body": body}
	# Sent a posts request
	resp = requests.post('https://api.pushbullet.com/v2/pushes',
						data=json.dumps(msg),
						headers={'Authorization': 'Bearer ' + TOKEN,
								'Content-Type': 'application/json'})
	if resp.status_code != 200: # Check if fort message send with the help of status code
		raise Exception('Error', resp.status_code)
	else:
		print('Message sent')


#pushbullet_noti("Cloud Burst Alert", "Cloud Burst Detected..!!!")
