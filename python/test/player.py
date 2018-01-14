import overwatch as OW
import cv2
import numpy as np
from utils import ImageUtils
import skimage
from skimage import measure

class Player:
    def __init__(self, index, frame):
        #: index of player, from 0 to 11
        self.index = index
        #: pointer to frame obj
        self.frame = frame
        #: image of current frame
        self.image = self.frame.image
        #: the player name
        self.name = self.frame.game.name_players_team_left[index] if index < 6 \
                    else self.frame.game.name_players_team_right[index - 6]
        #: team name
        self.team = self.frame.game.name_team_left if index < 6 \
                    else self.frame.game.name_team_right
        #: the character that this player is playing
        self.chara = None
        #: whether this player has ultimate ability now
        self.is_ult_ready = False
        #: whether this chara is dead
        self.is_dead = False
        # TODO: future work
        self.is_observed = None  # is daddy camera watching this guy?
        self.health = None
        self.ult_charge = None
        self.is_onfire = None

        # Analyze process
        self.get_ult_status()
        self.get_chara()

    def get_ult_status(self):
        
        ult_icon_pos = OW.get_ult_icon_pos(self.index)[self.frame.game.game_type]
        ult_icon = ImageUtils.crop(self.image, ult_icon_pos)
        ult_icon_ref = OW.get_ult_icon_ref(self.index)[self.frame.game.game_type]
        max_brightness = 230
        max_prob = 0.5
        ult_icon_ref, ult_icon = ImageUtils.rgb_to_gray(ult_icon_ref), ImageUtils.rgb_to_gray(ult_icon)
        prob = cv2.matchTemplate(ult_icon, ult_icon_ref, cv2.TM_CCOEFF_NORMED).max()

        # to avoid possible explosion effect
        brightness = np.mean(ult_icon)
        prob = 1 if brightness > max_brightness else prob
        if prob > max_prob:
            self.is_ult_ready = True

    def get_chara(self):
        bg_color  = []
        if self.frame.game.color_team_left is not None:
            bg_color = self.frame.game.color_team_left \
                       if self.index < 6 else self.frame.game.color_team_right
        else:
            team_colors = self.frame.get_team_colors()
            bg_color = team_colors["color_team_left"] \
                       if self.index < 6 else team_colors["color_team_right"]

        bg_image = ImageUtils.create_bg_image(bg_color, OW.AVATAR_WIDTH, OW.AVATAR_HEIGHT)
        avatars_ref = OW.get_avatars_ref()
        avatar = ImageUtils.crop(self.image, OW.get_avatar_pos(self.index)[self.frame.game.game_type])

        score = 0

        for (name, avatar_ref) in avatars_ref.iteritems():
            fused_avatar_ref = ImageUtils.overlay(bg_image, avatar_ref)
            fused_avatar_ref_small = ImageUtils.resize(ImageUtils.overlay(bg_image, avatar_ref), 33, 26)

            s = cv2.matchTemplate(fused_avatar_ref, avatar, cv2.TM_CCOEFF_NORMED)[0][0]
            s_small = cv2.matchTemplate(avatar, fused_avatar_ref_small, cv2.TM_CCOEFF_NORMED)[0][0]

            s_final = s if s > s_small else s_small
            if s_final > score:
                score = s_final
                self.chara = name
                self.is_observed = True if s > s_small else False

        self.get_living_status(fused_avatar_ref)

    def get_living_status(self, avatar_ref):        
        avatar = ImageUtils.crop(self.image, OW.get_avatar_pos_small(self.index)[self.frame.game.game_type])
        brightness = np.mean(avatar, 2)
        brightness_ref = np.mean(avatar_ref, 2)
        variation = brightness.max() - brightness.min();
        variation_ref = brightness_ref.max() - brightness_ref.min();

        if abs(variation_ref - variation) > 45:
            self.is_dead = True

    