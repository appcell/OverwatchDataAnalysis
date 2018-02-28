from . import overwatch as OW
from .frame import Frame
from .utils.video_loader import VideoLoader
from .excel import Excel
import os
import time
import copy
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
        is_test: if is in test mode. If true, analysis result would be
                 temporarily output to a .txt file.
        is_owl_version_setted: if game_type is OWL and OWL UI version is
                               detected
        owl_version: version of OWL game UI
        frames: list of all analyzed frames of the game
        avatars_ref: list of all topbar reference avatars fused
        killfeed_icons_ref: list of all killfeed reference icons
        assist_icons_ref: list of all killfeed reference assist icons
        ability_icons_ref: list of all killfeed reference ability icons
    """

    def __init__(self, game_type):
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
        self.analyzer_fps = OW.ANALYZER_FPS
        self.team_names = {"left": "", "right": ""}
        self.name_players_team_left = []
        self.name_players_team_right = []
        self.team_colors = None
        self.video_path = ""
        self.output_path = ""
        self.is_test = False
        self.is_game_version_set = False
        self.game_version = 0

        self.frames = []
        self.avatars_ref = {}
        self.killfeed_icons_ref = OW.get_killfeed_icons_ref(self.game_type, self.game_version)
        self.assist_icons_ref = OW.get_assist_icons_ref(self.game_type, self.game_version)
        self.ability_icons_ref = OW.get_ability_icons_ref(self.game_type, self.game_version)
        self.ult_charge_numbers_ref = OW.get_ult_charge_numbers_ref(self.game_type, self.game_version)
        self.replay_icon_ref = OW.get_replay_icon_ref(self.game_type, self.game_version)

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

        self.analyzer_fps = gui_info["fps"]
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
            start_time: timestamp since when the analysis starts
            end_time: timestamp till when the analysis ends
            is_test: tell if the Game instance is in test mode

        Returns:
            None 
        """
        video = VideoLoader(self.video_path)
        step = int(round(video.fps/self.analyzer_fps))
        step_cnt = 0
        self.is_test = is_test
        is_full_video = True if (start_time == end_time and end_time == 0) \
                        else False
        # For a video clip we specify start/end time.
        # But for a full video we don't.
        time1 = time.time()
        start_time = start_time if is_full_video is False else 0
        frame_image_index = start_time * video.fps 
        frame_image = video.get_frame_image(frame_image_index)
        while frame_image is not None \
            and (frame_image_index < video.frame_number and is_full_video is True) \
            or (frame_image_index < end_time * video.fps and is_full_video is False):
            frame = []
            time1 = time.time()
            if self.is_game_version_set:
                frame = Frame(frame_image,
                              start_time +
                              (1 / float(self.analyzer_fps)) * step_cnt,
                              self, self.game_version)
            else:
                frame = self._set_game_version(
                    frame_image,
                    start_time +(1 / float(self.analyzer_fps)) * step_cnt)
            self.frames.append(frame)
            time2 = time.time() - time1
            frame_image_index += step
            step_cnt += 1
            frame_image = video.get_frame_image(frame_image_index)
        video.close()
        self.postprocess()
        self.output_to_excel()

    def _set_game_version(self, frame_image, frame_time):
        for i in range(OW.VERSION_NUM[self.game_type]):
            test_frame = Frame(
                frame_image,
                frame_time,
                self, i)
            if test_frame.is_valid:
                self.is_game_version_set = True
                self.game_version = i
                print("Game version is set as:")
                print(i)
                return test_frame
        

    def output_to_excel(self):
        """Output the full event list to an Excel file.

        Author: KomorebiL

        Args:
            None

        Returns:
            None 
        """
        Excel(self).save()

    def postprocess(self):
        """ Postprocess player & killfeeds, remove incorrect info.
        
        Here why don't we directly override frame.players, but get a returned
        list of players in every frame instead? The 1st postprocess of players
        might be inaccurate, and overriding will cause loss of original info.
        However for killfeeds it's another story -- we consider killfeed chara
        identification as absolutely correct for now, and other info in kf
        (e.g. player name, team name etc) are temporarily inaccurate. It's
        totally fine to override killfeed info apart from chara name.

        Author: KomorebiL, Appcell

        Args:
            None

        Returns:
            players_ref: a 2-D list of all (potentially) correct idents of
                players in each frame.
        """
        self._clear_frames()

        # 1) 1st rematching
        players_ref = self._postprocess_players()
        self._rematch_killfeeds(players_ref)

        # 2) 2nd rematching
        self._reset_death_status(players_ref, self.frames)
        self._rematch_killfeeds(players_ref)

        for ind_frame, players in enumerate(players_ref):
            self.frames[ind_frame].players = players

        # 3) 3rd rematching
        players_ref_2 = self._postprocess_players()
        for ind_frame, players in enumerate(players_ref):
            self.frames[ind_frame].players = players        

    def _clear_frames(self):
        """Remove invalid frames & repeated killfeeds.

        1) Remove repeated killfeeds: for each 2 neighboring frames, if both 
        have recognized killfeeds, then the last of previous frame and first
        of current frame must be the same, i.e. repeated. Remove repeated ones
        from last frame to the first.

        2) For replay: Usually there's a gap of ~1s between replay effect and
        replay icon appears. Mark frames during this gap as invalid.

        3) Remove invalid frames.

        Author: Appcell

        Args:
            None

        Returns:
            None 
        """
        # 1) Remove repeated killfeeds.
        # TODO: There must be a better way for this.
        frame_num = len(self.frames)
        for i in range(frame_num - 1, 0, -1):
            frame = self.frames[i]
            prev_frame = self.frames[i - 1]
            if frame.killfeeds and prev_frame.killfeeds \
                    and frame.killfeeds[0] == prev_frame.killfeeds[-1]:
                frame.killfeeds.pop(0)
            frame_before_effect_ind = int(i - (OW.FRAME_VALIDATION_EFFECT_TIME[
                self.game_type][self.game_version] * self.analyzer_fps) - 1)

            if frame_before_effect_ind >= 0:
                frame_before_effect = self.frames[frame_before_effect_ind]
                if (not frame_before_effect.is_valid) and not frame.is_valid:
                    for j in range(frame_before_effect_ind, i):
                        self.frames[j].is_valid = False


        # 2) Remove invalid frames
        self.frames = list(filter(
            lambda frame: frame.is_valid is True,
            self.frames))

    def _postprocess_players(self):
        """ Postprocess player status and remove outliers.
        
        1) When a chara dies, override his current chara/ult charge etc. with
        status from previous frame. For now, ult charge relies on 
        player.is_dead too much so we just leave it be.
        In other words, we freeze the player when he dies.

        2) Remove weird "chara switch" events. If identification res in one
        frame differs with its prev & next frames, temporarily we identify it
        as invalid chara switch event.

        Here we do not override original players for a good reason. Our
        postprocess might be inaccurate, thus it's only for reference.

        Author: KomorebiL, Appcell

        Args:
            None

        Returns:
            players_ref: a 2-D list of all (potentially) correct idents of
                players in each frame.
        """
        # 1) Freeze player status when chara is dead
        players_ref = [self.frames[0].players]
        for ind_frame in range(1, len(self.frames)):
            frame = self.frames[ind_frame]
            temp_players = []
            for ind_player, player in enumerate(frame.players):
                if player.is_dead:
                    temp_players.append(copy.copy(players_ref[ind_frame - 1][ind_player]))
                else:
                    temp_players.append(copy.copy(player))
            players_ref.append(temp_players)

        # 2) Remove invalid chara switch events
        for ind in range(1, len(players_ref) - 1):
            for ind_player in range(12):
                if players_ref[ind - 1][ind_player] == players_ref[ind + 1][ind_player]:
                    players_ref[ind][ind_player] = copy.copy(players_ref[ind - 1][ind_player])

        return players_ref

    def _rematch_killfeeds(self, players_ref):
        """ Rematch charas in killfeeds with charas in players
        
        For all killfeeds without a proper player name recognition, we fill in
        all the blanks here. Still, we do not write this into original results
        for a reason.

        Author: KomorebiL, Appcell

        Args:
            None

        Returns:
            killfeeds_ref: a 2-D list of all (potentially) correct idents of
                killfeeds in each frame.
        """
        for ind_frame, frame in enumerate(self.frames):
            for killfeed in frame.killfeeds:
                if killfeed.player1['player'] == "empty":
                    killfeed.player1['player'] = self._get_player_name(
                        killfeed.player1, players_ref, ind_frame)
                if killfeed.player2['player'] == "empty":
                    killfeed.player2['player'] = self._get_player_name(
                        killfeed.player2, players_ref, ind_frame)
                for assist in killfeed.assists:
                    if assist['player'] == "empty":
                        assist['player'] = self._get_player_name(
                            assist, players_ref, ind_frame)

    def _get_player_name(self, data, players_ref, ind_frame):
        """ Rematch player in kf with player in topbar

        Author: KomorebiL, Appcell

        Args:
            None

        Returns:
            name of the player matched
        """
        ind = ind_frame
        while ind >= 0:
            players = players_ref[ind]
            for player in players:
                if data['chara'] == player.chara and player.is_dead == False:
                    return player.name
            ind = ind - 1
        return "empty"

    def _reset_death_status(self, players_list, frames):
        """ When a player is killed/resurrected in killfeed, set his/her death state.

        Author: Appcell

        Args:
            players_list: a 2-D list of all (potentially) correct idents of
                players in each frame, should be ouput of 1st rematching.
            frames: list of all frames

        Returns:
            None
        """
        for ind_frame, frame in enumerate(frames):
            for kf in frame.killfeeds:
                if kf.player2['player'] != "empty":
                    respawn_frame_num = OW.MIN_RESPAWN_TIME * self.analyzer_fps
                    if kf.player1['chara'] == "mercy" and kf.player1['team'] == kf.player2['team']:
                        for i in range(min(respawn_frame_num, len(frames) - ind_frame)):
                            players_list[ind_frame + i][kf.player2['player']].is_dead = False
                    elif kf.player2['player'] != -1:
                        for i in range(min(respawn_frame_num, len(frames) - ind_frame)):
                            players_list[ind_frame + i][kf.player2['player']].is_dead = True

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
