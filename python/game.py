import overwatch as OW
from frame import Frame
from utils.video_loader import VideoLoader


class Game(object):
    """Class of a Game object.

    Contains meta info of a game, also all info retrieved from video.

    Attributes:
        game_type: type of this game, can be OW.CAMETYPE_OWL or
            OW.GAMETYPE_CUSTOM
        analyzer_fps: FPS of game analyzer, usually 2 for OWL video
        team_names: names of both teams
        name_players_team_left: names of players in left team
        name_players_team_right: names of players in right team
        team_colors: theme color of both teams. In form of:
                     {
                         "left": None,
                         "right": None
                     }
        video_path: video path
        output_path: output path
        frames: list of all analyzed frames of the game
        avatars_ref: list of all topbar reference avatars fused
        killfeed_icons_ref: list of all killfeed reference icons
        assist_icons_ref: list of all killfeed reference assist icons
        ability_icons_ref: list of all killfeed reference ability icons
    """

    def __init__(self, game_type, analyzer_fps):
        """Initialize a Game object.

        Author:
            Appcell

        Args:
            game_type: type of the game, can be OW.GAMETYPE_OWL 
                or OW.GAMETYPE_CUSTOM 
            analyzer_fps: at what fps this video is analyzed. Usually 2 
                for OWL.

        Returns:
            None 
        """
        self.game_type = game_type
        self.analyzer_fps = analyzer_fps
        self.team_names = {"left": "", "right": ""}
        self.name_players_team_left = []
        self.name_players_team_right = []
        self.team_colors = None
        self.video_path = ""
        self.output_path = ""
        self.frames = []
        self.avatars_ref = {}
        self.killfeed_icons_ref = OW.get_killfeed_icons_ref()[self.game_type]
        self.assist_icons_ref = OW.get_assist_icons_ref()[self.game_type]
        self.ability_icons_ref = OW.get_ability_icons_ref()[self.game_type]

    def set_team_colors(self, frame):
        """Set theme colors of both team in this game, using one frame.

        Author:
            Appcell

        Args:
            frame: from which colors are retrieved.

        Returns:
            None 
        """
        self.team_colors = frame.get_team_colors()

    def set_game_info(self, gui_info):
        """Set meta info of this game from user input

        Including I/O path and team/player names.

        Author:
            Appcell

        Args:
            gui_info: a dict of GUI inputs

        Returns:
            None 
        """
        self.video_path = gui_info["video_path"]
        self.output_path = gui_info["output_path"]

        if gui_info["name_team_left"]:
            self.team_names['left'] = gui_info["name_team_left"]
        else:
            self.team_names['left'] = ["Team Left"]

        if gui_info["name_team_right"]:
            self.team_names['right'] = gui_info["name_team_right"]
        else:
            self.team_names['right'] = ["Team Right"]

        if len(gui_info["name_players_team_left"]) == 6:
            self.name_players_team_left = gui_info["name_players_team_left"]
        else:
            self.name_players_team_left = ["1", "2", "3", "4", "5", "6"]

        if len(gui_info["name_players_team_right"]) == 6:
            self.name_players_team_right = gui_info["name_players_team_right"]
        else:
            self.name_players_team_right = ["7", "8", "9", "10", "11", "12"]

    def analyze(self):
        """Main analysis process

        Capture frames with given video, retrieve info from each frame. All 
        retrieved info in one frame is stored in a Frame object, then the 
        Frame obj is pushed into array: self.frames

        Author:
            Appcell

        Args:
            None

        Returns:
            None 
        """
        video = VideoLoader(self.video_path)
        step = int(round(video.fps/self.analyzer_fps))
        start_time = 110
        end_time = 120
        frame_image_index = start_time * video.fps
        frame_image = video.get_frame_image(frame_image_index)

        while frame_image is not None and frame_image_index < end_time * video.fps:
            frame = Frame(frame_image,
                          start_time + (1 / self.analyzer_fps) * \
                          (frame_image_index - start_time * video.fps),
                          self)
            self.frames.append(frame)

            frame_image_index += step
            frame_image = video.get_frame_image(frame_image_index)
        video.close()

    def output_to_excel(self):
        """Output the full event list to an excel file.

        Args:
            None

        Returns:
            None 
        """
        pass
