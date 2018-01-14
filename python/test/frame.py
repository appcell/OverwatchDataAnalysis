"""
@Author: Xiaochen (leavebody) Li 
"""
import cv2
import overwatch as OW
from utils import image as ImageUtils
from player import Player

class Frame:
    """
    Class of a Frame object, retrieves and stores all info captured in one frame.
    """
    def __init__(self, frame_image, frame_time, game):
        #: If the frame itself is valid, i.e. during a match
        self.is_valid = False
        
        self.players = []
        self.killfeeds = []
        self.image = ImageUtils.resize(frame_image, 1280, 720)  # Resize image to 720p.
        self.time = frame_time
        self.game = game
        # cv2.imshow("title", self.image)
        # cv2.waitKey(0)
        self.get_players()
        self.validate()

    def free(self):
        # free RAM by removing image
        del self.image

    def get_players(self):
        for i in range(0, 12):
            player = Player(i,self)
            self.players.append(player)

    def get_team_colors(self):
        pos = OW.get_team_color_pick_pos()[self.game.game_type]
        return {
        "color_team_left": self.image[pos[0][0], pos[0][1]],
        "color_team_right": self.image[pos[1][0], pos[1][1]]
        }

    def get_killfeed(self):
        pass

    def validate(self):
        self.is_valid = True

    def get_avatars_before_validation(self):
        team_colors = self.get_team_colors()
        avatars_left_ref = {}
        avatars_small_left_ref = {}
        avatars_right_ref = {}
        avatars_small_right_ref = {}

        # Create background image with team color
        bg_image_left = ImageUtils.create_bg_image(team_colors["color_team_left"], OW.AVATAR_WIDTH_REF, OW.AVATAR_HEIGHT_REF)
        bg_image_right = ImageUtils.create_bg_image(team_colors["color_team_right"], OW.AVATAR_WIDTH_REF, OW.AVATAR_HEIGHT_REF)
        avatars_ref = OW.get_avatars_ref()
   
        # Overlay transparent reference avatar on background
        for (name, avatar_ref) in avatars_ref.iteritems():
            avatars_left_ref[name] = ImageUtils.overlay(bg_image_left, avatar_ref)
            avatars_small_left_ref[name] = ImageUtils.resize(ImageUtils.overlay(bg_image_left, avatar_ref), 33, 26)
            avatars_right_ref[name] = ImageUtils.overlay(bg_image_right, avatar_ref)
            avatars_small_right_ref[name] = ImageUtils.resize(ImageUtils.overlay(bg_image_right, avatar_ref), 33, 26)

        return {
            "left": avatars_left_ref,
            "left_small": avatars_small_left_ref,
            "right": avatars_right_ref,
            "right_small": avatars_small_right_ref
        }


    def get_avatars(self, index):
        all_avatars = {}

        if self.game.color_team_left is not None:
            bg_color = self.game.color_team_left \
                       if index < 6 else self.game.color_team_right
            all_avatars = self.game.avatars_ref
        else:
            team_colors = self.get_team_colors()
            bg_color = team_colors["color_team_left"] \
                       if index < 6 else team_colors["color_team_right"]
            all_avatars = self.get_avatars_before_validation()

        if index < 6:
            return {
            "normal": all_avatars['left'],
            "small": all_avatars['left_small']
            }
        else:
            return {
            "normal": all_avatars['right'],
            "small": all_avatars['right_small']
            }
