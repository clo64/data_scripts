import cv2 as cv
import numpy as np 
import matplotlib.pyplot as plt 
import os.path

PATHRAWDATA = '../data/raw/'
VIDNAME = 'rbg_'
VIDEXT = '.mp4'
FRAMENAME = 'framedata_'
FRAMEEXT = '.json'

body_parts = { "Head": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
            "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
            "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "Chest": 14,
            "Background": 15 }

imageName = 'simple_pose.jpg'

cap = cv.imread(os.path.relpath(imageName))

net = cv.dnn.readNet(os.path.relpath('openpose_pose_mpi_faster_4_stages.prototxt'), 
    os.path.relpath('pose_iter_160000.caffemodel'))

height, width, depth = cap.shape

print(height)
print(width)
print(depth)

blob = cv.dnn.blobFromImage(cap, 1.0 / 255, (640, 480), (0, 0, 0), swapRB=False, crop=False)

net.setInput(blob)

out = net.forward()

print(out[0, 0, :, :])

print(out.shape)

print(out.shape[3])

cv.imshow('map', out[0, 0])

k = cv.waitKey(0)
