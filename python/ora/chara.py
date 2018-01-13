# -*- coding:utf-8 -*-
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
        # self.detector_chara()

    def _get_ultimate_status(self):
        """
        Get the ultimate status in this character zone.
        @return: A boolean for whether this character has ult.
        """

        ult_image = util.crop_by_limit(self.image, 0, 0, 0, 0) # todo crop to get the ulti zone
        ult_analyzer = UltimateSkillAnalyzer(ult_image, self.time)
        ult_analyzer.analyze()

        return ult_analyzer.has_ultimate

    def detector_chara(self):
        return CharaDetector(self.image, self.index, self.gamedata, self.fstruc).analyze()


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


class CharaDetector:
    def __init__(self, chara_image, index, game, fstruc):
        self.chara_image = chara_image
        self.fstruc = fstruc
        self.player = index
        self.icons = overwatch.CharacterIcons().icon_and_alpha_to_resize
        self.game = game

    @staticmethod
    def fused(icon, bg_image, alpha):
        """
        将 icon 和 bgimage 按照 alpha 的比例拼接成一个图片
        :param icon: 图标
        :param bgimage: 背景图
        :param alpha: icon 的 alpha
        :return: 新的图标
        """
        icon = icon.copy()
        height, width, _ = icon.shape
        a = alpha / 255
        b = (255 - alpha) / 255
        for i in range(height):
            for j in range(width):
                icon[i, j] = icon[i, j] * a[i, j] + bg_image[i, j] * b[i, j]
        return icon

    @staticmethod
    def create_bg_image(color):
        """
        创建一个 bgimage ， 并对它的三个通道进行染色
        :param color: b, g, r
        :return: background image
        """
        bg_image = np.zeros((30, 38, 3))
        bg_image[:, :, 0], bg_image[:, :, 1], bg_image[:, :, 2] = color
        return bg_image

    @staticmethod
    def get_img_light(img):
        img = util.mean_rgb(img)
        return img.max() - img.min()

    @staticmethod
    def _match_normed(image, template):
        return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

    def _is_dead(self, chara_icon, bg_image, index):
        """
        判断玩家是否死亡。
        :param chara_icon: 英雄图标
        :param bg_image: 染色后的背景图
        :param index: judge_gray 数组中最大数的下标
        :param chara_icons: [(img, alpha), ...]
        :return: True or False
        """
        height, width, _ = chara_icon.shape
        tmp_img = util.crop_by_limit(chara_icon, 4, height, 0, width)
        current_std = np.std(tmp_img, ddof=1).max()
        if current_std < 100:
            icon, alpha = self.icons[overwatch.CHARACTER_LIST[index]]
            fused_icon = self.fused(icon, bg_image, alpha)
            current, original = self.get_img_light(tmp_img), self.get_img_light(fused_icon)
            if abs(original - current) > 45:
                return True
        return False

    def _match(self, chara_icon, bg_image):
        """
        令 icons 中的 icon 与合成的每个图片进行匹配
        并输出 权重表
        :param chara_icon: 
        :param bg_image: 
        :return: [weight, ...]
        """
        judge_gray = []
        for _, v in self.icons.iteritems():
            icon, alpha = v
            fused_icon = self.fused(icon, bg_image, alpha)
            corr = self._match_normed(chara_icon, fused_icon).max()
            judge_gray.append(corr)
        return judge_gray

    def analyze(self):
        color = self.game.color_team1 if self.player <= 6 else self.game.color_team2
        # bg_image 和 self.fused 其实可以优化一下，没必要每次都生成。一次生成两个队的就可以了
        bg_image = self.create_bg_image(color)
        chara_icon = util.crop_by_limit(self.chara_image,
                                        self.fstruc.CHARA_TOP_Y,
                                        self.fstruc.CHARA_HEIGHT,
                                        self.fstruc.CHARA_TOP_X,
                                        self.fstruc.CHARA_WIDTH)
        judge_gray = self._match(chara_icon, bg_image)
        index = judge_gray.index(max(judge_gray))
        if self._is_dead(chara_icon, bg_image, index):
            return 'dead', judge_gray[index]
        else:
            return overwatch.CHARACTER_LIST[index], judge_gray[index]
