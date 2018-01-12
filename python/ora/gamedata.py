"""
@Author: Xiaochen (leavebody) Li 
"""


class GameData:
    """
    Holds the basic information of a game, and also contains all info retrieved from the video.
    """
    def __init__(self):
        #: The name of both team.
        self.name_team1 = None
        self.name_team2 = None
        #: The theme color of both team. In format [b,g,r] and each color is in [0,256).
        self.color_team1 = None
        self.color_team2 = None
        #: A list of all killfeed retrieved, in chronic sequence.
        self.killfeeds = []
        #: A list of all analyzed frames of the game. Frame step is 0.5 seconds.
        self.frames = []

    def set_team_name(self, team1, team2):
        """
        Set the name of both team in this game.
        @param team1: the name of the first (on the left) team.
        @param team2: the name of the second (on the right) team.
        @return: None
        """
        self.name_team1 = team1
        self.name_team2 = team2

    def get_last_killfeed(self):
        return self.killfeeds[-1] if len(self.killfeeds) > 0 else None

    def _add_killfeeds(self, new_killfeeds):
        """
        Append several killfeeds into existing killfeed list.
        @param new_killfeeds: A list of killfeeds.
        @return: None
        """
        self.killfeeds.extend(new_killfeeds)

    def add_frame(self, frame):
        self.frames.append(frame)
        self._add_killfeeds(frame.killfeeds)

    def set_ultimate_status(self):
        """
        After get all Frame, generate the ultimate event list.
        @return:
        """
        pass

    def to_excel(self):
        """
        Output the full event list to an excel file.
        @return:
        """
        pass
