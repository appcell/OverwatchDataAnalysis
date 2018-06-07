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
        self.frame_number = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.count = 0

    def get_frame_image(self, frame_index):
        """
        Get a specific frame from video.
        @param frame_index: an integer indicating the frame index of the desired frame
        @return: a numpy.ndarray object of this frame image
        """
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        ret, frame = self.cap.read()
        if ret:
            # cv2.imwrite("frame%d.jpg" % self.count, frame)
            self.count +=1
            return frame
        else:
            return None

    def save_image(self, frame):
        """
        Save an image for debug purpose.
        @param frame: a numpy.ndarray object of this frame image
        """
        cv2.imwrite("frame%d.jpg" % self.count, frame)
        self.count +=1

    def close(self):
        """
        Must call this after using this video to release the resource.
        @return:
        """
        self.cap.release()