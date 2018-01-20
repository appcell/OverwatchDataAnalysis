import overwatch as OW
from frame import Frame
from utils.video_loader import VideoLoader
from excel import Excel
import os
import cv2


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
        self.replay_icon_ref = OW.get_replay_icon_ref()[self.game_type]

    def set_team_colors(self, frame):
        """Set theme colors of both team in this game, using one frame.

        Author:
            Appcell

        Args:
            frame: from which colors are retrieved.

        Returns:
            None 
        """
        self.team_colors = frame.get_team_colors_from_image()

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
        filename = os.path.split(gui_info["video_path"])[1]
        self.video_path = gui_info["video_path"]
        self.output_path = gui_info["output_path"] \
            + '/' \
            + filename[:filename.index('.')] + '.xlsx'

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

    def analyze(self, start_time=0, end_time=0, is_test=False):
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
        step_cnt = 0

        # For testing we specify start/end time.
        # But for release version we don't.
        frame_image_index = start_time * video.fps if is_test else 0
        frame_image = video.get_frame_image(frame_image_index)
        while frame_image is not None \
            and (frame_image_index < video.frame_number and is_test is False) \
            or (frame_image_index < end_time * video.fps and is_test is True):

            frame = Frame(frame_image,
                          start_time +
                          (1 / float(self.analyzer_fps)) * step_cnt,
                          self)
            self.frames.append(frame)
            frame_image_index += step
            step_cnt += 1
            frame_image = video.get_frame_image(frame_image_index)

        video.close()
        self.clear_all_frames()
        self.output_to_excel()

        # for frame in self.frames:
        #     print frame.time
        #     for killfeed in frame.killfeeds:
        #         print "Player1: " + str(killfeed.player1)
        #         print "Player2: " + str(killfeed.player2)
        #         print "Ability: " + str(killfeed.ability)
        #         print "Assists: " + str(killfeed.assists)
        #         print "Is headshot: " + str(killfeed.is_headshot)

    def output_to_excel(self):
        """Output the full event list to an Excel file.

        Author: KomorebiL

        Args:
            None

        Returns:
            None 
        """
        Excel(self).save()

    def clear_all_frames(self):
        """Remove invalid frames & repeated killfeeds.

        1) Remove repeated killfeeds: for each 2 neighboring frames, if both 
        have recognized killfeeds, then the last of previous frame and first
        of current frame must be the same, i.e. repeated. Remove repeated ones
        from last frame to the first.

        2) For replay: Usually there's a gap of ~1s between replay effect and
        replay icon appears. Mark frames during this gap as invalid.

        3) Remove invalid frames.

        Args:
            None

        Returns:
            None 
        """

        # 1) Remove repeated killfeeds.
        # TODO: There must be a better way for this.
        frame_num = len(self.frames)
        for i in range(frame_num-1, 0, -1):
            frame = self.frames[i]
            prev_frame = self.frames[i - 1]
            if frame.killfeeds and prev_frame.killfeeds \
                    and frame.killfeeds[0] == prev_frame.killfeeds[-1]:
                frame.killfeeds.pop(0)
            frame_before_effect_ind = int(i - (OW.FRAME_VALIDATION_EFFECT_TIME[
                self.game_type] / self.analyzer_fps))
            if frame_before_effect_ind >= 0:
                frame_before_effect = self.frames[frame_before_effect_ind]
                if (not frame_before_effect.is_valid) and not frame.is_valid:
                    for j in range(frame_before_effect_ind, i):
                        self.frames[j].is_valid = False

        # 2) Remove invalid frames
        self.frames = list(filter(
            lambda frame: frame.is_valid is True,
            self.frames))

    def rematch_charas_and_players(self):
        """Rematch charas & players for killfeed

        Sometimes in a killfeed, chara gets recognized but there's no
        corresponding player info. Here we match them together with info from
        earlier & later frames so that no "empty" shows up in player names.

        Args:
            None

        Returns:
            None 
        """
        pass
