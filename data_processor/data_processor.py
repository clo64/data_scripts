"""
Writing to process webcam footage only, until walabot is setup

todo: 
write JSON file every ?x? iterations to prevent memory exhaustion 

functionalize processing elements

flag for selective capture of openpose data elements

walabot processing -> convert to cartesian coordinates
                      dimensional reduction
                      ?
"""

import cv2 as cv
import argparse
import data_processor_functions as dpf
import os.path
import numpy as np
import matplotlib.pyplot as plt
import time
import json

PATHRAWDATA = '../data/raw/'
VIDNAME = 'rbg_'
VIDEXT = '.mp4'
FRAMENAME = 'framedata_'
FRAMEEXT = '.json'

parser = argparse.ArgumentParser()
parser.add_argument('-rangestart', action='store', dest='rangestart', help='Enter the starting data session number',
required=True)
parser.add_argument('-rangeend', action='store', dest='rangeend', help="Enter the ending data session number",
required=True)
results = parser.parse_args()

start = results.rangestart
end = results.rangeend

#verfiy data files in range
#***add RF data file check after walabot is online***
dpf.verifyDataFiles(start, end)

body_parts = dpf.MPIBodyParts()
pose_pairs = dpf.MPIPosePairs()

#Required to refresh matplotlib heatmap overlay
plt.ion()

for i in range(int(start), int(end)+1):
    vidName = PATHRAWDATA + VIDNAME + str(i) + VIDEXT
    frameDataName = PATHRAWDATA + FRAMENAME + str(i) + FRAMEEXT

    jsonFile = open(frameDataName)
    frameData = json.load(jsonFile)

    cap = cv.VideoCapture(vidName)

    length = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    print(str(length) + ' frames to process from ' + vidName)

    net = cv.dnn.readNet(os.path.relpath('openpose_pose_mpi_faster_4_stages.prototxt'), 
    os.path.relpath('pose_iter_160000.caffemodel'))

    while True:
        hasFrame, frame = cap.read()
        currentFrame = cap.get(cv.CAP_PROP_POS_FRAMES)

        #End of video will trigger break
        if(not hasFrame):
            print('done')
            break

        frameWidth = frame.shape[1]
        frameHeight = frame.shape[0]

        blob = cv.dnn.blobFromImage(frame, 1.0 / 255, (640, 480), (0, 0, 0), swapRB=False, crop=False)
        net.setInput(blob)
        print('Processing frame ' + str(currentFrame))
        out = net.forward()

        #agregate full heatmap into one data structure
        
        probmapVIS1 = out[0, 0, :, :]
        probmapVIS2 = out[0, 1, :, :]
        probmapVIS3 = out[0, 2, :, :]
        probmapVIS4 = out[0, 3, :, :]
        """
        for j in range(1, len(body_parts)):
            probmapVIS = probmapVIS + out[0, j, :, :]
        """
        
        points = []
        for j in range(0, len(body_parts)):
            probmapPoints = out[0, j, :, :]
            _, conf, _, point = cv.minMaxLoc(probmapPoints)

            x = ((frameWidth * point[0]) / out.shape[3])
            y = ((frameHeight * point[1]) / out.shape[2])

            points.append((int(x), int(y)) if conf > .1 else None)

        
        #Currently appending all openpose data, probability part map and affinity map
        frameData[str(int(currentFrame))].append(out.tolist())
        frameData[str(int(currentFrame))].append(points)

        
        #***for visualization ONLY, remove for large data proccesing event***
        probmapVIS1 = cv.resize(probmapVIS1, (frameWidth, frameHeight))
        dpf.plotProbMap(probmapVIS1, frame)

        #***for point visualization ONLY, remove for large data processing event***
        #Points are already scaled to original image size
        for i in range(15):
            cv.circle(frame, points[i], 5, (25, 0, 255), 5)
        cv.imshow('frame', frame)
        

    #After each vid proccess, write to proccessed json file
    
    with open(PATHPROCCDATA + FRAMENAME + str(i) + FRAMEEXT, 'w') as fp:
        json.dump(frameData, fp)