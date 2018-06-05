import cv2
import logging
import numpy as np
from skimage import measure
from . import overwatch as OW
from . import gui as Gui
from .utils import image as ImageUtils
from .player import Player
from .killfeed import Killfeed
from . import pool

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

    def __init__(self, frame_image, frame_time, game, game_version=0, game_type=0):
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
        self.current_time = time.time()
        self.is_valid = False
        self.is_replay = False
        self.players = [None] * 12
        self.killfeeds = []
        self.image = ImageUtils.resize(frame_image, OW.DEFAULT_SCREEN_WIDTH, OW.DEFAULT_SCREEN_HEIGHT)

        logging.debug('resize time: %d ms', (time.time() - self.current_time) * 1000)
        self.current_time = time.time()

        self.time = frame_time
        self.game = game
        self.game_version = game_version
        self.game_type = game.game_type
        
        # Gui.gui_instance.show_progress(self.time)

        print(self.time)
        if self.game_type != OW.GAMETYPE_1ST:
            self.get_players() # Costs 246ms on i5
            logging.debug('get_players time: %d ms', (time.time() - self.current_time) * 1000)
            self.current_time = time.time()

        self.get_killfeeds() # Costs 38ms on i5
        logging.debug('get_killfeeds time: %d ms', (time.time() - self.current_time) * 1000)
        self.current_time = time.time()

        self.validate() # Costs 3ms on i5
        logging.debug('validate time: %d ms', (time.time() - self.current_time) * 1000)
        self.current_time = time.time()

        self.free() # Costs 0ms on i5
        logging.debug('free time: %d ms', (time.time() - self.current_time) * 1000)
        self.current_time = time.time()

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

    def player_callback(self, result):
        self.players[result.index] = result

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

        game_type = self.game_type
        game_version = self.game_version
        image = self.image
        ult_charge_numbers_ref = self.game.ult_charge_numbers_ref
        results = []

        for i in range(0, 12):
            # current_time = time.time()
            avatars = self.get_avatars(i) # 12ms each, or 0 after 1st time.
            # print("--- get_avatars %s ms ---" % ((time.time() - current_time) * 1000))
            team = -1

            if i < 6:
                team = self.game.team_names[OW.LEFT]
            else:
                team = self.game.team_names[OW.RIGHT]

            self.players[i] = Player(i, avatars, team, image, game_type, game_version, ult_charge_numbers_ref, self.time)
            # results.append(pool.PROCESS_POOL.apply_async(Player, 
            #     args=(i, avatars, team, image, game_type, game_version, ult_charge_numbers_ref, self.time),
            #     callback=self.player_callback))
        
        # for res in results:
        #     res.wait()
        
    def get_team_colors_from_image(self):
        """Get team colors from this frame.

        Author:
            Appcell

        Args:
            None

        Returns:
            None 
        """
        pos = OW.get_team_color_pick_pos(self.game_type, self.game_version)

        return [
            self.image[pos[0][0], pos[0][1]],
            self.image[pos[1][0], pos[1][1]]
        ]

    def get_team_colors(self):
        if self.game_type == OW.GAMETYPE_OWL:
            if self.game.team_colors is not None:
                return self.game.team_colors
            else:
                return self.get_team_colors_from_image()
        elif self.game_type == OW.GAMETYPE_CUSTOM or self.game_type == OW.GAMETYPE_1ST:
            return OW.TEAM_COLORS_DEFAULT[self.game_type][self.game_version]

    def get_killfeeds(self):
        """Get killfeed info in this frame.

        Author:
            Appcell, GenesisX

        Args:
            None

        Returns:
            None 
        """
        for i in range(6):
            killfeed = Killfeed(self, i)
            if killfeed.is_valid is True:
                self.killfeeds.append(killfeed)
                if self.game.frames and self.game.frames[-1].killfeeds:

                    last_killfeed = self.game.frames[-1].killfeeds[-1]
                    if killfeed == last_killfeed:
                        break
            elif i >= 1:
                break

        self.killfeeds.reverse()

    def validate(self):
        """Validate this frame, set up Game obj if it's not set.

        Validation by:
        1) Test if there's any players detectable. If none, frame is invalid
        2) Test if top-right corner is white for OWL. If not, frame is invalid
        If frame is valid and Game info (i.e. team colors, avatars) are not
        set, set them up.

        Author:
            Appcell

        Args:
            None

        Returns:
            None 
        """
        self.is_valid = True
        flag = False
        # 1) Test if there's any players detectable. If none, frame is invalid
        # This is only for non 1st person games.
        if self.game_type != OW.GAMETYPE_1ST:
            for player in self.players:
                if player.is_dead is False:
                    flag = True
                    break

            if flag is False:
                self.is_valid = False
                return


        # 2) Test if top-right corner is white. If not, frame is invalid.
        # This is only for OWL games.
        if self.game_type == OW.GAMETYPE_OWL:
            validation_roi = ImageUtils.crop(
                self.image,
                OW.get_frame_validation_pos(self.game_type, self.game_version))
            std = np.max([np.std(validation_roi[:, :, 0]),
                          np.std(validation_roi[:, :, 1]),
                          np.std(validation_roi[:, :, 2])])
            mean = [np.mean(validation_roi[:, :, 0]),
                    np.mean(validation_roi[:, :, 1]),
                    np.mean(validation_roi[:, :, 2])]

            if std < OW.FRAME_VALIDATION_COLOR_STD[self.game_type][self.game_version] \
                    and np.mean(mean) \
                        > OW.FRAME_VALIDATION_COLOR_MEAN[self.game_type][self.game_version] \
                    and flag is True:
                self.is_valid = True
            else:
                self.is_valid = False
                return

        # 3) Test if current frame is during replay. Still, for OWL only.
        if self.game_type == OW.GAMETYPE_OWL:
            replay_icon = ImageUtils.crop(
                self.image, OW.get_replay_icon_pos(self.game_type, self.game_version))

            replay_icon_preseason = ImageUtils.crop(
                self.image, OW.get_replay_icon_preseason_pos(self.game_type, self.game_version))
            max_val = measure.compare_ssim(
                replay_icon, self.game.replay_icon_ref, multichannel=True)
            max_val_preseason = measure.compare_ssim(
                replay_icon_preseason, self.game.replay_icon_ref, multichannel=True)

            max_val = max_val if max_val > max_val_preseason else max_val_preseason
            if max_val < OW.FRAME_VALIDATION_REPLAY_PROB[self.game_type][self.game_version]:
                self.is_valid = True
            else:
                self.is_valid = False
                self.is_replay = True
                return

        # 4) If frame is valid and Game info (i.e. team colors, avatars) are not
        # set, set them up.
        if self.is_valid is True and self.game.team_colors is None:
            self.game.set_team_colors(self)
            if self.game_type != OW.GAMETYPE_1ST:
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
        avatars_left_ref_observed = {}
        avatars_left_ref = {}
        avatars_right_ref_observed = {}
        avatars_right_ref = {}

        # Create background image with team color
        bg_image_left = ImageUtils.create_bg_image(
            team_colors[OW.LEFT], OW.AVATAR_WIDTH_REF[self.game_type][self.game_version],
            OW.AVATAR_HEIGHT_REF[self.game_type][self.game_version])
        bg_image_right = ImageUtils.create_bg_image(
            team_colors[OW.RIGHT], OW.AVATAR_WIDTH_REF[self.game_type][self.game_version], 
            OW.AVATAR_HEIGHT_REF[self.game_type][self.game_version])
        avatars_ref_observed = OW.get_avatars_ref_observed(self.game_type, self.game_version)

        # Overlay transparent reference avatar on background
        for (name, avatar_ref_observed) in avatars_ref_observed.items():
            avatars_left_ref_observed[name] = ImageUtils.overlay(
                bg_image_left, avatar_ref_observed)
            avatars_left_ref[name] = ImageUtils.resize(
                avatars_left_ref_observed[name], 33, 26)
            avatars_right_ref_observed[name] = ImageUtils.overlay(
                bg_image_right, avatar_ref_observed)
            avatars_right_ref[name] = ImageUtils.resize(
                avatars_right_ref_observed[name], 33, 26)

        return {
            "left_observed": avatars_left_ref_observed,
            "left": avatars_left_ref,
            "right_observed": avatars_right_ref_observed,
            "right": avatars_right_ref
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
                "observed": all_avatars['left_observed'],
                "normal": all_avatars['left']
            }
        return {
            "observed": all_avatars['right_observed'],
            "normal": all_avatars['right']
        }

    def dict(self):
        d = {
            'time': self.time,
            'killfeeds': [killfeed.dict() for killfeed in self.killfeeds]
        }
        if self.game_type != OW.GAMETYPE_1ST:
            d['players'] = [player.dict() for player in self.players]
        return d
