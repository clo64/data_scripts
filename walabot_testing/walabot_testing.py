import matplotlib.pyplot as plt
import WalabotAPI as wala
from imp import load_source
import cv2 as cv
import time
import numpy as np

#wala = load_source('WalabotAPI',
#'C:/Program Files/Walabot/WalabotSDK/python/WalabotAPI.py')

#defines minimum reflective power to image
THRESHOLD = 15

wala.Init()

wala.SetSettingsFolder()
wala.ConnectAny()
wala.SetProfile(wala.PROF_SENSOR)
wala.SetThreshold(THRESHOLD)
wala.SetDynamicImageFilter(wala.FILTER_TYPE_NONE)

minInCm, maxInCm, resInCm = 30, 200, 4
wala.SetArenaR(minInCm, maxInCm, resInCm)
"""
minInDegrees, maxInDegrees, resInDegrees = -30, 30, 5
minPhiInDegrees, maxPhiInDegrees, resPhiInDegrees = -20, 20, 5

wala.SetArenaR(minInCm, maxInCm, resInCm)
wala.SetArenaTheta(minInDegrees, maxInDegrees, resInDegrees)
wala.SetArenaPhi(minPhiInDegrees, maxPhiInDegrees, resPhiInDegrees)
"""
wala.SetDynamicImageFilter(wala.FILTER_TYPE_NONE)


wala.Start()
wala.StartCalibration()

stat, prog = wala.GetStatus()
wala.Trigger()
while stat == wala.STATUS_CALIBRATING and prog < 100:
    wala.Trigger()
    print("Calibrating " + str(prog) + "%")
    stat, prog = wala.GetStatus()

walaPairs = wala.GetAntennaPairs()

#40 antenna pairs
print(len(walaPairs))

antenna = len(walaPairs)

dataFile = open('walaDataFile', 'w')

#img = np.zeros((39, 27), dtype='uint8')

while True:

    wala.Trigger()
    mySlice, sizeX, sizeY, depth, power = wala.GetRawImageSlice()
    print(mySlice)

    img = np.array(mySlice, dtype=np.uint8)

    #img[1] = mySlice[1:]
    #img = mySlice[0:27]
    img2 = img[:, :, np.newaxis]

    print('Size x: {}'.format(sizeX))
    print('Size Y: {}'.format(sizeY))

    plt.imshow(mySlice)
    plt.pause(0.05)
    """
    img2 = cv.resize(img2, (sizeX*10, sizeY*10), interpolation=cv.INTER_AREA)
    print(img2.shape)
    cv.imshow('Test', img2)
    k = cv.waitKey(1)
    #cv.destroyAllWindows()
    """
    time.sleep(1)

plt.show()
wala.Stop()
wala.Disconnect()
wala.Clean()


