import overwatch as OW
from frame import Frame
from utils.video_loader import VideoLoader

class Game:
    """
    Contains meta info of a game, also all info retrieved from video.
    """
    def __init__(self, game_type, analyzer_fps):
        """
        Set the name of both team in this game.
        @Author: Leavebody, Appcell
        @param team_left: the name of the first (on the left) team.
        @param team_right: the name of the second (on the right) team.
        @return: None
        """
        #: Type of this game: 0 = OWL, 1 = Custom matches
        self.game_type = game_type

        #: FPS of game analyzer.
        self.analyzer_fps = analyzer_fps

        #: Names of both teams.
        self.name_team_left = ""
        self.name_team_right = ""

        self.team_names = {
        "left": "",
        "right": ""
        }

        #: Names of players in both teams.
        self.name_players_team_left = []
        self.name_players_team_right = []

        #: Theme color of both teams. In form of:
        # {
        #     "left": None,
        #     "right": None
        # }
        self.team_colors = None

        #: Video path & output path
        self.video_path = ""
        self.output_path = ""

        #: A list of all analyzed frames of the game.
        self.frames = []
        self.avatars_ref = {}

        # Read in killfeed & assist & ability icons
        self.killfeed_icons_ref = OW.get_killfeed_icons_ref()[self.game_type]
        self.assist_icons_ref = OW.get_assist_icons_ref()[self.game_type]
        self.ability_icons_ref = OW.get_ability_icons_ref()[self.game_type]

    def set_team_colors(self, frame):
        """
        Set theme colors of both team in this game, using one frame.
        @Author: Appcell
        @param frame: the frame from which team color data is extracted
        @return: None
        """
        colors = frame.get_team_colors()
        self.team_colors = colors

    def set_game_info(self, gui_info):
        """
        Set meta info of this game, including I/O path and team/player names.
        Data comes from GUI input.
        @Author: Appcell
        @param gui_info: a dict containing all info from GUI input
        @return: None
        """        
        self.video_path = gui_info["video_path"]
        self.output_path = gui_info["output_path"]
        self.team_names['left'] = gui_info["name_team_left"] \
                              if len(gui_info["name_team_left"]) > 0 \
                              else ["Team Left"]
        self.team_names['right'] = gui_info["name_team_right"] \
                               if len(gui_info["name_team_right"]) > 0 \
                               else ["Team Right"]
        self.name_players_team_left = gui_info["name_players_team_left"] \
                              if len(gui_info["name_players_team_left"]) == 6 \
                              else ["1", "2", "3", "4", "5", "6"]
        self.name_players_team_right = gui_info["name_players_team_right"] \
                               if len(gui_info["name_players_team_right"]) == 6 \
                               else ["7", "8", "9", "10", "11", "12"]

    def get_last_killfeed(self):
        return self.killfeeds[-1] if len(self.killfeeds) > 0 else None

    def analyze(self):
        """
        Main analyzing process, capture frames in video and retrieve info from each frame.
        All retrieved info in one frame is stored in a Frame object, then the Frame obj
            is pushed into array: self.frames
        @Author: Leavebody, Appcell
        @param None
        @return: None
        """
        video = VideoLoader(self.video_path)
        step = int(round(video.fps/self.analyzer_fps))
        start_time = 110
        end_time = 120
        frame_image_index = start_time * video.fps
        frame_image = video.get_frame_image(frame_image_index)

        while frame_image is not None and frame_image_index < end_time * video.fps:
            frame = Frame(frame_image, 
                          start_time + (1 / self.analyzer_fps) * frame_image_index, 
                          self)

            if frame.is_valid is True and self.team_colors is None:
                self.set_team_colors(frame)
                self.avatars_ref = frame.get_avatars_before_validation()

            frame.free()
            self.frames.append(frame)

            frame_image_index += step
            frame_image = video.get_frame_image(frame_image_index)
        video.close()

    def output_to_excel(self):
        """
        Output the full event list to an excel file.
        @return:
        """
        pass
