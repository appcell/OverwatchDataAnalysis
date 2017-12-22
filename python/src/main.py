"""
@Author: Xiaochen (leavebody) Li
Adapted from Matlab code.
"""
from video import VideoLoader
import cv2
import image
import overwatch
import time


def analyze_video(video_loader):
    """
    Analyze the killfeed of an video.
    @param video_loader: a video.VideoLoader object
    @return:
    """
    step = video_loader.fps/2.0
    killfeed_list = []
    index = 0
    frame = video.get_frame(index)
    while frame:
        analyzer = FrameAnalyzer(frame)
        new_killfeeds = analyzer.get_killfeed(killfeed_list[-1] if len(killfeed_list) > 0 else None)


class FrameAnalyzer:
    def __init__(self, frame):
        """
        @param frame: frame: a numpy.ndarray image representing this frame
        """
        #: the frame to analyze
        self.frame = cv2.resize(frame, (1280, 720))  # resize the image to 720p

    def get_killfeed(self, killfeed_last=None):
        """
        Get the list of new killfeeds in this frame.
        Scan the killfeeds from top down, and stop if the scanned killfeed collides with
        the last killfeed from the existing killfeed list.

        @param killfeed_last: the last killfeed in the existing killfeed list
        @return: a list of new killfeeds in this frame
        """
        for i in range(5):
            self._get_icons_in_row(i)
        return []

    def _get_icons_in_row(self, row_number):
        # TODO fine-grain these parameters
        # TODO save these parameters as static value
        icon_right = image.crop_by_limit(self.frame, 116 + row_number*35, 23, 1130, 140)
        icon_left = image.crop_by_limit(self.frame, 116 + row_number*35, 23, 963, 205)
        #cv2.imshow("left"+str(row_number), icon_left)
        #cv2.imshow("right"+str(row_number), icon_right)
        name = "left"+str(row_number)
        character_right = self._match_character(icon_left, name)

    def _match_character(self, cropped,name=None):
        cropped_height = cropped.shape[0]
        cropped_width = cropped.shape[1]

        for (object_name, object_icon) in overwatch.ICON_KILLFEED_DICT_720P.iteritems():
            cropped_gray = image.to_gray(cropped)
            template_gray = image.to_gray(object_icon)
            match_result = cv2.matchTemplate(cropped_gray, template_gray, cv2.TM_CCOEFF_NORMED)
            if object_name == overwatch.MERCY:
                print name, max(max(match_result))
                #cv2.imshow("mc_"+name, match_result)


if __name__ == '__main__':
    path = '../../videos/2.mp4'
    video = VideoLoader(path)
    analyze_video(video)
    video.close()
