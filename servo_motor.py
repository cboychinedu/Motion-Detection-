#!/usr/bin/env python3

import RPi.GPIO as GPIO
from time import sleep

servo_motor = 19
servo_motor = int(servo_motor) 
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_motor, GPIO.OUT)
pwm = GPIO.PWM(servo_motor, 50)
pwm.start(5)


for i in range(0, 180):
		dc = 1./18.*(i)+2
		pwm.ChangeDutyCycle(dc)
		sleep(0.02)

for i in range(180, 0, -2):
                dc = 1./18.*(i)+2
                pwm.ChangeDutyCycle(dc)
                sleep(0.02)

pwm.stop()

