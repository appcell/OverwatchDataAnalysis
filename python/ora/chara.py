"""
@Author: Xiaochen (leavebody) Li 
"""
import util
import cv2
import numpy as np
import overwatch

class CharacterAnalyzer:
    """

    """
    def __init__(self, index, chara_image, frame_analyzer, gamedata, time):
        #: The index of this player in game. An integer in 1-6 for away team and 7-12 for home team.
        self.index = index
        self.image = chara_image
        self.frame_analyzer = frame_analyzer
        self.gamedata = gamedata
        self.time = time

        self.fstruc = frame_analyzer.fstruc

        self.chara = overwatch.Chara()

    def analyze(self):
        self.chara.ultimate_status = self._get_ultimate_status()

    def _get_ultimate_status(self):
        """
        Get the ultimate status in this character zone.
        @return: A boolean for whether this character has ult.
        """

        ult_image = util.crop_by_limit(self.image, 0, 0, 0, 0) # todo crop to get the ulti zone
        ult_analyzer = UltimateSkillAnalyzer(ult_image, self.time)
        ult_analyzer.analyze()

        return ult_analyzer.has_ultimate


class UltimateSkillAnalyzer:
    def __init__(self, ult_image, time):
        self.ultimate_icons = overwatch.UltimateSkillIcons(720)
        self.time = time
        self.has_ultimate = None

    def analyze(self):
        # todo modify the things below to get the ultimate status
        pass

    def ultimate_match(self):
        m = self._player_status_image()
        result = self._get_player_ultimate_skill(m, 'LEFT') + self._get_player_ultimate_skill(m, 'RIGHT')
        return result

    def _get_player_ultimate_skill(self, skill_image, flag):
        assert flag in ['LEFT', 'RIGHT']
        result = []
        r = self.fstruc.ULTIMATE_TOP_X_LEFT if flag == 'LEFT' else self.fstruc.ULTIMATE_TOP_X_RIGHT
        for i in range(6):
            img = util.crop_by_limit(
                skill_image,
                self.fstruc.ULTIMATE_TOP_Y,
                self.fstruc.ULTIMATE_HEIGHT,
                i * self.fstruc.ULTIMATE_ITEM_X + r,
                self.fstruc.ULTIMATE_WIDTH,
                )
            icons = self.ultimate_icons.ICONS.get(flag)
            result.append(self._match_ultimate_skill(icons, img))
        return result

    @staticmethod
    def _match_ultimate_skill(template, ultimate_image):
        max_flash = 230
        max_weight = 0.5

        template, ultimate_image = util.to_gray(template),\
                                   util.to_gray(ultimate_image)
        weight = cv2.matchTemplate(ultimate_image, template, cv2.TM_CCOEFF_NORMED).max()

        # to avoid possible explosion effect
        flash = np.mean(ultimate_image)
        if flash > max_flash:
            weight = 1

        if weight > max_weight:
            return True
        return False
