"""
@Author: Xiaochen (leavebody) Li
"""

import numpy as np
import cv2
import time


class VideoLoader:
    def __init__(self):
        pass

    """
    return a iterator that iterates over all frames of the video 
    """
    @staticmethod
    def load_from_file(path):
        cap = cv2.VideoCapture(path)
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            yield frame
        cap.release()


if __name__ == '__main__':
    start_time = time.time()
    path = '../../videos/1.mp4'
    count = 0
    for frame in VideoLoader.load_from_file(path):
        count += 1
        if count==1:
            print "---------  frame is a %s  ----------"%type(frame)
        # uncomment these lines to view video:
        # cv2.imshow('frame',frame)
        # # press q to exit
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    print "---------  frame count: %s  ----------"%count
    print "---------  %s seconds  ----------"%(time.time() - start_time)
