"""
@Author: Xiaochen (leavebody) Li 
"""
import cv2
import numpy as np
from math import sqrt


class VideoLoader:
    def __init__(self, path):
        self.cap = cv2.VideoCapture(path)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)  # frame per second

    def get_frame_iterator(self):
        """
        @return: a iterator that iterates over all frames of the video
        """
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
            yield frame

    def get_frame(self, frame_index):
        """
        Get a specific frame from video.
        @param frame_index: an integer indicating the frame index of the desired frame
        @return: a numpy.ndarray object of this frame image
        """
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        ret, frame = self.cap.read()
        print ret
        if ret:
            return frame
        else:
            return None

    def close(self):
        """
        Must call this after used this video to release the resource.
        @return:
        """
        self.cap.release()


def read_img(path):
    return cv2.imread(path)


def to_gray(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def crop_by_limit(img, y, h, x, w):
    return img[y: y + h, x: x + w]


def read_unchanged_img(img):
    """
    :param img: img path
    :return: (img, alpha)
    """
    img = cv2.imread(img, cv2.IMREAD_UNCHANGED)
    b, g, r, alpha = cv2.split(img)
    return cv2.merge((b, g, r)), alpha


def mean_rgb(img):
    """
    tmp = np.array([1, 2, 3])
    mean_rgb == np.mean(tmp)
    :param img: image
    :return: array
    """
    height, width, _ = img.shape
    result = np.zeros((height, width))
    for i in range(height):
        for j in range(width):
            result[i, j] = np.mean(img[i, j])
    return result


def color_distance(c1, c2):
    """
    Return the distance between two colors.
    Color should be in bgr format and value of each item is in [0, 255].
    See https://www.compuphase.com/cmetric.htm for the algorithm.
    @param c1: Color 1. [b1, g1, r1]
    @param c2: Color 1. [b1, g1, r1]
    @return: The color distance between them. 0 for same colors.
    """
    c1 = [int(n) for n in c1]
    c2 = [int(n) for n in c2]
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


def singleton(theClass):
    """ decorator for a class to make a singleton out of it """
    classInstances = {}

    def getInstance(*args, **kwargs):
        """ creating or just return the one and only class instance.
            The singleton depends on the parameters used in __init__ """
        key = (theClass, args, str(kwargs))
        if key not in classInstances:
            classInstances[key] = theClass(*args, **kwargs)
        return classInstances[key]

    return getInstance
