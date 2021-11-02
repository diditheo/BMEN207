# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 12:01:04 2021

@author: didit
"""

import matplotlib.pyplot as plt
import skimage.transform as transform
import matplotlib.image as mpimg
import numpy as np
import skimage.morphology as morphology
import skimage.measure as meas
import math
from skimage import data #built in images .camera and .cell for test
from skimage.color import rgb2gray
from skimage.exposure import histogram
from skimage.filters import threshold_minimum #automated threshold
#_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-

#USER INPUTS================================================
file_path = "C:\\Users\\didit\\Desktop\\BMEN 207\\PROJECT 2\\mole_data\\mole_data\\"
image_file_name = "mole_1.png"

#===========================================================



#rbg scale image
original = mpimg.imread(file_path + image_file_name)

#converts image to grayscale
grayscale = rgb2gray(original)



plt.figure(1)
hist, hist_centers = histogram(grayscale, nbins=256)
plt.plot(hist_centers, hist)
plt.title("Histogram of Grayscale values for cell image")
