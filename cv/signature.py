#!/usr/bin/env python
"""
Toy library for extracting signature from an image
"""
import matplotlib.pyplot as plt
import numpy as np
from skimage.filter import sobel, canny
from skimage.feature import corner_harris, corner_subpix, corner_peaks
from skimage.data import imread
from skimage.color import rgb2gray
from skimage.transform import probabilistic_hough
from skimage.measure import find_contours
import math
import os

imagepath = os.path.join(os.getcwd(),'test.tif')

# read in image file, convert to grayscale so we can do algorithms on it
img = imread(imagepath)
img = img > 0.9
img = rgb2gray(img)

contours = find_contours(img, 0.9)
for n, contour in enumerate(contours):
    std1, std2 = np.std(contour[:, 1]), np.std(contour[:, 0])
    len1, len2 = len(contour[:, 1]), len(contour[:, 0])
    #if std1 > 20 or std2 > 20:
    #    plt.plot(contour[:, 1], contour[:, 0], linewidth=1)
    if (len1 > 300 or len2 > 300):
        print len1, len2
        plt.plot(contour[:, 1], contour[:, 0], linewidth=1)
        

plt.gray()
plt.imshow(img)


#sobel_edges = sobel(img)
#canny_edges = canny(img, sigma=5)
#lines = probabilistic_hough(canny_edges, threshold=10, line_length=10, line_gap=5)
#plt.imshow(canny_edges * 0)
#for line in lines:
#      p0, p1 = line
#      plt.plot((p0[0], p1[0]), (p0[1], p1[1]))

#fig, axis0 = plt.subplots(ncols=1)
#axis0.imshow(out, cmap=plt.cm.gray)
plt.savefig('out.png')
