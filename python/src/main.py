"""
@Author: Xiaochen (leavebody) Li
Partially adapted from Matlab code.
"""
import video
import cv2
import image
import overwatch
import time
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
        for k in new_killfeeds:
            print index/video_loader.fps, k
        index += step
        frame = video_loader.get_frame(index)
    video_loader.close()


class FrameAnalyzer:
    """
    The analyzer for a frame in a game.
    Analyses in 1280x720 resolution.
    """
    def __init__(self, frame, frame_time):
        """
        @param frame: frame: a numpy.ndarray image representing this frame
        """
        #: the frame to analyze
        self.frame = cv2.resize(frame, (1280, 720))  # Resize the image to 720p.
        self.time = frame_time
        self.icons = overwatch.KillfeedIcons(720)
        self.fstruc = overwatch.OWLFrameStructure(720)  # Using OWL frame structure now.

    def get_killfeed(self, killfeed_last=None):
        """
        Get the list of new killfeeds in this frame.
        Scan the killfeeds from top down, and stop if the scanned killfeed collides with
        the last killfeed from the existing killfeed list.

        @param killfeed_last: the last killfeed in the existing killfeed list
        @return: a list of new killfeeds in this frame
        """
        result = []
        for i in range(overwatch.KILLFEED_ITEM_MAX_COUNT_IN_SCREEN):
            killfeed_in_row = self._get_killfeed_in_row(i)
            if killfeed_in_row is None or killfeed_in_row == killfeed_last:
                break
            result.append(killfeed_in_row)
        result.reverse()  # Reverse the list to make it from bottom to top.
        return result

    def _get_killfeed_in_row(self, row_number):
        # Crop the image and get the desired row.
        killfeed_image = image.crop_by_limit(self.frame,
                                             self.fstruc.KILLFEED_TOP_Y + row_number*self.fstruc.KILLFEED_ITEM_HEIGHT,
                                             self.icons.ICON_CHARACTER_HEIGHT,
                                             self.fstruc.KILLFEED_RIGHT_X - self.fstruc.KILLFEED_MAX_WIDTH,
                                             self.fstruc.KILLFEED_MAX_WIDTH)
        # cv2.imshow("row"+str(row_number), killfeed_image)
        name = "killfeed_image"+str(row_number)
        icons_weights = self._get_icons_weights(killfeed_image, name)
        # TODO Only needs two best matches in the end. Keep three while debugging.
        best_matches = [self.KillfeedIconMatch("", -1, -1)] * 3
        for item in icons_weights:
            if item.score > best_matches[0].score:
                best_matches.insert(0, item)
                best_matches.pop()
            elif item.score > best_matches[1].score:
                best_matches.insert(1, item)
                best_matches.pop()
            elif item.score > best_matches[2].score:
                best_matches.pop()
                best_matches.append(item)

        # Edge detection around the found icons.
        edge_image = cv2.Canny(killfeed_image, 100, 200)  # Generate the edges in this killfeed image.
        # cv2.imshow(str(row_number), edge_image)
        edge_span = np.zeros(edge_image.shape)
        for i in range(edge_image.shape[0]):
            for j in range(1, edge_image.shape[1]):
                edge_span[i, j] = sum(edge_image[i, j-1: j+1])  # Get the "spanned" edge image.
        edge_sum = edge_span.sum(0)  # Sum the result on y axis.
        edge_sum = edge_sum/(255 * self.icons.ICON_CHARACTER_HEIGHT)  # Normalize the result.
        # todo Detect right edge too.
        matched_icons = []
        for item in best_matches:
            if item.score < 0.6:  # todo save 0.6 as a constant
                continue
            edge_scores = edge_sum[item.x-2: item.x+2]
            threshold = (self.icons.ICON_CHARACTER_HEIGHT - 1.0) / self.icons.ICON_CHARACTER_HEIGHT
            if max(edge_scores if len(edge_scores) > 0 else [0]) >= threshold:
                # The metric is that there should be a vertical edge
                # between left 3 pixels to the icon position
                # and right 1 pixel to the icon position
                # with no more than 1 pixels in the vertical line missing.
                # A vertical line should have a width of no more than 2.
                matched_icons.append(item)

        # print "row", row_number, best_matches, [max(edge_sum[best_matches[i][2]-2: best_matches[i][2]+2]) for i in range(3)]
        if len(matched_icons) == 0:
            return
        elif len(matched_icons) == 1:
            if matched_icons[0].x < self.fstruc.KILLFEED_MAX_WIDTH - self.fstruc.KILLFEED_CHARACTER2_MAX_WIDTH:
                # If the only icon found is not in the right place, this might be a killfeed that only shows half.
                # Leave it alone for this frame, and deal with it in later frames.
                return
            return self._generate_suicide_killfeed(matched_icons)
        else:
            return self._generate_non_suicide_killfeed(matched_icons[:2])

    def _get_icons_weights(self, killfeed_image, name=""):
        result = []
        for (object_name, object_icon) in self.icons.ICONS_CHARACTER.iteritems():
            # Match in gray scale
            # killfeed_gray = image.to_gray(killfeed_image)
            # template_gray = image.to_gray(object_icon)
            # match_result = cv2.matchTemplate(killfeed_gray, template_gray, cv2.TM_CCOEFF_NORMED)

            # Match in original color, which seems not really hurting the performance.
            match_result = cv2.matchTemplate(killfeed_image, object_icon, cv2.TM_CCOEFF_NORMED)

            # Find two most possible location of this character's icon in the killfeed image.
            # Mask the pixels around the first location to find the second one.
            _, max_val, _, max_loc = cv2.minMaxLoc(match_result)
            result.append(self.KillfeedIconMatch(object_name, max_val, max_loc[0]))
            half_mask_width = 5
            mask_index_left = max((max_loc[0] - half_mask_width, 0))
            mask_index_right = min((max_loc[0] + half_mask_width + 1,
                                    self.fstruc.KILLFEED_MAX_WIDTH - self.icons.ICON_CHARACTER_WIDTH))
            match_result[0, mask_index_left: mask_index_right] = [-1] * (mask_index_right - mask_index_left)

            _, max_val, _, max_loc = cv2.minMaxLoc(match_result)
            result.append(self.KillfeedIconMatch(object_name, max_val, max_loc[0]))
        return result

    class KillfeedIconMatch:
        """
        A helper class to store the intermediate result of a recognized icon in the killfeed.
        """
        def __init__(self, object_name, score, x):
            #: The name of the recognized object.
            self.object_name = object_name
            #: The score of this match.
            self.score = score
            #: The x coordinate of the recognized object in the killfeed image.
            self.x = x

    def _generate_suicide_killfeed(self, matched_icons):
        return overwatch.KillFeed("test", self.time, character2=matched_icons[0][0], event="suicide")

    def _generate_non_suicide_killfeed(self, best_matches):
        if best_matches[0].x > best_matches[1].x:
            best_matches = [best_matches[1], best_matches[0]]
        return overwatch.KillFeed("test", self.time, character1=best_matches[0].object_name, character2=best_matches[1].object_name)


if __name__ == '__main__':
    path = '../../videos/SDvsNYXL_Preseason.mp4'
    video = video.VideoLoader(path)
    t = time.time()
    analyze_video(video)
    print "time:", time.time()-t
    video.close()

