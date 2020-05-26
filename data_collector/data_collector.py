"""
Writing for webcam data collection until
walabot is received
"""
import cv2 as cv
import numpy as np
from datetime import datetime
import json
import time
import argparse
import os.path

#Argument parsing block to receive data session number as integer.
parser = argparse.ArgumentParser()
parser.add_argument('-datasession', action='store', dest='datasession', type=str, help='Enter the data session number for file naming',
required=True)
results = parser.parse_args()

#Check to ensure datasession files don't already exist
if(os.path.exists('../data/raw/framedata_' + results.datasession + '.json') or (os.path.exists('../data/raw/rbg_' + results.datasession + '.mp4'))):
    print('Data session files already exist, cannot overwrite')
    exit()

cap = cv.VideoCapture(1)
time.sleep(2)

#video capture dimensions must be correctly set
#for write to file success
cap.set(3, 640)
cap.set(4, 480)

#assuming .mp4 is widely portable
#20 frames per second
fourcc = cv.VideoWriter_fourcc(*'mp4v')
out = cv.VideoWriter('../data/raw/rbg_' + results.datasession + '.mp4', fourcc, 20.0, (640, 480))

#rgbTimeStamp dictionary agregates frame number and timestamp
rgbTimeStamp = {}
frameCount = 1
global_Timer = 0
iteration = 0

while True:
    ret, frame = cap.read()
    out.write(frame)
    
    rgbTimeStamp.update({frameCount: [str(datetime.now())] })
    print(datetime.now())

    frameCount += 1

    cv.imshow('frame', frame)
    
    if(cv.waitKey(1) & 0xFF == ord('q')):
        #on quit write timestamp to file, JSON format
        with open('../data/raw/framedata_' + results.datasession + '.json', 'w') as fp:
            json.dump(rgbTimeStamp, fp, indent=2)
        break

cap.release()
cv.destroyAllWindows()

