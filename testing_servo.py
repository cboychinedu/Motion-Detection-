#!/usr/bin/env python3

# Importing the necessary Packages.
import RPi.GPIO as GPIO
from time import sleep

servo_motor = 19
servo_motor = int(servo_motor)
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_motor, GPIO.OUT)
pwm = GPIO.PWM(servo_motor, 50)
pwm.start(8.5)

running = True


while running:

##    for i in range(0, 180):
##        dc = 1/18.0*(i)+2
##        pwm.ChangeDutyCycle(dc)
##        sleep(0.02)

    for i in range(180, 0, -3):
        dc = 1/18.0*(i)+2
        pwm.ChangeDutyCycle(dc)
        sleep(0.1)


pwm.stop()
GPIO.cleanup() 
