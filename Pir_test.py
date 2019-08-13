#!/usr/bin/env python3

import RPi.GPIO as GPIO
from time import sleep 

pir_sensor = 16



pir_sensor = int(pir_sensor)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pir_sensor, GPIO.IN)


run = True
sleep(5)
while run:
    if GPIO.input(pir_sensor):
        print('Motion Detected')
    else:
        print('Scanning for motion')




GPIO.cleanup()
