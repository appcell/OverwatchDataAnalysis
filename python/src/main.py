"""
@Author: Xiaochen (leavebody) Li
Partially adapted from Matlab code.
"""
import video
import cv2
import image
import overwatch
import time
from matplotlib import pyplot as plt
import numpy as np


def analyze_video(video_loader):
    """
    Analyze the killfeed of an video.
    @param video_loader: a video.VideoLoader object
    @return:
    """
    step = int(round(video_loader.fps/2))
    killfeed_list = []
    index = 0
    frame = video_loader.get_frame(index)
    while frame is not None:
        analyzer = FrameAnalyzer(frame, index)
        new_killfeeds = analyzer.get_killfeed(killfeed_list[-1] if len(killfeed_list) > 0 else None)
        killfeed_list.extend(new_killfeeds)
        index += step
        frame = video_loader.get_frame(index)
        for k in new_killfeeds:
            print index/video_loader.fps, k
    # for k in killfeed_list:
    #     print k



class FrameAnalyzer:
    def __init__(self, frame, frame_time):
        """
        @param frame: frame: a numpy.ndarray image representing this frame
        """
        #: the frame to analyze
        self.frame = cv2.resize(frame, (1280, 720))  # resize the image to 720p
        self.time = frame_time

    def get_killfeed(self, killfeed_last=None):
        """
        Get the list of new killfeeds in this frame.
        Scan the killfeeds from top down, and stop if the scanned killfeed collides with
        the last killfeed from the existing killfeed list.

        @param killfeed_last: the last killfeed in the existing killfeed list
        @return: a list of new killfeeds in this frame
        """
        result = []
        for i in range(5):
            killfeed_in_row = self._get_killfeed_in_row(i)
            if killfeed_in_row is not None:
                if killfeed_in_row == killfeed_last:
                    break
                result.append(killfeed_in_row)
        return result

    def _get_killfeed_in_row(self, row_number):
        # Crop the image and get the desired row.
        # TODO save these parameters as static value
        killfeed_image = image.crop_by_limit(self.frame, 116 + row_number*35, 23, 963, 1270-963)
        cv2.imshow("row"+str(row_number), killfeed_image)
        name = "killfeed_image"+str(row_number)
        icons_weights = self._get_icons_weights(killfeed_image, name)
        # TODO Only needs two best matches in the end. Keep three while debugging.
        best_matches = [["", -1, -1], ["", -1, -1], ["", -1, -1]]
        for item in icons_weights:
            if item[1] > best_matches[0][1]:
                best_matches.insert(0, item)
                best_matches.pop()
            elif item[1] > best_matches[1][1]:
                best_matches.insert(1, item)
                best_matches.pop()
            elif item[1] > best_matches[2][1]:
                best_matches.pop()
                best_matches.append(item)

        # Edge detection around the found icons.
        edge_image = cv2.Canny(killfeed_image,100,200)  # Generate the edges in this killfeed image.
        edge_span = np.zeros(edge_image.shape)
        for i in range(edge_image.shape[0]):
            for j in range(3, edge_image.shape[1] - 1):
                edge_span[i, j] = sum(edge_image[i, j-3: j+1])  # Get the "spanned" edge image.
        edge_sum = edge_span.sum(0)  # Sum the result on y axis.
        edge_sum = edge_sum/(255*overwatch.ICON_KILLFEED_720P_HEIGHT)  # Normalize the result.

        matched_icons = []
        for item in best_matches:
            if edge_sum[item[2]] >= (overwatch.ICON_KILLFEED_720P_HEIGHT - 2.0)/overwatch.ICON_KILLFEED_720P_HEIGHT:
                # The metric is that there should be a vertical edge
                # between left 3 pixels to the icon position
                # and right 1 pixel to the icon position
                # with no more than 2 pixels in the vertical line missing.
                matched_icons.append(item)

        # print "row",row_number, best_matches, [edge_sum[best_matches[i][2]] for i in range(3)]
        if len(matched_icons) == 0:
            return
        elif len(matched_icons) == 1:
            return self._generate_suicide_killfeed(matched_icons)
        else:
            return self._generate_non_suicide_killfeed(matched_icons[:2])

    def _get_icons_weights(self, killfeed_image, name=""):
        result = []
        for (object_name, object_icon) in overwatch.ICON_KILLFEED_DICT_720P.iteritems():
            # Match in gray scale
            # killfeed_gray = image.to_gray(killfeed_image)
            # template_gray = image.to_gray(object_icon)
            # match_result = cv2.matchTemplate(killfeed_gray, template_gray, cv2.TM_CCOEFF_NORMED)
            # Match in original color, which seems not really hurting the performance.
            match_result = cv2.matchTemplate(killfeed_image, object_icon, cv2.TM_CCOEFF_NORMED)

            # Find two most possible location of this character's icon in the killfeed image.
            # Mask the pixels around the first location to find the second one.
            _, max_val, _, max_loc = cv2.minMaxLoc(match_result)
            result.append([object_name, max_val, max_loc[0]])
            half_mask_width = 5
            mask_index_left =  max((max_loc[0] - half_mask_width, 0))
            mask_index_right = min((max_loc[0] + half_mask_width + 1, 1270-963-34))  # TODO link this to killfeed constant of this resolution
            try:
                match_result[0, mask_index_left: mask_index_right] = [-1] * (mask_index_right - mask_index_left)
            except:
                print mask_index_left, mask_index_right
                exit(0)
            _, max_val, _, max_loc = cv2.minMaxLoc(match_result)
            result.append([object_name, max_val, max_loc[0]])
            # if object_name == overwatch.DVA:
            #     print name, max(match_result[0])
            #     cv2.imshow("mc_"+name, match_result)
        return result

    def _generate_suicide_killfeed(self, matched_icons):
        suicider = matched_icons[0]
        return overwatch.KillFeed("test", self.time, character2=suicider[0], event="suicide")

    def _generate_non_suicide_killfeed(self, best_matches):
        try:
            if best_matches[0][2] > best_matches[1][2]:
                best_matches = [best_matches[1], best_matches[0]]
        except:
            print best_matches

        return overwatch.KillFeed("test", self.time, character1=best_matches[0][0], character2=best_matches[1][0])



if __name__ == '__main__':
    path = '../../videos/2.mp4'
    path = '../../videos/SDvsNYXL_Preseason.mp4'
    video = video.VideoLoader(path)
    analyze_video(video)
    video.close()
