from firebase import firebase
def readFirebase():
    firebase1 = firebase.FirebaseApplication('https://augmentedreality-af310-default-rtdb.firebaseio.com/', None)
    temp = firebase1.get('/AE383/temp', None)
    humidity = firebase1.get('/AE383/humidity', None)
    mq2 = firebase1.get('/AE383/mq2_ppm', None)
    mq3 = firebase1.get('/AE383/mq3_ppm', None)
    mq7 = firebase1.get('/AE383/mq7_ppm', None)
    pollution_status = firebase1.get('/AE383/pollution_status', None)
    return(temp,humidity,mq2,mq3,mq7,pollution_status)

#print(readFirebase())
       