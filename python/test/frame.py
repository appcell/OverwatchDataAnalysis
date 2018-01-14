"""
@Author: Xiaochen (leavebody) Li 
"""
import cv2
import overwatch as OW
from utils import ImageUtils
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
        pass
