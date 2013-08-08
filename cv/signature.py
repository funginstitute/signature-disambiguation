#!/usr/bin/env python
"""
Toy library for extracting signature from an image
"""
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
from skimage.data import imread
from skimage.color import rgb2gray
from skimage.measure import find_contours
from scipy.spatial import distance
from scipy import stats
from sklearn.cluster import DBSCAN
from itertools import cycle
from collections import defaultdict
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

def run_dbscan(contours, eps=400, min_samples=3):
    """
    Given a list of points, runs DBSCAN with the parameters [eps] and [min_samples].
    Returns list of tuples, where each tuple is (label, contour center)
    """
    pointarray, distances = compute_distance_matrix(contours)
    # run DBSCAN
    db = DBSCAN(eps=eps, min_samples=min_samples).fit(distances)
    labels =  db.labels_
    colors = cycle('bgrcmy')
    for label, color in zip(set(labels), colors):
        if label == -1:
            color = 'k'
        for n, point in enumerate(pointarray):
            if labels[n] == label:
                plt.plot(point[0], point[1], color=color, marker='o')
    return zip(labels, pointarray)

def extract_signature(contours, pointlabels):
    """
    Given the [contours] from compute_contours and the list of (label, point) tuples
    from run_dbscan, finds the most horizontal group of points and draws
    a bounding box around the corresponding group of centroids.
    """
    clusters = defaultdict(list)
    # cluster points by their group
    for k,v in pointlabels:
        if k != -1: # -1 is not a group, so we skip
            clusters[k].append(v)
    if not clusters:
        print 'no signature found'
        return
    # compute linear regression for each group
    fits = {}
    for label, cluster in clusters.iteritems():
        array = np.array(cluster)
        xi = array[:, 0]
        y = array[:, 1]
        slope, intercept, r_value, p_value, std_err = stats.linregress(xi, y)
        # want to minimize slope and error, so we add
        # their absolute values and take the min
        fits[label] = abs(slope) + abs(std_err)
    bestfit_label = min(fits, key=lambda x: fits[x])
    # get indices into the contours list from the list of points
    tmp_points = [tuple(x[1]) for x in pointlabels]
    indices = [tmp_points.index(tuple(x)) for x in clusters[bestfit_label]]
    minx = miny = float('inf')
    maxx = maxy = float('-inf')
    for index in indices:
        contour = contours[index]
        minx = min(minx, min(contour, key=lambda x: x[1])[1])
        miny = min(miny, min(contour, key=lambda x: x[0])[0])
        maxx = max(maxx, max(contour, key=lambda x: x[1])[1])
        maxy = max(maxy, max(contour, key=lambda x: x[0])[0])
    maxx += 10
    maxy += 10
    minx -= 10
    miny -= 10
    x = (minx, maxx, maxx, minx, minx)
    y = (miny, miny, maxy, maxy, miny)
    plt.plot(x, y, '-b', linewidth=2)
    plt.gray()
    plt.imshow(img)
    plt.savefig('out.png')

def iterate(filename, lengths, epsilons, min_samples):
    """
    Given 3 lists of values for [length], [eps] and [min_samples],
    iterates through each of them and does the process above
    """
    imagepath = os.path.join(os.getcwd(), filename)
    img = get_image(imagepath)
    for length in lengths:
        for eps in epsilons:
            for min_sample in min_samples:
                print 'using length={0}, eps={1}, min_sample={2}'.format(length, eps, min_sample)
                contours, lengths = compute_contours(img, length)
                points = run_dbscan(contours, eps, min_sample)
                plt.gray()
                plt.imshow(img)
                plt.savefig('tune/{0}-{1}-{2}.png'.format(length, eps, min_sample))

if __name__=='__main__':
    if len(sys.argv) < 2:
      imagepath = os.path.join(os.getcwd(),'test.tif')
    else:
      imagepath = os.path.join(os.getcwd(), sys.argv[1])
    img = get_image(imagepath)
    contours, lengths = compute_contours(img)
    points = run_dbscan(contours)
    extract_signature(contours, points)

    plt.gray()
    plt.imshow(img)

    plt.savefig('out.png')
