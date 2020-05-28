# following steps from https://api.walabot.com/_flow.html

from __future__ import print_function

import sys
from sys import platform
from os import system
import WalabotAPI as wlbt
import numpy as np
import cv2
import time
import keyboard
import tkinter as tk

CANVAS_SIZE = 650

# initial file openings
# setup output file
output_file = "walabot_out.txt"
file = open(output_file, "w")

# setup video recording
cap = cv2.VideoCapture(0)
# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
output_text = open("output.txt", "w")

class Walabot_GUI(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        print("Created")
        self.canvas = Canvas_Block()

    def init_loop(self):
        wlbt.Init("C:/Program Files/Walabot/WalabotSDK/bin/WalabotAPI.dll")  # load the WalabotSDK to the Python wrapper
        wlbt.Initialize()  # set the path to the essetial database files

        try:
            wlbt.ConnectAny()  # establishes communication with the Walabot
            status_label["text"] = "Connected to Walabot"
        except wlbt.WalabotError:
            status_label["text"] = "No Walabot found!"
            exit(1)

        wlbt.SetProfile(wlbt.PROF_TRACKER)  # set scan profile out of the possibilities
        # (min, max, resolution) in CM
        wlbt.SetArenaR(10,400,4) # 400cm ~ 13ft
        wlbt.SetArenaTheta(-20,20,10)
        wlbt.SetArenaPhi(-45,45,2)
        wlbt.SetDynamicImageFilter(wlbt.FILTER_TYPE_NONE)  # specify filter to use

        status_label["text"] = "Walbot initialized"

        # start (also does initial calibration)
        wlbt.Start()  # starts Walabot in preparation for scanning

        wlbt.Trigger()
        raw_image, x, y, sliceDepth, power = wlbt.GetRawImageSlice()
        self.canvas.set_grid(x, y)

        status_label["text"] = "Collecting data..."
        self.loop()

    def loop(self):
        wlbt.Trigger()  # initiates a scan and records signals

        raw_image, sizeX, sizeY, sliceDepth, power = wlbt.GetRawImageSlice()

        self.canvas.update(raw_image, sizeX, sizeY)

        # this line is necessary for the canvas to update
        self.cyclesId = self.after_idle(self.loop)

    def shut_down(self):
        self.after_cancel(self.cyclesId)
        wlbt.Stop()  # stops Walabot when finished scanning
        wlbt.Disconnect()  # stops communication with Walabot
        wlbt.Clean()
        file.close()
        output_text.close()
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        status_label["text"] = "Walabot stopped"

class Canvas_Block():
    def __init__(self):
        self.my_canvas = tk.Canvas(
            width=CANVAS_SIZE,
            height=CANVAS_SIZE
        )
        self.my_canvas.configure(background='#' + COLORS[0])
        self.my_canvas.grid(rowspan=3, column=1)

    def set_grid(self, x, y):
        recHeight, recWidth = CANVAS_SIZE // x, CANVAS_SIZE // y
        self.cells = [[
            self.my_canvas.create_rectangle(
                recWidth * col, recHeight * row,
                recWidth * (col + 1), recHeight * (row + 1),
                width=0,
                fill="white")
            for col in range(y)] for row in range(x)]

    def update(self, raw_image, sizeX, sizeY):
        for i in range(sizeX):
            for j in range(sizeY):
                self.my_canvas.itemconfigure(
                    self.cells[sizeX - i - 1][j],
                    fill='#' + COLORS[raw_image[i][j]])


COLORS = [
    "000083", "000087", "00008B", "00008F", "000093", "000097", "00009B",
    "00009F", "0000A3", "0000A7", "0000AB", "0000AF", "0000B3", "0000B7",
    "0000BB", "0000BF", "0000C3", "0000C7", "0000CB", "0000CF", "0000D3",
    "0000D7", "0000DB", "0000DF", "0000E3", "0000E7", "0000EB", "0000EF",
    "0000F3", "0000F7", "0000FB", "0000FF", "0003FF", "0007FF", "000BFF",
    "000FFF", "0013FF", "0017FF", "001BFF", "001FFF", "0023FF", "0027FF",
    "002BFF", "002FFF", "0033FF", "0037FF", "003BFF", "003FFF", "0043FF",
    "0047FF", "004BFF", "004FFF", "0053FF", "0057FF", "005BFF", "005FFF",
    "0063FF", "0067FF", "006BFF", "006FFF", "0073FF", "0077FF", "007BFF",
    "007FFF", "0083FF", "0087FF", "008BFF", "008FFF", "0093FF", "0097FF",
    "009BFF", "009FFF", "00A3FF", "00A7FF", "00ABFF", "00AFFF", "00B3FF",
    "00B7FF", "00BBFF", "00BFFF", "00C3FF", "00C7FF", "00CBFF", "00CFFF",
    "00D3FF", "00D7FF", "00DBFF", "00DFFF", "00E3FF", "00E7FF", "00EBFF",
    "00EFFF", "00F3FF", "00F7FF", "00FBFF", "00FFFF", "03FFFB", "07FFF7",
    "0BFFF3", "0FFFEF", "13FFEB", "17FFE7", "1BFFE3", "1FFFDF", "23FFDB",
    "27FFD7", "2BFFD3", "2FFFCF", "33FFCB", "37FFC7", "3BFFC3", "3FFFBF",
    "43FFBB", "47FFB7", "4BFFB3", "4FFFAF", "53FFAB", "57FFA7", "5BFFA3",
    "5FFF9F", "63FF9B", "67FF97", "6BFF93", "6FFF8F", "73FF8B", "77FF87",
    "7BFF83", "7FFF7F", "83FF7B", "87FF77", "8BFF73", "8FFF6F", "93FF6B",
    "97FF67", "9BFF63", "9FFF5F", "A3FF5B", "A7FF57", "ABFF53", "AFFF4F",
    "B3FF4B", "B7FF47", "BBFF43", "BFFF3F", "C3FF3B", "C7FF37", "CBFF33",
    "CFFF2F", "D3FF2B", "D7FF27", "DBFF23", "DFFF1F", "E3FF1B", "E7FF17",
    "EBFF13", "EFFF0F", "F3FF0B", "F7FF07", "FBFF03", "FFFF00", "FFFB00",
    "FFF700", "FFF300", "FFEF00", "FFEB00", "FFE700", "FFE300", "FFDF00",
    "FFDB00", "FFD700", "FFD300", "FFCF00", "FFCB00", "FFC700", "FFC300",
    "FFBF00", "FFBB00", "FFB700", "FFB300", "FFAF00", "FFAB00", "FFA700",
    "FFA300", "FF9F00", "FF9B00", "FF9700", "FF9300", "FF8F00", "FF8B00",
    "FF8700", "FF8300", "FF7F00", "FF7B00", "FF7700", "FF7300", "FF6F00",
    "FF6B00", "FF6700", "FF6300", "FF5F00", "FF5B00", "FF5700", "FF5300",
    "FF4F00", "FF4B00", "FF4700", "FF4300", "FF3F00", "FF3B00", "FF3700",
    "FF3300", "FF2F00", "FF2B00", "FF2700", "FF2300", "FF1F00", "FF1B00",
    "FF1700", "FF1300", "FF0F00", "FF0B00", "FF0700", "FF0300", "FF0000",
    "FB0000", "F70000", "F30000", "EF0000", "EB0000", "E70000", "E30000",
    "DF0000", "DB0000", "D70000", "D30000", "CF0000", "CB0000", "C70000",
    "C30000", "BF0000", "BB0000", "B70000", "B30000", "AF0000", "AB0000",
    "A70000", "A30000", "9F0000", "9B0000", "970000", "930000", "8F0000",
    "8B0000", "870000", "830000", "7F0000"]

# setup GUI
window = tk.Tk()
window.title("Walabot GUI")
window.rowconfigure([0,1,2], minsize=50, weight=1)
window.columnconfigure([0,1], minsize=50, weight=1)
gui = Walabot_GUI(window)

start_button = tk.Button(
    text="Start Walabot",
    width=25,
    height=5,
    bg="black",
    fg="white",
    master=window,
    command=gui.init_loop
)
start_button.grid(row=1, column=0)

stop_button = tk.Button(
    text="Stop Walabot",
    width=25,
    height=5,
    bg="black",
    fg="white",
    master=window,
    command=gui.shut_down
)
stop_button.grid(row=2,column=0)

status_label = tk.Label(
    text="Click Start",
    width=25,
    height=5,
    bg="gray",
    fg="black",
    master=window
)
status_label.grid(row=0,column=0)

window.mainloop()



