#!/usr/bin/env python3
# Author: Mbonu Chinedum Endurance
# University : Nnamdi Azikiwe University
# Date Created: 27/01/2019 "Buhari tenor"


"""

DESCRIPTION:

This Program was written to Detects Objects, Animals and Human Beings by the use of a PIR sensor which detects motion and tells the camera to take a picture
of the object or body that caused the motion.
A Machine learning model that was trained on the Pascal Voc Object Detection Dataset "YOLOv3" would then run a machine learning algorithm on the image captured
to actually tell us the object or body that is present in the image and then send us an email indicating what it is with it percentage accuracy.

A video Detection also starts if the object detected was a human being, thus making us to see a live streaming footage of the person in that location.

"""

# Importing the necessary packages
from time import sleep
from flask import Flask, render_template, Response
from video.camera import VideoCamera
from flask_basicauth import BasicAuth
from flask import url_for 
from subprocess import call
import urllib.request as url
import os
import cv2 
import sys
import smtplib
import threading
import re
import datetime
import RPi.GPIO as GPIO
import picamera

#call('mpg321 Startup.mp3 2>/dev/null ', shell=True)
sleep(2)

# Performing a Little Cleanup to clean unnecessary files.
if os.path.exists('detection/*.txt'):
    os.remove('detection/*.txt')
else:
    pass 


# Assigning the variable camera to the libary picamera and initialize it.
video_camera = VideoCamera()
object_classifier = cv2.CascadeClassifier('video/models/fullbody_recognition_model.xml')
camera = picamera.PiCamera()

# Setting the General Purpose Input And Output Pins,
# Number for the Servo-motor.
servo_motor = 19 

# Changing the pin values into an interger value for the servo motor.
# And setting the Board Mode to be 'BCM' mode. 
servo_motor = int(servo_motor)
GPIO.setmode(GPIO.BCM)


# While the servo_moto Receives pulse width  modulation
# signals from the GPIO pins.
GPIO.setwarnings(False)
GPIO.setup(servo_motor, GPIO.OUT)


# Setting Pulse width Modulation for the Servo_motor,
# And Setting the Frequency to be 50Hz.
pwm = GPIO.PWM(servo_motor, 50)
pwm.start(8.30)


# Creating a for loop that would make the servo motor,
# to rotate from angle 0 tp 180 degrees front and back. 
for i in range(0, 180):
    dc = 1/18.0*(i)+2
    pwm.ChangeDutyCycle(dc)
    sleep(0.02)

for i in range(180, 0, -1):
    dc = 1/18.0*(i)+2
    pwm.ChangeDutyCycle(dc)
    sleep(0.02)

# Sleeping for 2 seconds, then creating a for loop that Changes,
# The Pulse width modulation of the servo motor from
# 3miliseconds to 12miliseconds, Then cleanup afer the Process is done. 
sleep(2)
for items in range(4, 11):
    i = items
    pwm.ChangeDutyCycle(i)
    sleep(1.5)

pwm.ChangeDutyCycle(8.3)
sleep(2)

#pwm.stop()
GPIO.cleanup() 


'''
# Creating a Function to test for internet connection,
# And Assigning a Boolean value to its Status.
site = 'http://216.58.223.196'
try:
    url.urlopen(site)
    msg = True

except:
    msg = False
'''
# Creating a Dictionary for storing the web application Authentication Details.
app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'admin'
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)
last_epoch = 0


# Defining a camera function that snaps the object the moment there is motion.
# Initializing the camera and snap the object, wait for 2seconds and snap the image again.
# Stop the camera preview and break out of the loop.
def camera_snap():
    while True:
            camera.start_preview()
            camera.capture('image.jpg')
            sleep(2)
            camera.capture('image1.jpg')
            camera.stop_preview()
            break


# Defining an image Detection function That runs the YOLOv3 model
# On the captured image from the camera.
# we then run a bash script that runs the Machine learning Model on the image to give us,
# The accurate Predictions of the objects present in the image.
def image_detection():
    while True:
        call("bash image_detection.sh", shell=True)
        break


# Defining a Video detection function that run a machine learning model on live frames captured,
# From the Usb webcam.
# Setting the PWM signals of the GPIO output pin as 19 and sending a signal of 50hertz.
# Creating a for loop that changes the PWM signals after every 0.01seconds. 
def check_for_objects():
    global last_epoch
    run = True
    while run:
        for i in range(0, 180):
            dc = 1/18.*(i)+2
            pwm.ChangeDutyCycle(dc)
            sleep(0.2)

        for i in range(180, 0, -1):
            dc = 1/18.*(i)+2
            pwm.ChangeDutyCycle(dc)
            sleep(0.2)
        try:
            frame, found_obj = video_camera.get_object()
            continue

        except:
            pass

# Passing the Gotten Frames into a website called,
# index.html.
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

# Sending the frames and the page to a server to make it
# Avialable online.
@app.route('/video_feed')
def video_feed():
    return Response(gen(video_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Creating a Function that would start the whole Process,
# And Rub the webserver on a specific ip-address.
def main():
    servo_motor = 19
    servo_motor = int(servo_motor)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servo_motor, GPIO.OUT)
    if __name__ == '__main__':
        t = threading.Thread(target=check_for_objects, args=())
        t.daemon = True
        t.start()
        pwm.start(5)
        app.run(host='192.168.43.238', debug=False)



# Defining a function for sending of emails and importing the necessary modules for it.
# Importing the necessary Packages for sending of the emails.
def send_mail():
    from email import encoders
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText


    # Creating a comma seperated value and assigning it a variable called "COMMASPACE"
    COMMASPACE = ', '


    # Reading the predicted value into memory and assing it to a variable called fname.
    # Opening the variable fname as f and saving it into a new variable called content.
    fname = "detection/detections.txt"
    with open(fname, 'r') as f:
        content = f.read()
    
    ip_address = '192.168.43.238:5000'
    

    # Creating a varibale to save the sender email and the password.
    # And the recipients email Address.
    # Also Assign a new variable called 'body' to contain the body of the email we want to send.
    sender = 'noreplayalansmith@gmail.com'
    gmail_password = 'ilovepam!100%'
    recipients = ['cboy.chinedu@gmail.com','noreplayalansmith@gmail.com']
    body = (content + '\n Click on this link to Access the video Footage \nOnly if A Human Was Present: {}'.format(ip_address))
    


    # Create the enclosing (outer) message that saves all the variables into
    # An Array.
    # Assigning the MIMEMultipart() module to a variable called "outer"
    # Assinging the value "Object detected" to an array called "Subject"
    # Assigning the value of the recipients to an array called "To"
    # Assigning the value of the sender to an array called "From"
    outer = MIMEMultipart()
    outer['Subject'] = 'Object Detected From RPI-43A1'
    outer['To'] = COMMASPACE.join(recipients)
    outer['From'] = sender
    outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'


    # List of attachments
    # Creating an Array called attachemnt for storing the predicted image called "predictions.jpg"
    attachments = ['predictions.jpg', 'image1.jpg']



    # Add the attachments to the message, and creat a loope for the files and content in the variables called "attachments",
    # Perform the Actions below if the conditions above are met.
    # Open the file attachment as 'fp', and read the content of fp and attach it a value called 'msg.set_payload'
    # Encode the message using base64 encoding
    # Attaching the content of the msg to the array called outer.
    outer.attach(MIMEText(body, "plain"))
    for file in attachments:
        try:
            with open(file, 'rb') as fp:
                msg = MIMEBase('application', "octet-stream")
                msg.set_payload(fp.read())
            encoders.encode_base64(msg)
            msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
            outer.attach(msg)
        except:
            print("Unable to open one of the attachments. Error: ", sys.exc_info()[0])
            pass

    composed = outer.as_string()


    # Sending the email using Google smtp server by,
    # logging into the server with the required username and password,
    # And send the mail to the recipients.
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(sender, gmail_password)
            s.sendmail(sender, recipients, composed)
            s.close()
    except:
        pass


        
# Creating a Function that sends a motion Detection mail after
# motion has been detected by the PIR sensor.
def pir_mail():
    import smtplib

    li = ["cboy.chinedu@gmail.com"]
    for i in range(len(li)):
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login("noreplayalansmith@gmail.com", "ilovepam!100%")
            message = "Motion Detected From RPI-43A1, \nThe Image Analysis is in Progress.."
            s.sendmail("sender_email_id", li[i], message)
            s.quit()

# Defining a Function that Backups the image into a folder for further Purposes.
# Removing the first captured image "image.jpg" and "detect.mp3"
# Copying the predicted image.jpg into a backup folder called pic
# Assigning a location or path variable to the backup pic folder called "path"
# Saving the predicted image with different Random names for future uses.
def semi_function():
    call('rm -rf image2.jpg', shell=True)
    sleep(2)
    call('cp -r predictions.jpg /home/pi/Documents/opencv-project/pic/', shell=True)
    path = '/home/pi/Documents/opencv-project/pic/'
    files = os.listdir(path)

    # Setting the datetime function for the image captured
    dtime = datetime.datetime.now()
    dtime = str(dtime)
    new_time = dtime.split(' ')
    new_time = new_time[1]
    new_time = new_time[:8]
    i = new_time



    # Creating a for loop that loops through files in the directory path,
    # we then rename the files with random numbers for any new file created.
    # Then we delete the captured images, the predicted values in .txt files
    for file in files:
        filename, file_extension = os.path.splitext(file)
        i = new_time
        os.rename(os.path.join(path, file), os.path.join(path, filename + str(i) + file_extension))
        i = i
        call('rm -rf predictions.jpg; rm -rf detection/*.txt', shell=True)


# Creating a function that speaks and tells us what was detected using the Google Text To Speech Module.
# Assigning the Predicted values into a variable called detect.
# Assinging the Grep Value for Human into a new variable called fname.
def speech_function():
    detect = "detection/detections.txt"
    fname = "detection/alert.txt"


    # Reading in the save value for the Objects that were detected, and Assigning a
    # Variable to it.
    with open(fname, 'r') as f:
        content = f.read()
    #content = content[:5]
    content = content.rstrip()[:5]

    with open(detect, 'r') as f:
        detection = f.read()

    # Finding the number of Humans Detected
    human_val = re.findall('Human',  detection)
    human_number = len(human_val)

    # Removing the First 84th letters in the Variable, and Assinging it a new variable called "new_value"
    # Split the words present in the variable at the % so that we could make the word easy for the Speech_Function to Read out.
    new_value = detection[84:]
    objects_value = new_value.split("%")
    objects_value = int(len(objects_value))
    detected_objects = objects_value - int(1)
    object_number = int(detected_objects)


    # Calling in the engine functon to speak the word that are present in the variable called "detection"
    # And also then Tell us the Number of Objects that has been detected in the Image Snapped.
    if (human_number >= 2) and (object_number >= 2):
        sleep(2)
        call('mpg321 voice/{}human.mp3 2>/dev/null'.format(human_number), shell=True)
        sleep(2)
        call('mpg321 voice/{}object.mp3 2>/dev/null'.format(object_number), shell=True)



    # Creating a statement to check if the word "Human" is Present in the variable called "content1"
    # And if Present, it should Perform a gTTS function which would tell us that A Human Being has been detected,
    # Then Start A live video Analysis Using YOLO coco Model.
def video_detection():
    fname = 'detection/alert.txt'
    with open(fname, 'r') as f:
        content = f.read()
    content = content.strip()[:5]
    if content == "Human":
        call("mpg321 video/video_detection.mp3 2>/dev/null", shell=True)
        main() 
    
    else:
        pass


# Defining a Function That starts the whole process
# Setting The pin of the PIR sensor to be GPIO input pin 4
# Creating a while Loop that loops forever for if the PIR sensor detects input signals,
# The following functions should run.
def start_actions():
    camera_snap()
    call('mpg321 motion.mp3 2>/dev/null', shell=True)
    pir_mail()
    image_detection()
    speech_function()
    send_mail()

# Setting running to be True, and the pin mode to
# be BCM pin mode for the Raspberry pi.
# Setting GPIO pin 16 to be input for the Pir sensor and
# sleeping for 8 seconds to heat up the PIr sensor to make it Detect Accurate infrared Radiation. 
running = True
GPIO.setmode(GPIO.BCM)
pir_sensor = 16
pir_sensor = int(pir_sensor)
GPIO.setup(pir_sensor, GPIO.IN)
print('Initializing The Pir Sensor......')
sleep(8)


# Creating a while loop that will run all the functions.
while running:
    if GPIO.input(pir_sensor):
        print('motion Detected')
        sleep(1.4)
        start_actions()
        video_detection()
        semi_function() 
    else:
        print('Scanning For motion')

# Performing a cleanup to cleanup the GPIO pins, and
# Stop the PWM signals Before exiting. 
pwm.stop()
GPIO.cleanup()
        







        

    
