import os
import serial
import time
from firebase import firebase

arduino = serial.Serial('/dev/ttyACM0',9600)

firebase = firebase.FirebaseApplication('https://raspi-ph.firebaseio.com/', None)


def update_firebase():
    phair = arduino.readline()
    if data is not None:
        time.sleep(1)
        pieces = data.split("sensor= ")
        ph = pieces
        print ph
    else:
        print('Failed to get data. Try Again!')
        time.sleep(10)

    data = {"Sensor pH": phair}
    firebase.post('/sensor/ph', data)


while True:
    update_firebase()

    time.sleep(5)
