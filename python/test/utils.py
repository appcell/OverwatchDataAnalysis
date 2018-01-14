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

    def get_frame_image(self, frame_index):
        """
        Get a specific frame from video.
        @param frame_index: an integer indicating the frame index of the desired frame
        @return: a numpy.ndarray object of this frame image
        """
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        ret, frame = self.cap.read()
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

class Image:
    def crop(self, img, pos_arr):
        return img[pos_arr[0]:pos_arr[0]+pos_arr[1], pos_arr[2]:pos_arr[2]+pos_arr[3]]

    def rgb_to_gray(self, img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def read(self, path):
        return cv2.imread(path)

    def read_with_transparency(self, path):
        return cv2.imread(path, -1)

    def resize(self, img, scale_x, scale_y):
        return cv2.resize(img, (scale_x, scale_y))

    def create_bg_image(self, color, width, height):
        """
        create an image with one single color, given dimensions
        @param color: b, g, r
        @return: background image
        """
        bg_image = np.zeros((height, width, 3))
        bg_image[:, :, 0], bg_image[:, :, 1], bg_image[:, :, 2] = color
        return bg_image

    def overlay(self, bg, fg):
        b, g, r, a = cv2.split(fg)
        overlay_color = cv2.merge((b,g,r))
        height, width, _ = overlay_color.shape
        alpha = np.zeros((height, width, 3))
        alpha[:, :, 0] = alpha[:, :, 1] = alpha[:, :, 2] = a[:, :]
        res = (np.multiply(bg, (1 - alpha / 255)) + np.multiply(overlay_color, (alpha / 255))).astype('uint8')
        # print res
        return res





ImageUtils = Image() 