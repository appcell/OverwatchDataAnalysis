"""
@Author: Xiaochen (leavebody) Li 
"""
import cv2
from math import sqrt

def read_img(path):
    return cv2.imread(path)


def to_gray(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def crop_by_limit(img, y, h, x, w):
    return img[y: y + h, x: x + w]


def color_distance(c1, c2):
    """
    Return the distance between two colors.
    Color should be in bgr format and value of each item is in [0, 255].
    See https://www.compuphase.com/cmetric.htm for the algorithm.
    @param c1: Color 1. [b1, g1, r1]
    @param c2: Color 1. [b1, g1, r1]
    @return: The color distance between them. 0 for same colors.
    """
    r = 2
    g = 1
    b = 0
    r_bar = (c1[r]+c2[r])/2.0
    delta_r = c1[r] - c2[r]
    delta_g = c1[g] - c2[g]
    delta_b = c1[b] - c2[b]
    delta_c = sqrt((2+r_bar/256.0)*(delta_r**2) +
                   4*(delta_g**2) +
                   (2+(255-r_bar)/256.0)*delta_b**2)
    return delta_c
