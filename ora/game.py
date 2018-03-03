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
                     [
                         None,  # Left team
                         None   # Right team
                     ]
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
        self.team_names = [None, None]
        self.name_players = [None, None, None, None, None, None, None, None, None, None, None, None]
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
            self.team_names[0] = gui_info["name_team_left"]
        else:
            self.team_names[0] = ["Team Left"]

        if gui_info["name_team_right"]:
            self.team_names[1] = gui_info["name_team_right"]
        else:
            self.team_names[1] = ["Team Right"]

        if len(gui_info["name_players_team_left"]) == 6:
            self.name_players[0:6] = gui_info["name_players_team_left"]
        else:
            self.name_players[0:6] = ["1", "2", "3", "4", "5", "6"]

        if len(gui_info["name_players_team_right"]) == 6:
            self.name_players[6:12] = gui_info["name_players_team_right"]
        else:
            self.name_players[6:12] = ["7", "8", "9", "10", "11", "12"]

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
            players_list: a 2-D list of all (potentially) correct idents of
                players in each frame.
        """
        self._clear_frames()

        players_list = self._get_players_list()
        # 1) 1st rematching
        self._clean_chara_switching(players_list)
        self._rematch_killfeeds(players_list, False)
        self._reset_death_status(players_list, self.frames)
        self._freeze_death_status(players_list)

        # 2) 2nd rematching
        self._rematch_killfeeds(players_list, True)

        for ind_frame, players in enumerate(players_list):
            self.frames[ind_frame].players = players

        # 3) 3rd rematching
        self._clean_chara_switching(players_list)
        self._freeze_death_status(players_list)
        self._correct_dva_status(players_list, self.frames)
        self._correct_ult_charge(players_list)
        self._clean_chara_switching(players_list)

        for ind_frame, players in enumerate(players_list):
            self.frames[ind_frame].players = players

        # for frame in self.frames:
        #     player = frame.players[10]
        #     print(frame.time)
        #     print(player.chara)
        #     print(player.is_dead)
        #     print("==========")

        # for frame in self.frames:
        #     print(frame.time)
        #     for kf in frame.killfeeds:
        #         print(kf.player1)
        #         print(kf.player2)
        #     print("==========")

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

    def _get_players_list(self):
        players_list = []
        for frame in self.frames:
            players = frame.players
            players_list.append(players)
        return players_list

    def _clean_chara_switching(self, players_list):
        """ Remove invalid chara switch events.

        1) Remove weird "chara switch" events. If identification res in one
        frame differs with its prev & next frames, temporarily we identify it
        as invalid chara switch event.

        Here we do not override original players for a good reason. Our
        postprocess might be inaccurate, thus it's only for reference.

        Author: KomorebiL, Appcell

        Args:
            players_list: a 2-D list of all (potentially) correct idents of
                players in each frame.

        Returns:
            None
        """
        for ind in range(1, len(players_list) - 1):
            for ind_player in range(12):
                if players_list[ind - 1][ind_player].chara == players_list[ind + 1][ind_player].chara:
                    players_list[ind][ind_player].chara = players_list[ind - 1][ind_player].chara

    def _freeze_death_status(self, players_list):
        """ Freeze player status when chara is dead

        When a chara dies, override his current chara/ult charge etc. with
        status from previous frame. For now, ult charge relies on 
        player.is_dead too much so we just leave it be.
        In other words, we freeze the player when he dies.

        Here we do not override original players for a good reason. Our
        postprocess might be inaccurate, thus it's only for reference.

        Author: KomorebiL, Appcell

        Args:
            players_list: a 2-D list of all (potentially) correct idents of
                players in each frame.

        Returns:
            None
        """
        for ind, players in enumerate(players_list):
            if ind > 0:
                for ind_player, player in enumerate(players):
                    if player.is_dead:
                        players_list[ind][ind_player] = copy.copy(players_list[ind-1][ind_player])

    def _rematch_killfeeds(self, players_list, is_death_validated):
        """ Rematch charas in killfeeds with charas in players
        
        For all killfeeds without a proper player name recognition, we fill in
        all the blanks here. Still, we do not write this into original results
        for a reason.

        Author: KomorebiL, Appcell

        Args:
            players_list: a 2-D list of all (potentially) correct idents of
                players in each frame.

        Returns:
            killfeeds_ref: a 2-D list of all (potentially) correct idents of
                killfeeds in each frame.
        """
        for ind_frame, frame in enumerate(self.frames):
            for killfeed in frame.killfeeds:
                if killfeed.player1['chara'] != "empty":
                    killfeed.player1['player'] = self._get_player(
                        killfeed.player1, players_list, ind_frame, is_death_validated)
                killfeed.player2['player'] = self._get_player(
                    killfeed.player2, players_list, ind_frame, is_death_validated)
                for assist in killfeed.assists:
                    assist['player'] = self._get_player(
                        assist, players_list, ind_frame, is_death_validated)

    def _get_player(self, data, players_list, ind_frame, is_death_validated):
        """ Rematch player in kf with player in topbar

        Author: KomorebiL, Appcell

        Args:
            None

        Returns:
            name of the player matched
        """
        ind = ind_frame
        while ind >= 0:
            players = players_list[ind]
            for player in players:
                if data['team'] == 0:
                    if is_death_validated:
                        if OW.get_chara_name(data['chara']) == player.chara \
                        and player.is_dead is False and player.index < 6:
                            return player.index
                    else:
                        if OW.get_chara_name(data['chara']) == player.chara and player.index < 6:
                            return player.index
                elif data['team'] == 1:
                    if is_death_validated:
                        if OW.get_chara_name(data['chara']) == player.chara \
                        and player.is_dead is False and player.index >= 6:
                            return player.index
                    else:
                        if OW.get_chara_name(data['chara']) == player.chara and player.index >= 6:
                            return player.index
                else:
                    return -1
            ind = ind - 1
        return -1

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
            for killfeed in frame.killfeeds:
                if killfeed.player2['player'] != -1:
                    respawn_frame_num = OW.MIN_RESPAWN_TIME * self.analyzer_fps
                    if killfeed.player1['chara'] == "mercy" \
                    and killfeed.player1['team'] == killfeed.player2['team']:
                        for ind_frame_tmp in range(
                                ind_frame, 
                                ind_frame + min(respawn_frame_num, len(frames) - ind_frame)):
                            players_list[ind_frame_tmp][killfeed.player2['player']].is_dead = False
                    elif killfeed.player2['player'] != -1:
                        for ind_frame_tmp in range(
                                ind_frame - 1, 
                                ind_frame + min(respawn_frame_num, len(frames) - ind_frame)):
                            players_list[ind_frame_tmp][killfeed.player2['player']].is_dead = True

    def _correct_ult_charge(self, players_list):
        """ Postprocess player ult charge.
        
        In general, ult charge goes down when:
        1) ult ability is used
        2) player switches chara
        3) For D.Va it's a bit more complicated -- a player with his
        meka down can always go back to spawn room and get his meka again by
        switching chara. In this case, theoretically we should sense a chara
        switching event, thus it's usually same as condition 2). But what if
        that chara switching event isn't detected? Buh-oh. However when a
        player does this, it's only for when he has a mini-D.Va (i.e. with a
        meka down event beforehand). Since now we don't have D.Va status
        detector, we leave this one for later.

        Author: Appcell

        Args:
            players_list: a 2-D list of all (potentially) correct idents of
                players in each frame, should be ouput of 1st rematching.

        Returns:
            None
        """
        searched_frame_num = OW.MIN_SEARCH_TIME_FRAME * self.analyzer_fps

        # Remove unnatually large charge percentages
        players_list_len = len(players_list)
        for ind_frame in range(1, players_list_len - 1):
            for ind in range(12):
                # print(players_list[ind_frame - 1][ind])
                if players_list[ind_frame][ind].ult_charge \
                > players_list[ind_frame - 1][ind].ult_charge \
                and players_list[ind_frame][ind].ult_charge \
                > players_list[ind_frame + 1][ind].ult_charge:
                    players_list[ind_frame][ind].ult_charge \
                        = players_list[ind_frame + 1][ind].ult_charge

        for ind_frame in range(1, players_list_len - 1):
            for ind in range(12):
                if players_list[ind_frame][ind].ult_charge \
                < players_list[ind_frame - 1][ind].ult_charge:
                    if ind_frame < searched_frame_num:
                        players_list[ind_frame][ind].ult_charge \
                            = players_list[ind_frame - 1][ind].ult_charge
                        continue
                    # 1) Is there an ult ability used?
                    flag_ult_used = False
                    for ind_frame_tmp in range(
                            ind_frame - searched_frame_num + 1, ind_frame + 1):
                        if players_list[ind_frame_tmp][ind].is_ult_ready is False\
                        and players_list[ind_frame_tmp - 1][ind].is_ult_ready is True:
                            flag_ult_used = True
                    # 2) Is there a chara switching event?
                    flag_player_switched = False
                    for ind_frame_tmp in range(
                            ind_frame - searched_frame_num + 1, ind_frame + 1):
                        if players_list[ind_frame_tmp][ind].chara \
                        != players_list[ind_frame_tmp - 1][ind].chara:
                            flag_player_switched = True
                    # 3) For D.Va, is there a status change?
                    flag_dva_status_change = False
                    if players_list[ind_frame_tmp][ind].chara == OW.DVA \
                    and players_list[ind_frame_tmp][ind].dva_status \
                    != players_list[ind_frame_tmp - 1][ind].dva_status:
                        flag_dva_status_change = True
                    if (flag_ult_used or flag_player_switched or flag_dva_status_change) is False:
                        players_list[ind_frame][ind].ult_charge \
                            = players_list[ind_frame - 1][ind].ult_charge

    def _correct_dva_status(self, players_list, frames):
        """ Tell if a D.Va is with meka or not.

        We assume this D.Va is with her MEKA at first. Then when we see a MEKA
        DOWN event, or when she uses her primary ult, she loses her meka.
        A mini-D.Va gets her meka when she dies, and when she uses her 2nd ult,
        also when she does chara switching. 
        For the last situation, since we cannot tell if she truly switched
        chara (it's too fast), it's dealt by ult charge detection. When player
        does this, his ult charge goes to 0.


        Author: Appcell

        Args:
            players_list: a 2-D list to be corrected of all idents of players 
                          in each frame

        Returns:
            None
        """
        for ind_frame in range(1, len(frames)):
            frame = frames[ind_frame]
            players = players_list[ind_frame]
            for ind_player in range(12):
                if players[ind_player].chara == OW.DVA:
                    # 1) detect MEKA DOWN event
                    flag_meka_down = False
                    for killfeed in frame.killfeeds:
                        if killfeed.player2['chara'] == OW.MEKA\
                        and killfeed.player2['team'] == players[ind_player].team:
                            flag_meka_down = True
                    # 2) detect ult usage
                    flag_ult_used = False
                    searched_frame_num = OW.MIN_SEARCH_TIME_FRAME * self.analyzer_fps
                    for ind_frame_tmp in range(
                            ind_frame - searched_frame_num + 1, ind_frame + 1):
                        if players_list[ind_frame_tmp][ind_player].is_ult_ready is False \
                        and players_list[ind_frame_tmp - 1][ind_player].is_ult_ready is True:
                            flag_ult_used = True
                    # 3) detect chara switching with ult charge changes
                    flag_chara_switched = False
                    if (players[ind_player].ult_charge <= 1 \
                        and players_list[ind_frame - 1][ind_player].ult_charge > 0 \
                        and players_list[ind_frame - 1][ind_player].dva_status \
                        == OW.IS_WITHOUT_MEKA) \
                    or (players_list[ind_frame - 1][ind_player].chara \
                        != players_list[ind_frame][ind_player].chara):
                        flag_chara_switched = True

                    # Changing chara to mini-D.Va
                    if (flag_meka_down or flag_ult_used) \
                    and players[ind_player].dva_status == OW.IS_WITH_MEKA:
                        for ind_frame_tmp in range(ind_frame, len(frames)):
                            players_list[ind_frame_tmp][ind_player].dva_status \
                            = OW.IS_WITHOUT_MEKA

                    # Changing chara to big-D.Va
                    if (flag_ult_used \
                    and players[ind_player].dva_status == OW.IS_WITHOUT_MEKA) \
                    or flag_chara_switched:
                        for ind_frame_tmp in range(ind_frame, len(frames)):
                            players_list[ind_frame_tmp][ind_player].dva_status\
                            = OW.IS_WITH_MEKA



