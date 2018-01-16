import numpy as np
import overwatch as OW
from utils import image as ImageUtils
from player import Player
from killfeed import Killfeed


class Frame:
    """Class of a Frame object.

    Retrieves and stores all info captured in one frame.
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

        # If the frame itself is valid, i.e. during a match
        self.is_valid = True
        # List of Player instances in current frame, usually 12
        self.players = []
        # List of Killfeed instances in current frame, 6 at max
        self.killfeeds = []
        # Resize image to 720p
        self.image = ImageUtils.resize(frame_image, 1280, 720)
        self.time = frame_time
        self.game = game

        self.get_players()
        self.get_killfeeds()
        self.validate()

        # cv2.imshow('t',self.image)
        # cv2.waitKey(0)
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

    def get_players(self):
        """Get all players info in this frame.

        Author:
            Appcell

        Args:
            None

        Returns:
            None 
        """
        for i in range(0, 12):
            player = Player(i, self)
            self.players.append(player)

    def get_team_colors(self):
        """Get team colors in this frame.

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
                self.killfeeds.append(killfeed)
                # print killfeed.player1
                # print killfeed.player2
                # print killfeed.ability
                # print killfeed.assists
            else:
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

        # 
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
