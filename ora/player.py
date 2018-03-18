import cv2
import numpy as np
import skimage
from skimage import measure

from . import overwatch as OW
from .utils import image as ImageUtils



class Player:
    """Class of a Killfeed object.

    Contains info of one player in one frame.

    Attributes:
        index: index of player, from 0 to 11
        image: image of current frame
        team: team index
        chara: the character current player uses
        is_ult_ready: whether this player has primary ultimate ability now
        is_ult_2_ready: whether this player has secondary ultimate ability now
        is_dead: whether this chara is dead
        is_observed: whether this chara is observe by cam
        ult_charge: percentage of ultimate charge
        dva_status: see overwatch.py line 137-139. This is set in game.py
                    during postprocess

        avatars: list of combined avatart images
        ult_charge_numbers_ref: list of ult charge number images
    """

    def __init__(self, index, avatars, team, image, game_type, game_version, ult_charge_numbers_ref, time):
        """Initialize a Player object.

        Author:
            Appcell, GenesisX

        Args:
            index: row number of current player, ranges from 0 to 11.
            avatars: all character avatars for reference
            game_type: current game type
            team: index of the current team
            image: whole image of current frame
            ult_charge_numbers_ref: reference of ult charge numbers

        Returns:
            None 
        """
        self.index = index
        self.image = image
        self.team = team
        self.chara = None
        self.is_ult_ready = False
        self.is_secondary_ult_ready = False
        self.is_dead = False
        self.is_observed = None
        self.ult_charge = 0
        self.dva_status = OW.IS_NOT_DVA

        self.avatars = avatars
        self.ult_charge_numbers_ref = ult_charge_numbers_ref
        self.game_type = game_type
        self.game_version = game_version
        self.time = time
        # TODO: future work
        self.health = None
        self.is_onfire = None

        
        self.get_ult_status()
        self.get_chara()
        self.get_ult_charge()

        self.free()

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
        del self.image
        del self.avatars
        del self.ult_charge_numbers_ref

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
            self.index, self.game_type, self.game_version)
        ult_icon = ImageUtils.crop(self.image, ult_icon_pos)

        # Get reference icon image
        ult_icon_ref = OW.get_ult_icon_ref(
            self.index, self.game_type, self.game_version)
        # Tranfer both to grayscale for comparison
        ult_icon_ref = ImageUtils.rgb_to_gray(ult_icon_ref)
        ult_icon = ImageUtils.rgb_to_gray(ult_icon)

        # Compare cropped icon with reference, get the probability of them
        # being similar
        prob_map = cv2.matchTemplate(ult_icon, 
                                 ult_icon_ref, cv2.TM_CCOEFF_NORMED)
        prob_map_cropped = prob_map[0:(ult_icon.shape[0] - ult_icon_ref.shape[0]), :]
        _, prob, _, loc = cv2.minMaxLoc(prob_map_cropped)

        # To avoid possible explosion effect.
        # When ult gets ready, brightness of icon goes above limit.
        brightness = np.mean(ult_icon)
        deviation = np.std(ult_icon)

        if brightness > OW.ULT_ICON_MAX_BRIGHTNESS[self.game_type][self.game_version] \
            and deviation < OW.ULT_ICON_MAX_DEVIATION[self.game_type][self.game_version]:
            prob = 1
            self.is_ult_ready = True
            return

        temp_ult_icon = ImageUtils.crop(ult_icon, [loc[1], ult_icon_ref.shape[0], loc[0], ult_icon_ref.shape[1]])
        prob_ssim = measure.compare_ssim(
                            temp_ult_icon,
                            ult_icon_ref,
                            multichannel=False)

        if prob > OW.ULT_ICON_MAX_PROB[self.game_type][self.game_version]:
            if prob_ssim > OW.ULT_ICON_MAX_PROB_SSIM[self.game_type][self.game_version]:
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
        all_avatars = self.avatars
        avatars_ref_observed = all_avatars["observed"]
        avatars_ref = all_avatars["normal"]
        team_color = avatars_ref_observed['ana'][0, 0]

        # Crop avatar from frame
        avatar_observed = ImageUtils.crop(self.image, OW.get_avatar_pos_observed(
            self.index, self.game_type, self.game_version))
        avatar = ImageUtils.crop(self.image, OW.get_avatar_pos(
            self.index, self.game_type, self.game_version))

        # If player is observed, not sure about this tho
        avatar_diff = ImageUtils.crop(self.image, OW.get_avatar_diff_pos(
            self.index, self.game_type, self.game_version))
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
        for (name, avatar_ref_observed) in avatars_ref_observed.items():
            s_observed = cv2.matchTemplate(avatar_observed, avatar_ref_observed,
                                  cv2.TM_CCOEFF_NORMED)
            _, s_observed, _, loc_observed = cv2.minMaxLoc(s_observed)
            temp_avatar_observed = ImageUtils.crop(
                avatar_observed, 
                [loc_observed[1], avatar_ref_observed.shape[0], loc_observed[0], avatar_ref_observed.shape[1]])
            s_ssim_observed = measure.compare_ssim(temp_avatar_observed, avatar_ref_observed, 
                                          multichannel=True)
            s = cv2.matchTemplate(avatar, avatars_ref[
                                        name], cv2.TM_CCOEFF_NORMED)
            _, s, _, loc = cv2.minMaxLoc(s)
            temp_avatar = ImageUtils.crop(avatar, [loc[1], avatars_ref[
                                        name].shape[0], loc[0], avatars_ref[
                                        name].shape[1]])
            s_ssim = measure.compare_ssim(
                        temp_avatar,
                        avatars_ref[name],
                        multichannel=True)
            s_ssim_final = s_ssim_observed if s_ssim_observed > s_ssim else s_ssim
            s_final = s_observed if s_observed > s else s
            loc_final = loc_observed if s_observed > s else loc

            if s_final*0.4 + s_ssim_final*0.6 > score:
                score = s_final*0.4 + s_ssim_final*0.6
                self.chara = name

        if self.chara is None:
            self.chara = "empty"
            self.is_dead = True
            return

        if self.chara == OW.DVA:
            self.dva_status = OW.IS_WITH_MEKA
            
        self.get_living_status(avatars_ref_observed[self.chara])

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
            avatar = ImageUtils.crop(self.image, OW.get_avatar_pos_observed(
                self.index, self.game_type, self.game_version))
        else:
            avatar = ImageUtils.crop(self.image, OW.get_avatar_pos(
                self.index, self.game_type, self.game_version))
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
            Appcell
            
        Args:
            None

        Returns:
            None
        """

        if self.is_ult_ready:
            self.ult_charge = 100
            return

        ult_charge_pre_pos = OW.get_ult_charge_pre_pos(
            self.index, self.game_type, self.game_version)

        ult_charge_pre_image = ImageUtils.rgb_to_gray(
            ImageUtils.crop(self.image, ult_charge_pre_pos))

        ult_charge_shear = ImageUtils.shear(
            ult_charge_pre_image, OW.get_tf_shear(self.index, self.game_type, self.game_version))

        ult_charges = [0, 0]

        # Here's another thought: we need to find the gap more intellectually,
        # not relying only on fixed position.
        # In detail, after shearing, find the gap by telling if there are more
        # than 2 colors in same column.
        ult_charge_image = ImageUtils.crop(
            ult_charge_shear, 
            OW.get_ult_charge_pos(self.index, self.game_type, self.game_version))
        # TODO: I see there's no difference at all of brightness deviation!!
        # Our contrast adjusting must be seriously problematic. For grayscale
        # img, a simple normalization based on std would do.
        ult_charge_image_g = ImageUtils.normalize_gray(ult_charge_image)

        # tell if player is observed (more accurate than previous)
        # Here I use another local variable flag_observed, since the global one
        # might be inaccurate
        deviation_row = ult_charge_image_g.max(axis=1) - ult_charge_image_g.min(axis=1)
        if deviation_row[2] - deviation_row[0] > \
            OW.ULT_GAP_DEVIATION_LIMIT[self.game_type][self.game_version]:
            self.is_observed = True
        else:
            self.is_observed = False
        flag_observed = "observed" if self.is_observed else "normal"
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
        dev_list_left = []
        dev_list_right = []
        for i in range(width - 4, 3, -1):
            if deviation[i-3] - deviation[i] \
                > OW.ULT_GAP_DEVIATION_LIMIT[self.game_type][self.game_version] \
                and deviation[i+3] - deviation[i] \
                > OW.ULT_GAP_DEVIATION_LIMIT[self.game_type][self.game_version]:
                gap = i
                break
            dev_list_left.append(deviation[i-3] - deviation[i])
            dev_list_right.append(deviation[i+3] - deviation[i])

        bg_color = ult_charge_image_g[0, :].mean()
        if bg_color < 0.6:
            # Dark background
            ult_charge_image_g = ImageUtils.inverse_gray(ult_charge_image_g)

        # No need to switch to BW here.
        
        if gap == -1:
            # Only one digit
            num = ImageUtils.remove_digit_vertical_edge(
                ult_charge_image_g,
                OW.ULT_GAP_DEVIATION_LIMIT[self.game_type][self.game_version],
                ImageUtils.REMOVE_NUMBER_VERTICAL_EDGE_LEFT)
            if num.shape[1] < OW.ULT_CHARGE_IMG_WIDTH_OBSERVED[self.game_type][self.game_version]:
                padding = int(np.ceil((
                    OW.ULT_CHARGE_IMG_WIDTH_OBSERVED[self.game_type][self.game_version] - num.shape[1])/2))
                num = cv2.copyMakeBorder(
                    num, 0, 0,
                    padding, padding, cv2.BORDER_REPLICATE)
            self.ult_charge, score = self._identify_ult_charge_digit(
                num, 
                self.ult_charge_numbers_ref[flag_observed])
        else:
            # 2 digits
            num_left = ImageUtils.crop(
                ult_charge_image_g, 
                [0, ult_charge_image_g.shape[0], 0, gap + 1])
            num_right = ImageUtils.crop(
                ult_charge_image_g, 
                [0, ult_charge_image_g.shape[0], gap, ult_charge_image_g.shape[1] - gap])

            if self.is_observed:
                num_left = ImageUtils.crop(
                    num_left,
                    [0, num_left.shape[0], num_left.shape[1] \
                        - OW.ULT_CHARGE_NUMBER_WIDTH_OBSERVED[self.game_type][self.game_version] - 1, 
                     OW.ULT_CHARGE_NUMBER_WIDTH_OBSERVED[self.game_type][self.game_version]])
                num_right = ImageUtils.crop(
                    num_right,
                    [0, num_left.shape[0], 0, 
                     OW.ULT_CHARGE_NUMBER_WIDTH_OBSERVED[self.game_type][self.game_version]])
            else:
                num_left = ImageUtils.crop(
                    num_left,
                    [0, num_left.shape[0], num_left.shape[1] \
                        - OW.ULT_CHARGE_NUMBER_WIDTH[self.game_type][self.game_version] - 1, 
                     OW.ULT_CHARGE_NUMBER_WIDTH[self.game_type][self.game_version]])
                num_right = ImageUtils.crop(
                    num_right,
                    [0, num_left.shape[0], 0, 
                     OW.ULT_CHARGE_NUMBER_WIDTH[self.game_type][self.game_version]])
            if num_right.shape[1] < OW.ULT_CHARGE_IMG_WIDTH[self.game_type][self.game_version]:
                num_right = cv2.copyMakeBorder(
                    num_right, 0, 0, 0, 
                    OW.ULT_CHARGE_IMG_WIDTH[self.game_type][self.game_version] \
                        - num_right.shape[1], cv2.BORDER_REPLICATE)
            if num_left.shape[1] < OW.ULT_CHARGE_IMG_WIDTH[self.game_type][self.game_version]:
                num_left = cv2.copyMakeBorder(
                    num_left, 0, 0,
                    OW.ULT_CHARGE_IMG_WIDTH[self.game_type][self.game_version] \
                        - num_left.shape[1], 0, cv2.BORDER_REPLICATE)
            num_left_value, score_left = self._identify_ult_charge_digit(
                num_left, 
                self.ult_charge_numbers_ref[flag_observed])
            num_right_value, score_right = self._identify_ult_charge_digit(
                num_right, 
                self.ult_charge_numbers_ref[flag_observed])
            if score_left < OW.ULT_CHARGE_SSIM_THRESHOLD[self.game_type][self.game_version] \
            or score_right < OW.ULT_CHARGE_SSIM_THRESHOLD[self.game_type][self.game_version]:
                # Then it's actually 1 digit
                self.ult_charge, score = self._identify_ult_charge_digit(
                    ult_charge_image_g, 
                    self.ult_charge_numbers_ref[flag_observed])
            else:
                self.ult_charge = num_left_value * 10 + num_right_value

        return 

    def _identify_ult_charge_digit(self, digit, digit_refs):
        """Retrieves ultimate charge for current player.

        Author:
            Appcell
            
        Args:
            None

        Returns:
            None
        """
        score = 0
        res = -1
        digit = ImageUtils.float_to_uint8(digit)
        for i in range(10):
            match_result = []

            match_result = cv2.matchTemplate(
                digit, digit_refs[i], cv2.TM_CCOEFF_NORMED)

            _, max_val, _, max_loc = cv2.minMaxLoc(match_result)
            temp_digit = ImageUtils.crop(
                digit, 
                [max_loc[1], digit_refs[i].shape[0], max_loc[0], digit_refs[i].shape[1]])

            score_ssim = measure.compare_ssim(temp_digit, digit_refs[i], multichannel=True)
            if score_ssim + max_val > score:
                score = score_ssim + max_val
                res = i
        return [res, score]

    def dict(self):
        d = {
            'index': self.index + 1,
            'team': self.team,
            'chara': self.chara,
            'is_ult_ready': self.is_ult_ready,
            'is_dead': self.is_dead,
            'ult_charge': self.ult_charge,
            'dva_status': self.dva_status,
        }
        return d
