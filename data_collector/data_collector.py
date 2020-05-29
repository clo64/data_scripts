"""
Writing for webcam data collection until
walabot is received

Known issue: Writing to json using built-in library jas 
extreme limitation of pausing to create entire json strucure prior to writing
investigation a streaming version of json-write

ijson can be used for iterative parsing
Looks like possibly jsonstreams, but it's in beta... See if it works anyway???
"""
import matplotlib.pyplot as plt
import WalabotAPI as wala
import cv2 as cv
import numpy as np
from datetime import datetime
import json
import time
import argparse
import os.path

# Argument parsing block to receive data session number as integer.
    # Script expects input as -datasession <integer>
    # Input defines common file name association for 
    # video, timestamp and walabot

parser = argparse.ArgumentParser()
parser.add_argument('-datasession', action='store', dest='datasession', type=str, help='Enter the data session number -datasession <integer>',
required=True)
parse_results = parser.parse_args()

# Check to ensure datasession files don't already exist

if(os.path.exists('../data/raw/framedata_' + parse_results.datasession + '.json') or (os.path.exists('../data/raw/rbg_' + parse_results.datasession + '.mp4'))):
    print('Data session files already exist, cannot overwrite')
    exit()

# Walbot Initialization
    # SetProfile is chosen from a number of options, see Walabot API
    # SetThreshold defines the minimum reflected power to be imaged
    # SetDynamicImageFilter is chosen from a number of options, see walabot API

THRESHOLD = 15

wala.Init()
wala.SetSettingsFolder()
wala.ConnectAny()
wala.SetProfile(wala.PROF_SENSOR)
wala.SetThreshold(THRESHOLD)
wala.SetDynamicImageFilter(wala.FILTER_TYPE_NONE)

# Walabot 'Arena' settings
    # *_R values define spherical radial distance of imaging
    # All res_* values determine angle in degrees between antenna 
    # Some Arena settings commented out for testing

min_R, max_R, res_R = 30, 200, 4
wala.SetArenaR(min_R, max_R, res_R)
"""
min_Theta, max_Theta, res_Theta = -30, 30, 5
wala.SetArenaTheta(min_Theta, max_Theta, res_Theta)

min_Phi, max_Phi, res_Phi = -20, 20, 5
wala.SetArenaPhi(min_Phi, max_Phi, res_Phi)
"""

# Start Walabot and perform calibration

wala.Start()
wala.StartCalibration()

calibration_status, calibration_progress = wala.GetStatus()
wala.Trigger()

while calibration_status == wala.STATUS_CALIBRATING and calibration_progress < 100:
    wala.Trigger()
    print("Calibrating " + str(calibration_progress) + '%')
    calibration_status, calibration_progress = wala.GetStatus()

# Initialize video camera. Wait 1 second for 'warmup'

cap = cv.VideoCapture(0)
time.sleep(1)

# WebCam capture dimensions, a cv2 method

cap.set(3, 640)
cap.set(4, 480)

# Video Codec settings. See fourcc.org for more info

fourcc = cv.VideoWriter_fourcc(*'mp4v')

# Set write path destination for video output and walabot data

video_out = cv.VideoWriter('../data/raw/rbg_' + parse_results.datasession + '.mp4', fourcc, 20.0, (640, 480))
wala_out = ('../data/raw/wala_' + parse_results.datasession + '.json')

# time_stamp dictionarey to agregate frame number and timestamp
# frame_count used to incrimente every loop, matches frame captures

time_stamp = {}
frame_count = 1

while True:

# Trigger the walabot  for a frame, then read a camera frame

    wala.Trigger()
    ret, frame = cap.read()

# Write a single video frame to file then
# write a single walabot entry to the json stream

    video_out.write(frame)
    
    time_stamp.update({frame_count: [str(datetime.now())] })
    print(datetime.now())

    frame_count += 1

    cv.imshow('frame', frame)
    
    if(cv.waitKey(1) & 0xFF == ord('q')):
        #on quit write timestamp to file, JSON format
        with open('../data/raw/framedata_' + parse_results.datasession + '.json', 'w') as fp:
            json.dump(time_stamp, fp, indent=2)
        break

cap.release()
cv.destroyAllWindows()

