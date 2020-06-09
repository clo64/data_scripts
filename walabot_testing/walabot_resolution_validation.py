import WalabotAPI as wala
import time
import keyboard
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 
import time

THRESHOLD = 15

wala.Init()
wala.SetSettingsFolder()
wala.ConnectAny()
wala.SetProfile(wala.PROF_SENSOR)
wala.SetThreshold(THRESHOLD)
wala.SetDynamicImageFilter(wala.FILTER_TYPE_NONE)

min_R, max_R, res_R = 216, 457, 2
wala.SetArenaR(min_R, max_R, res_R)

min_Theta, max_Theta, res_Theta = -19 , 19, 2
wala.SetArenaTheta(min_Theta, max_Theta, res_Theta)

min_Phi, max_Phi, res_Phi = -43, 43, 2
wala.SetArenaPhi(min_Phi, max_Phi, res_Phi)

try:
    wala.Start()
except:
    print('resoltuion out of bounds')