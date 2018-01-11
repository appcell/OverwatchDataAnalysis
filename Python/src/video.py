"""
@Author: Xiaochen (leavebody) Li
"""

import numpy as np
import cv2


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
