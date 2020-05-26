"""
Writing to process webcam footage only, until walabot is setup
"""

import cv2 as cv
import argparse
import data_processor_functions as dpf

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

#verfiy data files in range
#***add RF data file check after walabot brouth online***
dpf.verifyDataFiles(results.rangestart, results.rangeend)

#once files verified, start the processing?
#We want to extract the pose probability map from each video frame and
#insert it into the correct entry in our .json file.
dpf.probMapFromVideo(results.rangestart, results.rangeend)