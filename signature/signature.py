import matplotlib.pyplot as plt
import numpy as np
from skimage.data import imread
from skimage import io
from skimage.color import rgb2gray
from skimage.measure import find_contours
from skimage.transform import probabilistic_hough_line
from itertools import cycle
from pylab import *
from PIL import Image
import os
import shutil
import sys
import pandas as pd
from skimage.morphology import square, erosion
from skimage.filter import hsobel
from scipy.spatial.distance import euclidean
from scipy.signal import convolve2d, convolve

## CONSTANTS ##
CONTOUR_MINLENGTH = 200

def compute_contours(img, length=300, value=0.1):
    """
    Given an Image object, finds the contours. Filters
    the contours by how long they are (this is the optional length
    argument)

    Returns:
    ret_contours (list of contours),
    ret_lengths (list of lengths of each contour in ret_contours)
    """
    length = CONTOUR_MINLENGTH
    contours = find_contours(img, value)
    contour_lengths = [len(x[:, 1]) for x in contours]
    ret_contours = []
    ret_lengths = []
    for contour in contours:
        if (contour.shape[0] >= length):
            ret_contours.append(contour)
            ret_lengths.append(contour.shape[0])
    return ret_contours, ret_lengths

def get_boundingboxes(contours, plot=False):
    """
    Given a list of contours, computes the bounding box
    for each and returns the list
    """
    boxes = []
    for contour in contours:
        # compute bounding box coordinates
        minx = miny = float('inf')
        maxx = maxy = float('-inf')
        minx = min(minx, min(contour, key=lambda x: x[1])[1])
        miny = min(miny, min(contour, key=lambda x: x[0])[0])
        maxx = max(maxx, max(contour, key=lambda x: x[1])[1])
        maxy = max(maxy, max(contour, key=lambda x: x[0])[0])
        if plot:
            x = (minx, maxx, maxx, minx, minx)
            y = (miny, miny, maxy, maxy, miny)
            plt.plot(x,y,'-b',linewidth=2)
        boxes.append( map(int,(minx,miny,maxx,maxy)) )
    return boxes

def boundingbox(contour):
    """
    Given a list of contours, computes the bounding box
    for each and returns the list
    """
    # compute bounding box coordinates
    minx = miny = float('inf')
    maxx = maxy = float('-inf')
    minx = int(min(minx, min(contour, key=lambda x: x[1])[1]))
    miny = int(min(miny, min(contour, key=lambda x: x[0])[0]))
    maxx = int(max(maxx, max(contour, key=lambda x: x[1])[1]))
    maxy = int(max(maxy, max(contour, key=lambda x: x[0])[0]))
    return (minx,miny,maxx,maxy)

def boundingboxcorners(box):
    minx,miny,maxx,maxy = box
    corners = []
    for x in (minx,maxx):
        for y in (miny,maxy):
            corners.append((x,y))
    return corners

def mergeboxes(box1,box2):
    minx1,miny1,maxx1,maxy1 = box1
    minx2,miny2,maxx2,maxy2 = box2
    minx = min(minx1,minx2)
    maxx = max(maxx1,maxx2)
    miny = min(miny1,miny2)
    maxy = max(maxy1,maxy2)
    return (minx,miny,maxx,maxy)

def is_box_in_box(corners1, corners2):
    """
    returns True if corners1 is in-part contained
    inside corners2
    """
    min_x = min(map(lambda x: x[0], corners2))
    max_x = max(map(lambda x: x[0], corners2))
    min_y = min(map(lambda x: x[1], corners2))
    max_y = max(map(lambda x: x[1], corners2))
    width = max_x - min_x
    height = max_y - min_y
    for p in corners1:
        if p[0] >= min_x and p[1] >= min_y and \
           p[0] < min_x+width and p[1] < min_y+height:
                return True
    return False
    

def do_merge(corners1, corners2):
    for corner1 in corners1:
        for corner2 in corners2:
            if euclidean(corner1,corner2) < 100:
                return True
    if is_box_in_box(corners1, corners2) or is_box_in_box(corners2, corners1):
        return True
    return False


def link_contours(contours):
    # check overlaps
    # remove flat lines
    merged = True
    boxes = map(boundingbox, contours)
    iterations_left = len(boxes)
    old_boxes = None
    for i in range(10*len(boxes)):
        if iterations_left == 0:
            print 'none',i,boxes
            break
        box1 = boxes.pop(0)
        iterations_left -= 1
        corners1 = boundingboxcorners(box1)
        for index,box2 in enumerate(boxes):
            corners2 = boundingboxcorners(box2)
            if do_merge(corners1, corners2):
                boxes.pop(index)
                boxes.append(mergeboxes(box1,box2))
                iterations_left += 1
                merged=True
                break
            else:
                if box1 not in boxes:
                    boxes.append(box1)
                merged = False
    print i,len(contours)
    return boxes
                        
def process(filename):
    imagepath = os.path.join(os.getcwd(), filename)
    orig_img = io.imread(filename,True,'pil')
    img = orig_img > 0.9 # binary threshold
    lines = probabilistic_hough_line(hsobel(img),line_length=200)
    for l in lines:
        x0, x1 = l[0][0],l[1][0]
        y = l[0][1]
        for x in range(x0,x1):
            img[y+1,x] = 1
            img[y,x] = 1
            img[y-1,x] = 1
    erode_img = erosion(img, square(2))
    contours, lengths = compute_contours(erode_img,0.8)
    lengths = pd.Series(lengths)
    lengths = lengths[lengths > 400]
    for i in lengths.index:
        contour = contours[i]
        box = get_boundingboxes([contour])[0]
        x_sum = sum(map(abs, np.gradient(contour[:,1])))
        y_sum = sum(map(abs, np.gradient(contour[:,0])))
        area = (box[2] - box[0]) * (box[3] - box[1])
        plt.plot(contour[:,1],contour[:,0])
    contours = [contours[i] for i in lengths.index]
    newboxes = set(link_contours(contours))
    retboxes = []
    for box in newboxes:
        minx,miny,maxx,maxy = box
        x = (minx, maxx, maxx, minx, minx)
        y = (miny, miny, maxy, maxy, miny)
        area = (maxx-minx) * (maxy-miny)
        if area > 10000:
            retboxes.append(box)
            plt.plot(x, y, '-b', linewidth=2)
    imshow(erode_img)
    return retboxes, contours

if __name__=='__main__':
    plt.gray()
    f = plt.figure(figsize=(16,12))
    filename = sys.argv[1]
    basename = ''.join(filename.split('/')[-1].split('.')[:-1])
    boxes, contours = process(filename)
    plt.savefig(basename+'-signature.png')
    if len(sys.argv) > 2:
        shutil.move(basename+'-signature.png',sys.argv[2])
