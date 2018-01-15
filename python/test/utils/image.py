import cv2
import numpy as np

def crop(img, pos_arr):
    """
    Crop given image with specified coordinates.
    @Author: Leavebody, Appcell
    @param img: image to be cropped
    @param pos_arr: coordinates for cropping, in the form of [y_min, h, x_min, w]
    @return: a numpy.ndarray object of this frame image
    """
    return img[pos_arr[0]:pos_arr[0]+pos_arr[1], pos_arr[2]:pos_arr[2]+pos_arr[3]]

def rgb_to_gray(img):
    """
    Transfer given RGB image to grayscale.
    @Author: Leavebody
    @param img: image to be transferred to grayscale
    @return: a numpy.ndarray object of this image
    """
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

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