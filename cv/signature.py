#!/usr/bin/env python
"""
Toy library for extracting signature from an image
"""
import matplotlib.pyplot as plt
import numpy as np
from skimage.data import imread
from skimage.color import rgb2gray
from skimage.measure import find_contours
from scipy.spatial import distance
from sklearn.cluster import DBSCAN
from itertools import cycle
import math
import os
import sys


def get_center(pointlist):
    """
    Takes in a list of tuples (x,y) and returns the average coordinate
    """
    return np.mean(pointlist, axis=0)

def get_image(imagepath):
    """
    Given an imagepath [string], takes a binary threshold of the image
    and converts it to gray scale before returning
    """
    img = imread(imagepath)
    img = img > 0.9
    img = rgb2gray(img)
    return img

def compute_contours(img, length=300):
    """
    Given an Image object, finds the contours. Filters
    the contours by how long they are (this is the optional length
    argument)

    Returns:
    ret_contours (list of contours),
    ret_lengths (list of lengths of each contour in ret_contours)
    """
    contours = find_contours(img, 0.9)
    contour_lengths = [len(x[:, 1]) for x in contours]
    ret_contours = []
    ret_lengths = []
    for contour in contours:
        if (contour.shape[0] >= length):
            plt.plot(contour[:, 1], contour[:, 0])
            ret_contours.append(contour)
            ret_lengths.append(contour.shape[0])
    return ret_contours, ret_lengths

def compute_distance_matrix(contours, normalize=False):
    """
    Given a list of contours, computes the centroid
    of each contour and inserts it into a distance
    matrix of all contour centers. If normalize is True,
    the distances are normalized where 1 is the same point
    """
    tmp = [zip(contour[:, 1], contour[:, 0]) for contour in contours]
    points = [get_center(pointlist) for pointlist in tmp]
    pointarray = np.array(points)
    D = distance.squareform(distance.pdist(pointarray))
    if normalize:
        return pointarray, 1 - (D / np.max(D))
    return pointarray, D

def run_dbscan(contours, eps=20, min_samples=2):
    """
    Given a list of points, runs DBSCAN with the parameters [eps] and [min_samples].
    Returns list of tuples, where each tuple is (label, contour center)
    """
    pointarray, distances = compute_distance_matrix(contours)
    # run DBSCAN
    db = DBSCAN(eps=20, min_samples=2).fit(distances)
    labels =  db.labels_

    colors = cycle('bgrcmy')
    for label, color in zip(set(labels), colors):
        if label == -1:
          color = 'k'
        for n, point in enumerate(pointarray):
            if labels[n] == label:
                plt.plot(point[0], point[1], color=color, marker='o')
    return zip(labels, pointarray)

if __name__=='__main__':
    if len(sys.argv) < 2:
      imagepath = os.path.join(os.getcwd(),'test.tif')
    else:
      imagepath = os.path.join(os.getcwd(), sys.argv[1])
    img = get_image(imagepath)
    contours, lengths = compute_contours(img)
    points = run_dbscan(contours)

    plt.gray()
    plt.imshow(img)

    plt.savefig('out.png')
