import os
import serial
import time
from firebase import firebase

arduino = serial.Serial('/dev/ttyACM0', 9600)
firebase = firebase.FirebaseApplication('https://raspi-ph.firebaseio.com/', None)

def update_firebase():
    try:
        phair = arduino.readline().decode().strip()
        if phair:
            pieces = phair.split("sensor = ")
            if len(pieces) > 1:
                ph = pieces[1]
                print("pH:", ph)
                data = {"Sensor pH": ph}
                firebase.post('/sensor/ph', data)
            else:
                print("Data format error")
        else:
            print('Failed to get data. Trying again...')
            time.sleep(10)
    except Exception as e:
        print("Error:", e)
        time.sleep(10)

while True:
    update_firebase()
    time.sleep(5)
