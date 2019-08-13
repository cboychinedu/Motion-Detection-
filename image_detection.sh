#!/bin/bash 
# Author: Mbonu Chinedum Endurance 
# University: Nnamdi Azikiwe University
# Date Created: 27/01/2019 "Buhari tenor"
# Description: This script will run the YOLOv3 model on the image "image.jpg" file and output the Analysis into a ".txt" file.
# It then looks for a value called "person" in the file 'detections.txt' and outputs it into a '.txt' file called alert. 
# conda activate {envs}  to activate the anaconda environment you are working on..
python3 voc.py >>detection/detections.txt
grep "Human" detection/detections.txt | cut -c 1-5 | head -n 1 >>detection/alert.txt

