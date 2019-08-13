#!/usr/bin/env python3
"""
DESCRIPTION:
	This Script would load a machine learning Model That was Trained on the Pascal Voc Object detection dataset,
	and run its Algorithm on an image to Predict the objects that are Present in it.
	The Predictions Gotten would be redirected to another script for analysis using Stream Redirection.
"""

# importing the necessary packages
import numpy as np
import os
import cv2
import time

# Loading in the Path to the Predicted image and The YOLOv3 model that was
# Trained on the Pascal VOC Object Detection Dataset.
# Setting 0.5 to be the Default value for confidence And
# 0.3 to be the default value for the threshold.
yolo = 'yolo-coco'
img = 'image.jpg'
confidence = float(0.5)
threshold = float(0.3)


# Loading the COCO class labels our YOLO model was trained on 
labelsPath = os.path.join(yolo, "coco.names")
LABELS = open(labelsPath).read().strip().split("\n")

# initialize a list of colors to represent each possible class label 
np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
	dtype="uint8")

# derive the paths to the YOLO weights and model configuration 
weightsPath = os.path.join(yolo, "yolov3.weights")
configPath = os.path.join(yolo, "yolov3.cfg")

# Loading our YOLO object detector trained on COCO dataset (80 classes)
print("loading Voc Model from disk...")
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

# load our input image and grab its spatial dimensions
image = cv2.imread(img)
(H, W) = image.shape[:2]

# determine only the *output* layer names that we need from YOLO
ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# construct a blob from the input image and then perform a forward
# pass of the YOLO object detector, giving us our bounding boxes and
# associated probabilities
blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
	swapRB=True, crop=False)
net.setInput(blob)
start = time.time()
layerOutputs = net.forward(ln)
end = time.time()
# Assigning the predicted time value a variable called Tchange
# and displaying the first 4 values of the time it took to predict the image. 
time_change = end - start
time_change = str(time_change)
Tchange = time_change[:4]

# show timing information on YOLO
print("Voc Model took {} seconds".format(Tchange))
print("The Image Analysed are as follows: ")

# initialize our lists of detected bounding boxes, confidences, and 
# class IDS, respectively. 
boxes = []
confidences = []
classIDs = []

# loop over each of the layer outputs
for output in layerOutputs:
	# loop over each of the detections
	for detection in output:
		# extract the class ID and confidence (i.e., probability) of
		# the current object detection
		scores = detection[5:]
		classID = np.argmax(scores)
		confidence = scores[classID]

		# filter out weak predictions by ensuring the detected
		# probability is greater than the minimum probability
		if confidence >= confidence:
			# scale the bounding box coordinates back relative to the
			# size of the image, keeping in mind that YOLO actually
			# returns the center (x, y)-coordinates of the bounding
			# box followed by the boxes' width and height
			box = detection[0:4] * np.array([W, H, W, H])
			(centerX, centerY, width, height) = box.astype("int")

			# use the center (x, y)-coordinates to derive the top and
			# and left corner of the bounding box
			x = int(centerX - (width / 2))
			y = int(centerY - (height / 2))

			# update our list of bounding box coordinates, confidences,
			# and class IDs
			boxes.append([x, y, int(width), int(height)])
			confidences.append(float(confidence))
			classIDs.append(classID)


# apply non-maxima suppression to supress weak, overlapping bounding
# boxes 
idxs = cv2.dnn.NMSBoxes(boxes, confidences, confidence,
						threshold)

# Ensure at least one detection exists 
if len(idxs) > 0:
	# loop over the indexes we are keeping 
	for i in idxs.flatten():
		# extract the bounding box coordinates 
		(x, y) = (boxes[i][0], boxes[i][1])
		(w, h) = (boxes[i][2], boxes[i][3])

		# draw a bounding box rectangle and label on the image 
		color = [int(c) for c in COLORS[classIDs[i]]]
		cv2.rectangle(image, (x, y), (x + w, y + h), color, 3)
		text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
		#print("{}".format(text))

		# Spliting the predicted value and converting it into a floating point number
		# Rounding up the predictied value to 2 decimal places, for an effective text to speech output.
		value = text.split(":")[0]
		percent = text.split(":")[1]
		percent = percent[1:5]
		# Converting the prediction rating into a floating point number, and
		# then assigning it a new variable called percent. 
		percent = float(percent)*100
		percent = str(percent)
		# Printing the predicted value on the screen with its percentage ratings. 
		print(value+':', percent+"%.")
		cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
			0.5, color, 2)

# Saving the Predicted image values.
cv2.imwrite("predictions.jpg", image)
exit()
