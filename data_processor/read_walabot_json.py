"""
Quick practice script to learn how to use ijson

Goal is to read very large JSON files without loading into
memory

note: ijson likes files opened in binary format
"""

import ijson
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import rasterio

min_R, max_R, res_R = 30, 200, 4
min_Theta, max_Theta, res_Theta = -40, 40, 4
min_Phi, max_Phi, res_Phi = -40, 40, 4

# rb flag opens file in binary
json_to_parse = open('../data/raw/wala_1.json', 'rb')

test_object = ijson.items(json_to_parse, '25')

1

print(wala_data_array)
print(wala_data_array.shape)

fig = plt.figure()
ax = plt.axes(projection='3d')



    


