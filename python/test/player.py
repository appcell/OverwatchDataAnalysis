import overwatch as OW
import cv2
import numpy as np
from utils import image as ImageUtils
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
        self.team = self.frame.game.team_names['left'] if index < 6 \
                    else self.frame.game.team_names['right']
        #: the character current player uses
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
        # Analysis process
        self.get_ult_status()
        self.get_chara()

    def get_ult_status(self):
        """
        Retrieves ultimate statues info for current player in current frame.
        @Author: Appcell
        @return: None
        """
        # Crop icon from current frame
        ult_icon_pos = OW.get_ult_icon_pos(self.index)[self.frame.game.game_type]
        ult_icon = ImageUtils.crop(self.image, ult_icon_pos)
        # Get reference icon image
        ult_icon_ref = OW.get_ult_icon_ref(self.index)[self.frame.game.game_type]
        # Tranfer both to grayscale for comparison
        ult_icon_ref, ult_icon = ImageUtils.rgb_to_gray(ult_icon_ref), ImageUtils.rgb_to_gray(ult_icon)

        # Compare cropped icon with reference, get the probability of them being similar
        prob = cv2.matchTemplate(ult_icon, ult_icon_ref, cv2.TM_CCOEFF_NORMED).max()

        # To avoid possible explosion effect.
        # When ult gets ready, brightness of icon goes above limit.
        brightness = np.mean(ult_icon)
        prob = 1 if brightness > OW.ULT_ICON_MAX_BRIGHTNESS[self.frame.game.game_type] else prob

        if prob > OW.ULT_ICON_MAX_PROB[self.frame.game.game_type]:
            self.is_ult_ready = True

    def get_chara(self):
        """
        Retrieves chara name for current player in current frame.
        Compare cropped avatar with reference avatars, pick the best match as the chara current player plays with.
        @Author: Appcell
        @return: None
        """
        # Get background image to overlay reference avatar on.
        # Color of background image corresponds to team color of current player.
        all_avatars = self.frame.get_avatars(self.index)
        avatars_ref = all_avatars["normal"]
        avatars_small_ref = all_avatars["small"]

        # Crop avatar from frame
        avatar = ImageUtils.crop(self.image, OW.get_avatar_pos(self.index)[self.frame.game.game_type])
        
        # Compare cropped avatar with all reference avatars overlayed on team color background, then
        # pick the one with max similarity.
        # In OWL, currently observed player has a larger avatar. Choose the better match between the two.
        score = 0
        for (name, avatar_ref) in avatars_ref.iteritems():
            s = cv2.matchTemplate(avatar, avatar_ref, cv2.TM_CCOEFF_NORMED)[0][0]
            s_small = cv2.matchTemplate(avatar, avatars_small_ref[name], cv2.TM_CCOEFF_NORMED)[0][0]

            s_final = s if s > s_small else s_small
            if s_final > score:
                score = s_final
                self.chara = name
                self.is_observed = True if s > s_small else False

        self.get_living_status(avatars_ref[self.chara])

    def get_living_status(self, avatar_ref):
        """
        Retrieves chara living statues for current player.
        If the chara is dead, general variation of avatar brightness gets lower than reference.
        @Author: Appcell
        @param avatar_ref: reference avatar image
        @return: None
        """
        avatar = ImageUtils.crop(self.image, OW.get_avatar_pos_small(self.index)[self.frame.game.game_type])
        brightness = np.mean(avatar, 2)
        brightness_ref = np.mean(avatar_ref, 2)
        variation = brightness.max() - brightness.min();
        variation_ref = brightness_ref.max() - brightness_ref.min();

        if abs(variation_ref - variation) > 45:
            self.is_dead = True

    