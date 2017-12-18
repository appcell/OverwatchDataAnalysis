"""
@Author: Xiaochen (leavebody) Li 
"""
import cv2
import numpy as np
from ora_video import VideoLoader
import ora_image


class KillFeed:
    def __init__(self, frame):
        # TODO: crop it on portion in future
        # cropped = ora_image.crop_by_limit(frame, 200, 200, 900, 300)
        cropped = ora_image.crop_by_limit(frame, 100, 250, 1000, 300)
        self.image = cropped
        # gray scale
        self.image_gray = ora_image.to_gray(cropped)

        # gray = cv2.GaussianBlur(gray_cropped, (3, 3), 0)
        #
        # edged = cv2.Canny(gray, 10, 250)
        #
        # # construct and apply a closing kernel to 'close' gaps between 'white'
        # # pixels
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        # closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
        # cv2.imshow("Closed", closed)
        # cv2.waitKey(0)


if __name__ == '__main__':
    path = '../../videos/2.mp4'
    video = VideoLoader(path)
    killFeed = KillFeed(video.get_frame(1010))

    cv2.imshow("cropped", killFeed.image)
    cv2.waitKey(0)
