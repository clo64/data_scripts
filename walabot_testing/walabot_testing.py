#import matplotlib.pyplot as plt
import WalabotAPI as wala
from imp import load_source
import cv2 as cv
import time
import numpy as np

#wala = load_source('WalabotAPI',
#'C:/Program Files/Walabot/WalabotSDK/python/WalabotAPI.py')

#defines minimum reflective power to image
THRESHOLD = 35

wala.Init()
wala.SetSettingsFolder()
wala.ConnectAny()
wala.SetProfile(wala.PROF_SENSOR)
wala.SetThreshold(THRESHOLD)
wala.SetDynamicImageFilter(wala.FILTER_TYPE_NONE)

walaPairs = wala.GetAntennaPairs()

#40 antenna pairs
print(len(walaPairs))

wala.Start()

antenna = len(walaPairs)

dataFile = open('walaDataFile', 'w')

wala.StartCalibration()

while wala.GetStatus()[0] == wala.STATUS_CALIBRATING:
    wala.Trigger()

#img = np.zeros((39, 27), dtype='uint8')

while True:

    wala.Trigger()
    mySlice, sizeX, sizeY, depth, power = wala.GetRawImageSlice()
    print(mySlice)

    img = np.array(mySlice, dtype='uint8')

    #img[1] = mySlice[1:]
    #img = mySlice[0:27]
    img2 = img[:, :, np.newaxis]

    print('Size x: {}'.format(sizeX))
    print('Size Y: {}'.format(sizeY))

    img2 = cv.resize(img2, (390, 270), interpolation=cv.INTER_AREA)
    print(img2.shape)
    cv.imshow('Test', img2)
    k = cv.waitKey(1)
    #cv.destroyAllWindows()
    time.sleep(1)
