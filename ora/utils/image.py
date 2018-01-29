import cv2
import numpy as np
from skimage import transform as tf
from skimage.exposure import adjust_log
from skimage.filters import threshold_otsu

REMOVE_NUMBER_VERTICAL_EDGE_LEFT = 0
REMOVE_NUMBER_VERTICAL_EDGE_RIGHT = 0
REMOVE_NUMBER_VERTICAL_EDGE_BOTH = 0

def crop(img, pos_arr):
    """
    Crop given image with specified coordinates.
    @Author: Leavebody, Appcell
    @param img: image to be cropped
    @param pos_arr: coordinates for cropping, in the form of [y_min, h, x_min, w]
    @return: a numpy.ndarray object of this frame image
    """
    return img[pos_arr[0]:pos_arr[0]+pos_arr[1], pos_arr[2]:pos_arr[2]+pos_arr[3]]


def shear(img, shear_rad):
    """
    Shear a image to a given radian.
    @Author: Rigel
    @param img: image to be sheared
    @param shear_rad: radian to which the image will be sheared
    @return: a numpy.ndarray object of this image
    """
    affine_tf = tf.AffineTransform(shear=shear_rad)
    return tf.warp(img, inverse_map=affine_tf)

def normalize_gray(img):
    """
    Normalize a grayscale img
    @Author: Appcell
    @param img: image to be normalized
    @return: a numpy.ndarray object of this image
    """
    std = np.std(img)
    mean = np.mean(img)
    w = img.shape[1]
    h = img.shape[0]
    res = np.zeros((h, w))

    for i in range(h):
        for j in range(w):
            res[i, j] = ((img[i, j] - mean) / std)
    min_img = np.min(res)
    max_img = np.max(res)
    for i in range(h):
        for j in range(w):
            res[i, j] = (res[i, j] - min_img) / (max_img - min_img)

    return res

def rgb_to_gray(img):
    """
    Transfer given RGB image to grayscale.
    @Author: Leavebody
    @param img: image to be transferred to grayscale
    @return: a numpy.ndarray object of this image
    """
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def inverse_gray(img):
    w = img.shape[1]
    h = img.shape[0]
    res = np.ones((h, w)) - img
    return res

def rgb_to_bw(img, threshold):
    w = img.shape[1]
    h = img.shape[0]
    res = np.zeros((h, w))

    for i in range(h):
        for j in range(w):
            if color_distance(img[i, j], np.array([255, 255, 255])) < 40:
                res[i, j] = 255
    return res

def remove_digit_vertical_edge(img, deviation_limit, side):
    width = img.shape[1]
    height = img.shape[0]
    edge_left = 0
    edge_right = width - 1

    res = []
    # sometimes there's noise at bottom, thus we remove 5px first
    img2 = crop(img, [0, height - 5, 0, width])
    deviation = img2.max(axis=0) - img2.min(axis=0)

    # Here we have to start searching from right, since there might be
    # noise on left.
    for i in range(width - 4, 1, -1):
        if deviation[i + 3] - deviation[i] > deviation_limit:
            edge_left = i
            break
    for i in range(width - 4, 1, -1):
        if deviation[i] - deviation[i+3] > deviation_limit:
            edge_right = i
            break

    if side == REMOVE_NUMBER_VERTICAL_EDGE_BOTH:
        res = crop(img, [0, height, edge_left, edge_right - edge_left + 1])
    elif side == REMOVE_NUMBER_VERTICAL_EDGE_LEFT:
        res = crop(img, [0, height, edge_left, width - edge_left])
    else:
        res = crop(img, [0, height, 0, edge_right])

    return res

def increase_contrast(img):
    """
    Increase contrast of an RGB image
    @Author: Appcell
    @param img: image to be processed
    @return: a numpy.ndarray object of this image
    """
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(4, 4))
    cl = clahe.apply(l)
    limg = cv2.merge((cl,a,b))
    final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    return final

def similarity(img, img2):
    """
    Similarity between 2 BW images with same size.
    """
    bwimg = img
    bwimg2 = img2
    if len(img.shape) > 2 and img.shape[2] == 3:
        bwimg = rgb_to_bw(img, 40)
    if len(img2.shape) > 2 and img2.shape[2] == 3:
        bwimg2 = rgb_to_bw(img2, 40)
    w = bwimg.shape[1]
    h = bwimg.shape[0]
    s = 0
    for i in range(h):
        for j in range(w):
            if bwimg[i, j] == bwimg2[i, j]:
                s += 1

    return float(s)/(w*h)

def read(path):
    """
    Read RGB channels of an image with given path from file system.
    @Author: Leavebody
    @param path: path of image file
    @return: a numpy.ndarray object of read image, with only RGB channels.
    """
    return cv2.imread(path)


def read_with_transparency(path):
    """
    Read RGBA channels of an image with given path from file system, 
    @Author: Leavebody
    @param path: path of image file
    @return: a numpy.ndarray object of read image, with RGB + Alpha channels.
    """
    return cv2.imread(path, -1)


def read_bw(path):
    """
    Read a B/W image with given path from file system.
    @Author: Rigel
    @param path: path of image file
    @return: a numpy.ndarray object of read image, with boolean type pixels
    """
    img_gray = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    return img_gray > 127


def resize(img, dest_width, dest_height):
    """
    Resize an image with given destination dimensions.
    @Author: Appcell
    @param img: the image to be resized
    @dest_width: width of image after resizing
    @dest_height: height of image after resizing
    @return: a numpy.ndarray object of resized image.
    """
    return cv2.resize(img, (dest_width, dest_height))


def contrast_adjust_log(img, gain):
    """
    Perform logarithm correction to increase contrast
    @Author: Rigel
    @param img: the image to be corrected
    @gain: constant multiplier
    @return: a numpy.ndarray object of corrected image.
    """
    return adjust_log(img, gain)


def binary_otsu(img):
    """
    Perform binarization with otsu algorithm
    @Author: Rigel
    @param img: the image to be corrected
    @gain: constant multiplier
    @return: a numpy.ndarray boolean object of binary image.
    """
    global_thresh = threshold_otsu(img)
    return img > global_thresh


def create_bg_image(color, width, height):
    """
    Generate an image with one single color, given dimensions
    @Author: Appcell
    @param color: b, g, r
    @param width: width of generated image
    @param height: height of generated image
    @return: the image generated
    """
    bg_image = np.zeros((height, width, 3))
    bg_image[:, :, 0], bg_image[:, :, 1], bg_image[:, :, 2] = color
    return bg_image


def overlay(bg, fg):
    """
    Overlay a TRANSPARENT image (foreground) onto background.
    Both images have to have same width & height.
    @Author: Appcell
    @param bg: background image, WITHOUT transparency
    @param fg: foreground image, WITH transparency
    @return: overlay result
    """
    b, g, r, a = cv2.split(fg)
    overlay_color = cv2.merge((b,g,r))
    height, width, _ = overlay_color.shape
    alpha = np.zeros((height, width, 3))
    alpha[:, :, 0] = alpha[:, :, 1] = alpha[:, :, 2] = a[:, :]
    res = (np.multiply(bg, (1 - alpha / 255)) + np.multiply(overlay_color, (alpha / 255))).astype('uint8')
    return res


def color_distance_normalized(color1, color2):
    color_temp = np.abs(color1 - (color2 + np.mean(color1) - np.mean(color2)));
    return np.max(color_temp)


def color_distance(color1, color2):
    return np.linalg.norm(color1.astype('double') - color2.astype('double'))