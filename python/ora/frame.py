"""
@Author: Xiaochen (leavebody) Li 
"""
import cv2
import overwatch
from killfeed import KillfeedAnalyzer
from chara import CharacterAnalyzer
import util


class FrameAnalyzer:
    """
    The analyzer for a frame in a game.
    Analyses in 1280x720 resolution.
    """
    def __init__(self, frame, frame_time, game):
        """
        @param frame: a numpy.ndarray image representing this frame
        """
        #: the frame image to analyze
        self.image = cv2.resize(frame, (1280, 720))  # Resize the image to 720p.
        self.time = frame_time
        self.killfeed_icons = overwatch.KillfeedIcons(720)
        self.fstruc = overwatch.OWLFrameStructure(720)  # Using OWL frame structure now.
        #: The OverwatchGame object for this frame.
        self.game = game

        self.frame = None

    def analyze(self):
        """
        Retrieve information from this frame.
        @return: None
        """
        self.frame = overwatch.Frame()
        self.frame.is_valid = self.validate_frame()
        if not self.frame.is_valid:
            return
        # killfeed
        killfeed_last = self.game.get_last_killfeed()
        self.frame.killfeeds = self.get_killfeed(killfeed_last)

    def validate_frame(self):
        # todo: check whether this frame is valid
        return True

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
            killfeed_image = self.get_killfeed_row_image(i)
            killfeed_analyzer = KillfeedAnalyzer(killfeed_image, self)
            killfeed_in_row = killfeed_analyzer.get_killfeed("row: "+str(i))
            if killfeed_in_row is None or killfeed_in_row == killfeed_last:
                break
            result.append(killfeed_in_row)
        result.reverse()  # Reverse the list to make it from bottom to top.
        return result

    def get_killfeed_row_image(self, row_number):
        """
        Get the cropped image of a killfeed by its row number.
        @param row_number: An integer in range(6).
        @return: The cropped killfeed image.
        """
        return util.crop_by_limit(self.image,
                                  self.fstruc.KILLFEED_TOP_Y + row_number * self.fstruc.KILLFEED_ITEM_HEIGHT,
                                  self.killfeed_icons.ICON_CHARACTER_HEIGHT,
                                  self.fstruc.KILLFEED_RIGHT_X - self.fstruc.KILLFEED_MAX_WIDTH,
                                  self.fstruc.KILLFEED_MAX_WIDTH)

    def get_charas(self):
        """
        Get the info from top player bar.
        @return: A dictionary where the key is the index of the player (integer from 1 to 12)
                    and value is the corresponding overwatch.Chara instance.
        """
        charas = {}
        for i in range(1,13):
            chara_image = self.get_chara_zone_image(i)
            chara_analyzer = CharacterAnalyzer(i, chara_image, self, self.game)
            chara_analyzer.analyze()
            charas[i] = chara_analyzer.chara
        return charas


    def get_chara_zone_image(self, index):
        """
        Get the cropped image of a player's zone in the top bar.
        @param index: The index of the player. Should be an integer in 1-12.
        @return: The cropped image.
        """
        if index < 6.5:
            left_x_index = int(round(self.fstruc.PLAYER_ZONE_TEAM1_LEFT_X +
                                     (index-1)*self.fstruc.PLAYER_ZONE_HORIZONTAL_STEP))
        else:
            left_x_index = int(round(self.fstruc.PLAYER_ZONE_TEAM2_LEFT_X +
                                     (index-7)*self.fstruc.PLAYER_ZONE_HORIZONTAL_STEP))
        return util.crop_by_limit(self.image,
                                  self.fstruc.PLAYER_ZONE_TOP_Y,
                                  self.fstruc.PLAYER_ZONE_HEIGHT,
                                  left_x_index,
                                  self.fstruc.PLAYER_ZONE_WIDTH)

    def set_team_color(self):
        self.game.color_team1 = self.image[1][1][:]
        self.game.color_team2 = self.image[1][1278][:]
