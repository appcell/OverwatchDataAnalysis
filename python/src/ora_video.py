"""
@Author: Xiaochen (leavebody) Li
"""

import numpy as np
import cv2
import time


class VideoLoader:
    def __init__(self, path):
        self.cap = cv2.VideoCapture(path)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)  # frame per second

    """
    Return a iterator that iterates over all frames of the video.
    """
    def get_frame_iterator(self):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES , 0)
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
            yield frame

    """
    Get a specific frame from video.
    """
    def get_frame(self, frame_index):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES , frame_index)
        ret, frame = self.cap.read()
        if ret:
            return frame
        else:
            return None

    """
    Must call this after used this video to release the resource.
    """
    def close(self):
        self.cap.release()


if __name__ == '__main__':
    start_time = time.time()
    path = '../../videos/1.mp4'
    video = VideoLoader(path)

    count = 0
    for frame in video.get_frame_iterator():
        count += 1
        # uncomment these lines to view video:
        # cv2.imshow('frame',frame)
        # # press q to exit
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
    print "---------  frame count: %s  ----------" % count
    print "---------  %s seconds  ----------" % (time.time() - start_time)

    print "---------  frame per second is: %s  ----------" % video.fps
    print "---------  frame is a %s  ----------" % type(video.get_frame(0))

    video.close()
