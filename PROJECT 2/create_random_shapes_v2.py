# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 07:23:07 2020

@author: john.hanks
"""


import matplotlib.pyplot as plt
from skimage.exposure import histogram
from skimage.draw import random_shapes
from skimage.measure import label, regionprops, regionprops_table
from skimage.transform import rotate
import numpy as np
from numpy import random

'''

The proram randomly creates objects of different shapes and sizes using circle, rectangles, and triangles.

'''
############ INPUTS #################
MIN_SIZE_OF_SHAPE = 50  # in pixels
MAX_SIZE_OF_SHAPE = 60
SIZE_OF_IMAGE = 200
MAX_ANGLE = 30
MIN_NUMBER_OF_SHAPES = 12
MAX_NUMBER_OF_SHAPES = 16

#################################

# close all figures if any are open
plt.close('all')


result = random_shapes((SIZE_OF_IMAGE, SIZE_OF_IMAGE), 
                       max_shapes=MAX_NUMBER_OF_SHAPES, 
                       min_shapes=MIN_NUMBER_OF_SHAPES, 
                       min_size=MIN_SIZE_OF_SHAPE, 
                       max_size=MAX_SIZE_OF_SHAPE,
                       shape=None,
                       multichannel=False, 
                       allow_overlap=True, 
                       random_seed=None)

# We get back a tuple consisting of (1) the image with the generated shapes
# and (2) a list of label tuples with the kind of shape (e.g. circle,
# rectangle) and ((r0, r1), (c0, c1)) coordinates.
image, labels = result

# create histogram
plt.figure(1)
hist, hist_centers = histogram(image, nbins=256)
plt.plot(hist_centers, hist)
plt.title("Histogram of gray scale values: ")

# show image before threshold
plt.figure(2)
plt.imshow(image , cmap='gray')
plt.title('Before Thrshold')

# threshold and rotate image (use resize True so that objects don't touch the edge)
image = image < (np.max(image))
binary_image = rotate(image, random.randint(MAX_ANGLE),resize=True)
     
print(f"Image shape: {image.shape}\nLabels: {labels}")

# chow the thresholded image
plt.figure(3)
plt.imshow(binary_image , cmap='gray')
plt.title('Random shape at Random Angle')