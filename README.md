# Motion Detection By The Use Of A Passive Infrared Sensor And A Neural Net.

## Description 
This program was written to detect objects, animals and human beings by the use of a pir(Passive Infrared Sensor) and a Raspberry pi camera. 
The image captured is passed into a neural net that runs a machine learning algorithm on the image to actually predict the object or body that caused the motion. 

## Installation 
For the Program to work, install the Necessary packages and note that the program was implemented on a linux machine. 

# The Python Packages Needed Are:
pip install opencv-python==3.4.2.16 
pip install flask 
pip install flask_basicauth 
pip install RPi.GPIO 
pip install numpy 
pip install video 
pip install picamera 
pip install smtplib 

# The Linux Packages Needed Are:
sudo apt-get install python3-opencv 
sudo apt-get install espeak 
sudo apt-get update 
sudo apt-get upgrade -y 

## Implementation 
This project is implement using the raspberry pi 3 B+, PIR sensor, and a servo-motor.


















