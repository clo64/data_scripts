import cv2 as cv
import keyboard

cap = cv.VideoCapture(0)

fourcc = cv.VideoWriter_fourcc(*'mp4v')

video_out = cv.VideoWriter('vidTest.mp4', fourcc, 20.0, (640, 480))

while True:

    ret, frame = cap.read()

    cv.imshow('frame', frame)

    k = cv.waitKey(1)

    video_out.write(frame)