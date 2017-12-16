"""
@Author: Xiaochen (leavebody) Li 
"""
import cv2
import numpy as np
from VideoLoader import VideoLoader


class KillFeed:
    def __init__(self, frame):
        # TODO: crop it on portion in future
        cropped = self._crop_by_limit(frame, 200, 200, 900, 230)
        # gray scale
        gray_cropped = self._to_gray(cropped)
        # contrast
        self.image = cv2.equalizeHist(gray_cropped)

    @staticmethod
    def _to_gray(img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def _crop_by_limit(img, y, h, x, w):
        return img[y: y + h, x: x + w]


if __name__ == '__main__':
    path = '../../videos/1.mp4'
    video = VideoLoader(path)
    killFeed = KillFeed(video.get_frame(16000))

    cv2.imshow("cropped", killFeed.image)
    cv2.waitKey(0)
