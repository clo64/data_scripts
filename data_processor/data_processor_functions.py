"""
Set of functions to aid in processing video and RF files
"""
import os.path
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import time
import json

PATHRAWDATA = '../data/raw/'
PATHPROCCDATA = '../data/processed/'
VIDNAME = 'rbg_'
VIDEXT = '.mp4'
FRAMENAME = 'framedata_'
FRAMEEXT = '.json'

def verifyDataFiles(start, end):

    print('Verifying all files exist...')

    for i in range(int(start), int(end)+1):
        vidName = PATHRAWDATA + VIDNAME + str(i) + VIDEXT
        frameDataName = PATHRAWDATA + FRAMENAME + str(i) + FRAMEEXT

        #Check for all video files
        if(os.path.exists(vidName)):
            flag = 'found'
            print('{0:35}...    {1:6}'.format(vidName, flag))
        else:
            flag = 'failed'
            print('{0:35}...    {1:6}'.format(vidName, flag))
            print(vidName + ' not found, check files')
            exit()

        #Check for all frame data files
        if(os.path.exists(frameDataName)):
            flag = 'found'
            print('{0:35}...    {1:6}'.format(frameDataName, flag))
        else:
            flag = 'failed'
            print('{0:35}...    {1:6}'.format(frameDataName, flag))
            print(frameDataName + ' not found, check files')
            exit()

        #**Check for RF data files in future**

def probMapFromVideo(start, end):

    frameProcessingCount = 1
    body_parts = MPIBodyParts()
    pose_pairs = MPIPosePairs()

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

           

            frameData[str(int(currentFrame))].append(out.tolist())
            frameData[str(int(currentFrame))].append(points)

            
            #***for visualization ONLY, remove for large data proccesing event***
            probmapVIS1 = cv.resize(probmapVIS1, (frameWidth, frameHeight))
            plotProbMap(probmapVIS1, frame)

            #***for point visualization ONLY, remove for large data processing event***
            #Points are already scaled to original image size
            for i in range(15):
                cv.circle(frame, points[i], 5, (25, 0, 255), 5)
            cv.imshow('frame', frame)
            

        #After each vid proccess, write to proccessed json file
        
        with open(PATHPROCCDATA + FRAMENAME + str(i) + FRAMEEXT, 'w') as fp:
            json.dump(frameData, fp)
        
    
            

def plotProbMap(probmap, frame):
    plt.imshow(cv.cvtColor(frame, cv.COLOR_BGR2RGB))
    plt.imshow(probmap, alpha=0.6)
    plt.pause(.03)
    plt.show()

def MPIBodyParts():
    return { "Head": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
            "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
            "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "Chest": 14,
            "Background": 15 }

def MPIPosePairs():
    return [ ["Head", "Neck"], ["Neck", "RShoulder"], ["RShoulder", "RElbow"],
            ["RElbow", "RWrist"], ["Neck", "LShoulder"], ["LShoulder", "LElbow"],
            ["LElbow", "LWrist"], ["Neck", "Chest"], ["Chest", "RHip"], ["RHip", "RKnee"],
            ["RKnee", "RAnkle"], ["Chest", "LHip"], ["LHip", "LKnee"], ["LKnee", "LAnkle"] ]


