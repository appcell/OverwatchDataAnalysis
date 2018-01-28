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
        self.ult_charge = 0

        # TODO: future work
        self.health = None
        self.is_onfire = None



        self.get_ult_status()
        self.get_chara()
        self.get_ult_charge()
        self.free()

        # if self.index == 3:
        #     print self.index
        #     print self.chara
        #     print self.is_dead
        #     print "==="

    def free(self):
        """Free RAM by removing images from the Frame instance.
        Done after analysis.
        Author:
            Appcell
        Args:
            None
        Returns:
            None 
        """
        self.image = None

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
        prob_map = cv2.matchTemplate(ult_icon, 
                                 ult_icon_ref, cv2.TM_CCOEFF_NORMED)
        prob_map_cropped = prob_map[0:(ult_icon.shape[0] - ult_icon_ref.shape[0]), :]
        _, prob, _, loc = cv2.minMaxLoc(prob_map_cropped)

        # To avoid possible explosion effect.
        # When ult gets ready, brightness of icon goes above limit.
        brightness = np.mean(ult_icon)

        if brightness > OW.ULT_ICON_MAX_BRIGHTNESS[self.frame.game.game_type]:
            prob = 1
            self.is_ult_ready = True
            return

        if prob > OW.ULT_ICON_MAX_PROB[self.frame.game.game_type]:
            temp_ult_icon = ImageUtils.crop(ult_icon, [loc[1], ult_icon_ref.shape[0], loc[0], ult_icon_ref.shape[1]])
            prob_ssim = measure.compare_ssim(
                            temp_ult_icon,
                            ult_icon_ref,
                            multichannel=False)
            if prob_ssim > OW.ULT_ICON_MAX_PROB_SSIM[self.frame.game.game_type]:
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
        team_color = avatars_ref['ana'][0, 0]

        # Crop avatar from frame
        avatar = ImageUtils.crop(self.image, OW.get_avatar_pos(
            self.index)[self.frame.game.game_type])
        avatar_small = ImageUtils.crop(avatar, [4, avatar.shape[0] - 4, 0, avatar.shape[1]])

        # If player is observed, not sure about this tho
        avatar_diff = ImageUtils.crop(self.image, OW.get_avatar_diff_pos(
            self.index)[self.frame.game.game_type])
        max_diff = 0
        for i in range(avatar_diff.shape[0]):
            for j in range(avatar_diff.shape[1]):
                if ImageUtils.color_distance(
                        avatar_diff[i, j], team_color) > max_diff:
                    max_diff = ImageUtils.color_distance(
                        avatar_diff[i, j], team_color)
        if max_diff < 40 and self.is_ult_ready is False:
            self.is_observed = True
        score = 0
        for (name, avatar_ref) in avatars_ref.iteritems():
            s = cv2.matchTemplate(avatar, avatar_ref,
                                  cv2.TM_CCOEFF_NORMED)
            _, s, _, loc1 = cv2.minMaxLoc(s)
            temp_avatar = ImageUtils.crop(avatar, [loc1[1], avatar_ref.shape[0], loc1[0], avatar_ref.shape[1]])
            s_ssim1 = measure.compare_ssim(temp_avatar, avatar_ref, 
                                          multichannel=True)
            s_small = cv2.matchTemplate(avatar_small, avatars_small_ref[
                                        name], cv2.TM_CCOEFF_NORMED)
            _, s_small, _, loc2 = cv2.minMaxLoc(s_small)
            temp_avatar2 = ImageUtils.crop(avatar_small, [loc2[1], avatars_small_ref[
                                        name].shape[0], loc2[0], avatars_small_ref[
                                        name].shape[1]])
            s_ssim2 = measure.compare_ssim(
                        temp_avatar2,
                        avatars_small_ref[name],
                        multichannel=True)
            s_ssim = s_ssim1 if s > s_small else s_ssim2
            s_final = s if s > s_small else s_small
            loc = loc1 if s > s_small else loc2

            if s_final + s_ssim > score:
                score = s_final + s_ssim
                self.chara = name

        if self.chara is None:
            self.chara = "empty"
            self.is_dead = True
            return
            
        self.get_living_status(avatars_ref[self.chara])

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
        avatar = []
        if self.is_observed:
            avatar = ImageUtils.crop(self.image, OW.get_avatar_pos(
                self.index)[self.frame.game.game_type])
        else:
            avatar = ImageUtils.crop(self.image, OW.get_avatar_pos_small(
                self.index)[self.frame.game.game_type])
        brightness = np.mean(avatar, 2)
        brightness_ref = np.mean(avatar_ref, 2)
        variation = brightness.max() - brightness.min()
        variation_ref = brightness_ref.max() - brightness_ref.min()
        
        # TODO: write consts here into ow.py
        if abs(variation_ref - variation) > 45:
            self.is_dead = True

    def get_ult_charge(self):
        """Retrieves ultimate charge for current player.

        Author:

        Args:
            None

        Returns:
            None
        """
        if self.is_ult_ready:
            self.ult_charge = 100
            return
        if self.is_dead:
            return

        ult_charge_pre_pos = OW.get_ult_charge_pre_pos(
            self.index)[self.frame.game.game_type]
        ult_charge_pre_image = ImageUtils.rgb_to_gray(
            ImageUtils.crop(self.image, ult_charge_pre_pos))

        ult_charge_shear = ImageUtils.shear(
            ult_charge_pre_image, OW.get_tf_shear(self.index)[self.frame.game.game_type])

        ult_charges = [0, 0]

        # Here's another thought: we need to find the gap more intellectually,
        # not relying only on fixed position.
        # In detail, after shearing, find the gap by telling if there are more
        # than 2 colors in same column.
        ult_charge_image = ImageUtils.crop(
            ult_charge_shear, 
            OW.get_ult_charge_pos(self.index)[self.frame.game.game_type])

        # TODO: I see there's no difference at all of brightness deviation!!
        # Our contrast adjusting must be seriously problematic. For grayscale
        # img, a simple normalization based on std would do.
        # ult_charge_image_g = ImageUtils.contrast_adjust_log(
        #     ult_charge_image, OW.ULT_ADJUST_LOG_INDEX)
        ult_charge_image_g = ImageUtils.normalize_gray(ult_charge_image)

        # tell if player is observed (more accurate than previous)
        # Here I use another local variable flag_observed, since the global one
        # might be inaccurate
        flag_observed = False
        deviation_row = ult_charge_image_g.max(axis=1) - ult_charge_image_g.min(axis=1)
        if deviation_row[2] - deviation_row[0] > \
            OW.ULT_GAP_DEVIATION_LIMIT[self.frame.game.game_type]:
            self.is_observed = True
            flag_observed = True

        # If current player is observed, there's a white dot on right side
        # needs to be removed.
        # TODO: write this into ow.py as well
        if flag_observed is True:
            ult_charge_image_g = ImageUtils.crop(
                ult_charge_image_g,
                [0, ult_charge_image_g.shape[0], 0, ult_charge_image_g.shape[1] - 5])
        width = ult_charge_image_g.shape[1]
        height = ult_charge_image_g.shape[0]

        # Find the gap
        deviation = ult_charge_image_g.max(axis=0) - ult_charge_image_g.min(axis=0)
        gap = -1
        for i in range(width - 4, 3, -1):
            if deviation[i-3] - deviation[i] \
                > OW.ULT_GAP_DEVIATION_LIMIT[self.frame.game.game_type] \
                and deviation[i+3] - deviation[i] \
                > OW.ULT_GAP_DEVIATION_LIMIT[self.frame.game.game_type]:
                gap = i
                break

        bg_color = ult_charge_image_g[:, 0].mean()

        if bg_color < 0.6:
            # Dark background
            ult_charge_image_g = ImageUtils.inverse_gray(ult_charge_image_g)
        # No need to switch to BW here.


        # cv2.imshow('t', ult_charge_image_g)
        # cv2.waitKey(0)

        if gap == -1:
            # Only one digit
            num = ImageUtils.remove_digit_vertical_edge(
                ult_charge_image_g,
                OW.ULT_GAP_DEVIATION_LIMIT[self.frame.game.game_type],
                ImageUtils.REMOVE_NUMBER_VERTICAL_EDGE_BOTH)
            # if self.index >= 6:
            #     cv2.imshow('t', ult_charge_image_g)
            #     cv2.waitKey(0)
            #     cv2.imshow('t1', num)
            #     cv2.waitKey(0)
        else:
            # 2 digits
            num_left = ImageUtils.crop(
                ult_charge_image_g, 
                [0, ult_charge_image_g.shape[0], 0, gap + 1])
            num_right = ImageUtils.crop(
                ult_charge_image_g, 
                [0, ult_charge_image_g.shape[0], gap, ult_charge_image_g.shape[1] - gap])

            if flag_observed is True:
                num_left = ImageUtils.crop(
                    num_left,
                    [0, num_left.shape[0], num_left.shape[1] \
                        - OW.ULT_CHARGE_NUMBER_WIDTH_OBSERVED[self.frame.game.game_type] - 1, 
                     OW.ULT_CHARGE_NUMBER_WIDTH_OBSERVED[self.frame.game.game_type]])
                num_right = ImageUtils.crop(
                    num_right,
                    [0, num_left.shape[0], 0, 
                     OW.ULT_CHARGE_NUMBER_WIDTH_OBSERVED[self.frame.game.game_type]])
            else:
                num_left = ImageUtils.crop(
                    num_left,
                    [0, num_left.shape[0], num_left.shape[1] \
                        - OW.ULT_CHARGE_NUMBER_WIDTH_OBSERVED[self.frame.game.game_type] - 1, 
                     OW.ULT_CHARGE_NUMBER_WIDTH_OBSERVED[self.frame.game.game_type]])
                num_right = ImageUtils.crop(
                    num_right,
                    [0, num_left.shape[0], 0, 
                     OW.ULT_CHARGE_NUMBER_WIDTH_OBSERVED[self.frame.game.game_type]])

            # if self.index == 5:
            #     cv2.imshow('t1', num_left)
            #     cv2.waitKey(0)            
            #     cv2.imshow('t2', num_right)
            #     cv2.waitKey(0)
            # Since when cropping img we also included the slope on left side,
            # num_left could actually be empty
            # Also we need another recognition method. Simple MSE wouldn't work due to error.
            




        # ult_charge_image_g = ImageUtils.contrast_adjust_log(
        #     ult_charge_image, OW.ULT_ADJUST_LOG_INDEX)

        # for i in (0,1):
            

        #     cv2.imshow('t', ult_charge_image)
        #     cv2.waitKey(0)
        #     try:
        #         ult_charge_image_binary = ImageUtils.binary_otsu(ult_charge_image_g)

        #     except ValueError:
        #         self.ult_charge = None
        #         return
        #     ult_charge_similarities = np.zeros(11)
        #     for j in range(1 - i, 11-i):
        #         # 1st number can't be 0, 2nd number can't be empty
        #         ult_charge_ref = self.frame.game.ult_charge_numbers_ref[j - i]
        #         ult_charge_similarities[j] = ImageUtils.similarity(ult_charge_ref, ult_charge_image_binary)
        #     ult_charges[i] = np.argmax(ult_charge_similarities)
        #     print ult_charges[i]
        #     if ult_charges[i] == 10:
        #         ult_charges[i] = 0

        self.ult_charge = ult_charges[0] * 10 + ult_charges[1]
        return
