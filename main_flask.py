#!/usr/bin/env python3
# Author: Mbonu Chinedum Endurance
# University: Nnamdi Azikiwe University
# Date Created: 24/6/2019 "Buhari Tenor"

"""
DESCRIPTION:
    This script would capture live frames form a specified webcam and stream it live
    on a webserver that has a static ip-address.
    Thus making the user to access the live video feed from a web browser.

"""

# Importing the necessary Packages.
import cv2
from flask import Flask, render_template, Response
from video.camera import VideoCamera
from flask import url_for
from flask_basicauth import BasicAuth
from time import sleep
import RPi.GPIO as GPIO
import threading

# Assigning the video camera class to a variable called video_camera and,
# And Loading in the  Haar Cascade classifier for fullbody recognition into,
# an Opencv classifier.
video_camera = VideoCamera()
object_classifier = cv2.CascadeClassifier('video/models/fullbody_recognition_model.xml')
servo_motor = 19
servo_motor = int(servo_motor)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) 
GPIO.setup(servo_motor, GPIO.OUT)
pwm = GPIO.PWM(servo_motor, 50)
pwm.start(5)

# Creating a Dictionary for storing the web application Authentication Details.
app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'admin'
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)
last_epoch = 0


# Defining a function for collection of frames from the webcam,
# And pass the frames into the opencv Haar Classifier in a loop.
# And make the servo motor to rotate clockwise and anticlockwise.
def check_for_objects():
    global last_epoch
    run = True
    while run:
        for i in range(0, 180):
            dc = 1.0/18.0*(i)+2
            pwm.ChangeDutyCycle(dc)
            sleep(0.05)
        for i in range(180, 0, -1):
            dc = 1.0/18.0*(i)+2
            pwm.ChangeDutyCycle(dc)
            sleep(0.05)
        try:
            frame, found_obj = video_camera.get_object()
            continue
        except:
            pass

# Passing the Gotten frames into a website called,
# 'index.html'
@app.route('/')
@basic_auth.required
def index():
    return render_template('index.html')


# Creating a box on the webpage for the frames of the camera, 
# to be visible.
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# sending the frames and the page to a server to make it 
# Available online.
@app.route('/video_feed')
def video_feed():
    return Response(gen(video_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# Creating a Function that would start the whole Process,
# And run the webserver on a specific ip-address.
def main():
    if __name__ == '__main__':
        t = threading.Thread(target=check_for_objects, args=())
        t.daemon = True
        t.start()
        app.run(host='192.168.43.238', debug=False)


pwm.stop()
GPIO.cleanup()
