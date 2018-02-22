from . import overwatch as OW
from .frame import Frame
from .utils.video_loader import VideoLoader
from .excel import Excel
import os
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

        # For OWL games only
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
        start_time = start_time if is_full_video is False else 0
        frame_image_index = start_time * video.fps 
        frame_image = video.get_frame_image(frame_image_index)
        while frame_image is not None \
            and (frame_image_index < video.frame_number and is_full_video is True) \
            or (frame_image_index < end_time * video.fps and is_full_video is False):
            frame = []
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
            frame_image_index += step
            step_cnt += 1
            frame_image = video.get_frame_image(frame_image_index)

        video.close()
        self.clear_all_frames()
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
                return test_frame
        
    def clear_all_frames(self):
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
        # for frame in self.frames:
        #     for kf in frame.killfeeds:
        #         print(kf.player1)
        #         print(kf.player2)
        #         print("***")
        #     print("=========")
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

    def output_to_excel(self):
        """Output the full event list to an Excel file.

        Author: KomorebiL

        Args:
            None

        Returns:
            None 
        """
        data = NewData(self).update()
        Excel(data).save()

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


class NewData:
    def __init__(self, game):
        self.game = copy.deepcopy(game)
        self.team_left = game.team_names['left']
        self.players = copy.copy(game.frames[0].players)

    def update(self):
        for idx, data in enumerate(self.game.frames):
            self._update_players(data.players, idx)
            self._update_killfeed(data.killfeeds, data.players, idx)
        return self.game

    def _update_players(self, players, index):
        """
        如果玩家阵亡，将他死之前的角色、大招能量覆盖到当前位置
        大招状态太依赖于 is_dead，所以先剥离出来
        换种说法，把玩家死之前的状态冻结。
        玩家存活的话就更新玩家的状态到 self.players
        """
        previous_players = (self.game.frames[0].players if index == 0
                            else self.game.frames[index - 1].players)
        next_players = (self.game.frames[-1].players if index >= len(self.game.frames) - 1
                        else self.game.frames[index + 1].players)
        for idx, player in enumerate(players):
            pre_player, next_player = previous_players[idx], next_players[idx]
            # if pre_player.is_dead and next_player.is_dead:
            #     player.is_dead = True

            if player.is_dead:
                player.chara = self.players[idx].chara
                player.ult_charge = self.players[idx].ult_charge
                player.is_ult_ready = self.players[idx].is_ult_ready
            else:
                if pre_player.chara == next_player.chara:
                    player.chara = pre_player.chara
                self.players[idx] = copy.copy(player)

    def _update_killfeed(self, killfeeds, players, index):
        """
        遍历 killfeed，填充缺失的玩家姓名。
        如果是天使，则修正爆头信息
        """
        for idx, killfeed in enumerate(killfeeds):
            killfeed.player1['player'] = self._get_player_name(killfeed.player1,
                                                               players,
                                                               self.players,
                                                               index,)
            killfeed.player2['player'] = self._get_player_name(killfeed.player2,
                                                               players,
                                                               self.players,
                                                               index,)
            if killfeed.player1['team'] == killfeed.player2['team']:
                if killfeed.player1['chara'] == 'mercy':
                    killfeed.is_headshot = False

            for assist in killfeed.assists:
                assist['player'] = self._get_player_name(assist,
                                                         players,
                                                         self.players,
                                                         index,
                                                         )

    def _get_player_name(self, player, current_player, previous_chara, index):
        """
        获取玩家姓名
        :param player: 当前玩家的信息(killfeed中的player1或player2)
        :param current_player: 包含了当前12个玩家信息的 list
        :param index: 当前帧的下标
        :return: player_name
        """
        if player['player'] != 'empty':
            return player['player']
        myslice = slice(0, 6) if player['team'] == self.team_left else slice(6, 12)
        players = current_player[myslice] + previous_chara[myslice]
        if index - 2 >= 0:
            players += self.game.frames[index - 2].players[myslice]
        for p in players:
            if p.chara == player['chara']:
                return p.name
        return 'empty'
