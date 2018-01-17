import cv2
import numpy as np
import skimage
from skimage import measure

import overwatch as OW
from utils import image as ImageUtils



class Player:
    """Class of a Killfeed object.

    Contains info of one player in one frame.

    Attributes:
        index: index of player, from 0 to 11
        frame: pointer to frame obj
        image: image of current frame
        name: the player name
        team: team name
        chara: the character current player uses
        is_ult_ready: whether this player has ultimate ability now
        is_dead: whether this chara is dead
        is_observed: whether this chara is observe by cam
    """

    def __init__(self, index, frame):
        """Initialize a Player object.

        Author:
            Appcell

        Args:
            frame: the Frame obj current player is in
            index: row number of current player, ranges from 0 to 11.

        Returns:
            None 
        """
        self.index = index
        self.frame = frame
        self.image = self.frame.image
        if index < 6:
            self.name = self.frame.game.name_players_team_left[index]
        else:
            self.name = self.frame.game.name_players_team_right[index - 6]
        if index < 6:
            self.team = self.frame.game.team_names['left']
        else:
            self.team = self.frame.game.team_names['right']
        self.chara = None
        self.is_ult_ready = False
        self.is_dead = False
        self.is_observed = None 

        # TODO: future work
        self.health = None
        self.ult_charge = None
        self.is_onfire = None

        self.get_ult_status()
        self.get_chara()

    def get_ult_status(self):
        """Retrieves ultimate statues info for current player in current frame.

        Author:
            Appcell

        Args:
            None

        Returns:
            None 
        """
        # Crop icon from current frame
        ult_icon_pos = OW.get_ult_icon_pos(
            self.index)[self.frame.game.game_type]
        ult_icon = ImageUtils.crop(self.image, ult_icon_pos)
        # Get reference icon image
        ult_icon_ref = OW.get_ult_icon_ref(
            self.index)[self.frame.game.game_type]
        # Tranfer both to grayscale for comparison
        ult_icon_ref, ult_icon = ImageUtils.rgb_to_gray(
            ult_icon_ref), ImageUtils.rgb_to_gray(ult_icon)

        # Compare cropped icon with reference, get the probability of them
        # being similar
        prob = cv2.matchTemplate(ult_icon, 
                                 ult_icon_ref, cv2.TM_CCOEFF_NORMED).max()

        # To avoid possible explosion effect.
        # When ult gets ready, brightness of icon goes above limit.
        brightness = np.mean(ult_icon)

        if brightness > OW.ULT_ICON_MAX_BRIGHTNESS[self.frame.game.game_type]:
            prob = 1

        if prob > OW.ULT_ICON_MAX_PROB[self.frame.game.game_type]:
            self.is_ult_ready = True

    def get_chara(self):
        """Retrieves chara name for current player in current frame.

        Compare cropped avatar with reference avatars, pick the best match as 
        the chara current player plays with. In OWL, currently observed player
        has a larger avatar. To differentiate between the two, comparison has
        to run twice and the better match gets chosen.

        Author:
            Appcell

        Args:
            None

        Returns:
            None 
        """
        all_avatars = self.frame.get_avatars(self.index)
        avatars_ref = all_avatars["normal"]
        avatars_small_ref = all_avatars["small"]

        # Crop avatar from frame
        avatar = ImageUtils.crop(self.image, OW.get_avatar_pos(
            self.index)[self.frame.game.game_type])
        avatar_small = ImageUtils.crop(avatar, [1, avatar.shape[0] - 4, 0, avatar.shape[1]])
        score = 0
        # if self.index == 0:
        #     cv2.imshow('t',avatar)
        #     cv2.imshow('t',avatar_small)
        #     cv2.waitKey(0)
        for (name, avatar_ref) in avatars_ref.iteritems():

            s = cv2.matchTemplate(avatar, avatar_ref,
                                  cv2.TM_CCOEFF_NORMED)
            _, s, _, _ = cv2.minMaxLoc(s)
            s_small = cv2.matchTemplate(avatar_small, avatars_small_ref[
                                        name], cv2.TM_CCOEFF_NORMED)
            _, s_small, _, _ = cv2.minMaxLoc(s_small)

            s_final = s if s > s_small else s_small

            # if self.index == 0 and (name == 'roadhog' or name == 'symmetra' or name == 'orisa'):
            #     print [name, s_small, s]
            if s_final > score:
                score = s_final
                self.chara = name
                self.is_observed = True if s > s_small else False

        if self.chara == None:
            self.chara = "empty"
            self.is_dead = True
            return
            
        self.get_living_status(avatars_ref[self.chara])
        # if self.index == 0:
        #     print self.is_dead

    def get_living_status(self, avatar_ref):
        """Retrieves chara living status for current player.

        If the chara is dead, general variation of avatar brightness gets lower
        than reference.

        Author:
            Appcell

        Args:
            avatar_ref: reference avatar image

        Returns:
            None 
        """
        avatar = ImageUtils.crop(self.image, OW.get_avatar_pos_small(
            self.index)[self.frame.game.game_type])
        brightness = np.mean(avatar, 2)
        brightness_ref = np.mean(avatar_ref, 2)
        variation = brightness.max() - brightness.min()
        variation_ref = brightness_ref.max() - brightness_ref.min()

        # TODO: write consts here into ow.py
        if abs(variation_ref - variation) > 45:
            self.is_dead = True
