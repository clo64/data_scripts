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


