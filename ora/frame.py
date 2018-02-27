import cv2
import numpy as np
from skimage import measure
import overwatch as OW
import gui as Gui
from utils import image as ImageUtils
from player import Player
from killfeed import Killfeed
import pool

import time

class Frame(object):
    """Class of a Frame object.

    Retrieves and stores all info captured in one frame.

    Attributes:
        is_valid: If the frame itself is valid, i.e. during a match
        players: List of Player instances in current frame, usually 12
        killfeeds: List of Killfeed instances in current frame, 6 at max
        image: image of the frame, resized to 720p
        time: time of frame in video, in seconds
        game: the Game object who fathers all frames
    """

    def __init__(self, frame_image, frame_time, game):
        """Initialize a Frame object.

        Author:
            Appcell

        Args:
            frame_image: the image cropped from video for this frame
            frame_time: time of frame in video, in seconds
            game: the Game object which controls all frames

        Returns:
            None 
        """
        t1 = time.time()
        self.is_valid = False
        self.players = []
        self.killfeeds = []
        self.image = ImageUtils.resize(frame_image, 1280, 720)
        self.time = frame_time
        self.game = game
        if self.game.ult_colors is None:
            self.game.set_ult_colors(self)

        # Gui.gui_instance.show_progress(self.time)
        print self.time
        self.get_players()
        self.get_killfeeds()
        self.validate()
        self.free()

        t2 = time.time()
        print(t2 - t1)
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

    def get_players(self):
        """Get all players info in this frame.

        Author:
            Appcell, GenesisX

        Args:
            None

        Returns:
            None 
        """
        # Multiprocess players

        game_type = self.game.game_type
        image = self.image
        ult_charge_numbers_ref = self.game.ult_charge_numbers_ref

        results = []

        for i in range(0, 12):
            avatars = self.get_avatars(i)
            team = ""
            name = ""

            if i < 6:
                name = self.game.name_players_team_left[i]
            else:
                name = self.game.name_players_team_right[i - 6]
            if i < 6:
                team = self.game.team_names['left']
            else:
                team = self.game.team_names['right']

            results.append(pool.PROCESS_POOL.apply_async(Player, args=(
                i, avatars, name, team, image, game_type, ult_charge_numbers_ref)))
        
        for res in results:
            self.players.append(res.get())

    def get_team_colors_from_image(self):
        """Get team colors from this frame.

        Author:
            Appcell

        Args:
            None

        Returns:
            None 
        """
        pos = OW.get_team_color_pick_pos()[self.game.game_type]

        return {
            "left": self.image[pos[0][0], pos[0][1]],
            "right": self.image[pos[1][0], pos[1][1]]
        }

    def get_team_colors(self):
        if self.game.team_colors is not None:
            return self.game.team_colors
        else:
            return self.get_team_colors_from_image()

    def get_ult_colors_from_image(self):
        """Get ultimate charge number colors from this frame.

        Author:
            Rigel

        Args:
            None

        Returns:
            @ult_color: array of int, -1: white number, 1: black number
        """
        left_pre_pos = OW.get_ult_charge_color_pre_pos(True)[self.game.game_type]
        left_pre_image = ImageUtils.rgb_to_gray(ImageUtils.crop(self.image, left_pre_pos))
        left_shear = ImageUtils.shear(left_pre_image, OW.get_tf_shear(True)[self.game.game_type])
        left_pos = OW.get_ult_charge_color_pos(True)[self.game.game_type]
        left_image = ImageUtils.crop(left_shear, left_pos)
        left_image_g = ImageUtils.contrast_adjust_log(left_image, OW.ULT_ADJUST_LOG_INDEX)
        left_bin = ImageUtils.binary_otsu(left_image_g)

        right_pre_pos = OW.get_ult_charge_color_pre_pos(False)[self.game.game_type]
        right_pre_image = ImageUtils.rgb_to_gray(ImageUtils.crop(self.image, right_pre_pos))
        right_shear = ImageUtils.shear(right_pre_image, OW.get_tf_shear(False)[self.game.game_type])
        right_pos = OW.get_ult_charge_color_pos(False)[self.game.game_type]
        right_image = ImageUtils.crop(right_shear, right_pos)
        right_image_g = ImageUtils.contrast_adjust_log(right_image, OW.ULT_ADJUST_LOG_INDEX)
        right_bin = ImageUtils.binary_otsu(right_image_g)
        return {
            "left": np.sign(2 * np.sum(left_bin) - np.size(left_bin)),
            "right": np.sign(2 * np.sum(right_bin) - np.size(right_bin))
        }

    def get_ult_colors(self):
        if self.game.ult_colors is not None:
            return self.game.ult_colors
        else:
            return self.get_ult_colors_from_image()

    def get_killfeeds(self):
        """Get killfeed info in this frame.

        Author:
            Appcell

        Args:
            None

        Returns:
            None 
        """
        for i in range(6):
            killfeed = Killfeed(self, i)
            if killfeed.is_valid is True:
                if self.game.frames and self.game.frames[-1].killfeeds:
                    last_killfeed = self.game.frames[-1].killfeeds[-1]
                    if killfeed == last_killfeed:
                        self.killfeeds.append(killfeed)
                        break
                    else:
                        self.killfeeds.append(killfeed)
                else:
                    self.killfeeds.append(killfeed)
            elif i >= 1:
                break

        self.killfeeds.reverse()

    def validate(self):
        """Validate this frame, set up Game obj if it's not set.

        Validation by:
        1) Test if there's any players detectable. If none, frame is invalid
        2) Test if top-right corner is white. If not, frame is invalid
        If frame is valid and Game info (i.e. team colors, avatars) are not
        set, set them up.

        Author:
            Appcell

        Args:
            None

        Returns:
            None 
        """
        flag = False
        for player in self.players:
            if player.is_dead is False:
                flag = True

        if flag == False:
            self.is_valid = False
            return
        else:
            self.is_valid = True
        validation_roi = ImageUtils.crop(self.image,
                                         OW.FRAME_VALIDATION_POS[self.game.game_type])

        std = np.max([np.std(validation_roi[:, :, 0]),
                      np.std(validation_roi[:, :, 1]),
                      np.std(validation_roi[:, :, 2])])

        mean = [np.mean(validation_roi[:, :, 0]),
                np.mean(validation_roi[:, :, 1]),
                np.mean(validation_roi[:, :, 2])]


        if std < OW.FRAME_VALIDATION_COLOR_STD[self.game.game_type] \
                and np.mean(mean) > OW.FRAME_VALIDATION_COLOR_MEAN[self.game.game_type] \
                and flag is True:
            self.is_valid = True
        else:
            self.is_valid = False
            return

        replay_icon = ImageUtils.crop(
            self.image, OW.get_replay_icon_pos()[self.game.game_type])

        replay_icon_preseason = ImageUtils.crop(
            self.image, OW.get_replay_icon_preseason_pos()[self.game.game_type])
        max_val = measure.compare_ssim(
                replay_icon, self.game.replay_icon_ref, multichannel=True)
        max_val_preseason = measure.compare_ssim(
                replay_icon_preseason, self.game.replay_icon_ref, multichannel=True)
        

        # TODO: another situation: after replay effect there might be a blue
        # rectangle remaining on screen.
        max_val = max_val if max_val > max_val_preseason else max_val_preseason
        if max_val < OW.FRAME_VALIDATION_REPLAY_PROB[self.game.game_type]:
            self.is_valid = True
        else:
            self.is_valid = False
            return

        if self.is_valid is True and self.game.team_colors is None:
            self.game.set_team_colors(self)
            self.game.avatars_ref = self._get_avatars_before_validation()

    def _get_avatars_before_validation(self):
        """Get fused avatar icons for this frame.

        Used when Game info is not set. First pick team colors from current
        frame, then overlay transparent icons on them and form new avatars. 
        Color of background image corresponds to team color of current player.
        
        Author:
            Appcell

        Args:
            None

        Returns:
            A dict of all avatar icons fused
        """
        team_colors = self.get_team_colors()
        avatars_left_ref = {}
        avatars_small_left_ref = {}
        avatars_right_ref = {}
        avatars_small_right_ref = {}

        # Create background image with team color
        bg_image_left = ImageUtils.create_bg_image(
            team_colors["left"], OW.AVATAR_WIDTH_REF, OW.AVATAR_HEIGHT_REF)
        bg_image_right = ImageUtils.create_bg_image(
            team_colors["right"], OW.AVATAR_WIDTH_REF, OW.AVATAR_HEIGHT_REF)
        avatars_ref = OW.get_avatars_ref()

        # Overlay transparent reference avatar on background
        for (name, avatar_ref) in avatars_ref.iteritems():
            avatars_left_ref[name] = ImageUtils.overlay(
                bg_image_left, avatar_ref)
            avatars_small_left_ref[name] = ImageUtils.resize(
                ImageUtils.overlay(bg_image_left, avatar_ref), 33, 26)
            avatars_right_ref[name] = ImageUtils.overlay(
                bg_image_right, avatar_ref)
            avatars_small_right_ref[name] = ImageUtils.resize(
                ImageUtils.overlay(bg_image_right, avatar_ref), 33, 26)

        return {
            "left": avatars_left_ref,
            "left_small": avatars_small_left_ref,
            "right": avatars_right_ref,
            "right_small": avatars_small_right_ref
        }

    def get_avatars(self, index):
        """Get fused avatar icons for a player.

        If Game info is set, retrieves avatars from Game obj.
        If not, generate avatars from frame itself.

        Author:
            Appcell

        Args:
            Index: Index of player.

        Returns:
            A dict of avatars.
        """
        all_avatars = {}
        if self.game.team_colors is not None:
            all_avatars = self.game.avatars_ref
        else:
            all_avatars = self._get_avatars_before_validation()

        if index < 6:
            return {
                "normal": all_avatars['left'],
                "small": all_avatars['left_small']
            }
        return {
            "normal": all_avatars['right'],
            "small": all_avatars['right_small']
        }