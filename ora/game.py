from . import overwatch as OW
from .frame import Frame
from .utils.video_loader import VideoLoader
from .excel import Excel
from json import dump
import os
import math as Math
import time
import copy
import cv2
import logging

class Game(object):
    """Class of a Game object.

    Contains meta info of a game, also all info retrieved from video.

    Attributes:
        game_type: type of this game, can be OW.CAMETYPE_OWL or
            OW.GAMETYPE_CUSTOM, OW.GAMETYPE_1ST
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
        self.json = False
        self.is_game_version_set = False
        self.game_version = 0

        self.frames = []
        self.avatars_ref = {}
        self.killfeed_icons_ref = OW.get_killfeed_icons_ref(self.game_type, self.game_version)
        self.assist_icons_ref = OW.get_assist_icons_ref(self.game_type, self.game_version)
        self.ability_icons_ref = OW.get_ability_icons_ref(self.game_type, self.game_version)
        self.ult_charge_numbers_ref = OW.get_ult_charge_numbers_ref(
            self.game_type, self.game_version)
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
        if self.game_type == OW.GAMETYPE_OWL:
            self.team_colors = frame.get_team_colors_from_image()
        elif self.game_type == OW.GAMETYPE_CUSTOM or self.game_type == OW.GAMETYPE_1ST:
            self.team_colors = OW.TEAM_COLORS_DEFAULT[self.game_type][self.game_version]

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
        current_time = time.time()
        video = VideoLoader(self.video_path)
        logging.debug('Loading video time: %d ms', (time.time() - current_time) * 1000)
        current_time = time.time()

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
        logging.debug('Loading get_frame_image time: %d ms', (time.time() - current_time) * 1000)
        current_time = time.time()

        while frame_image is not None \
            and (frame_image_index < video.frame_number and is_full_video is True) \
            or (frame_image_index < end_time * video.fps and is_full_video is False):
            frame = []
            if self.game_type == OW.GAMETYPE_1ST:
                frame = Frame(frame_image,
                              start_time +
                              (1 / float(self.analyzer_fps)) * step_cnt,
                              self, self.game_version, self.game_type)
            elif self.is_game_version_set:
                logging.debug('Analyzing frame with game version set.')
                frame = Frame(frame_image,
                              start_time +
                              (1 / float(self.analyzer_fps)) * step_cnt,
                              self, self.game_version)
            else:
                logging.debug('Analyzing frame without game version set.')
                frame = self._set_game_version(
                    frame_image,
                    start_time +(1 / float(self.analyzer_fps)) * step_cnt)
                if not frame:
                    logging.debug('Invalid frame.')

            if frame:
                self.frames.append(frame)

            frame_image_index += step
            step_cnt += 1
            logging.debug('Processing frame time: %d ms', (time.time() - current_time) * 1000)
            current_time = time.time()
            frame_image = video.get_frame_image(frame_image_index)
            logging.debug('get_frame_image time: %d ms', (time.time() - current_time) * 1000)
            current_time = time.time()

        video.close()
        logging.debug('Processing video time: %d ms', (time.time() - current_time) * 1000)
        current_time = time.time()
        if self.game_type != OW.GAMETYPE_1ST:
            self.postprocess()
            logging.debug('Post processing video time: %d ms', (time.time() - current_time) * 1000)
        current_time = time.time()

    def _set_game_version(self, frame_image, frame_time):
        for i in range(OW.VERSION_NUM[self.game_type]):
            test_frame = Frame(
                frame_image,
                frame_time,
                self, i)
            if test_frame.is_valid:
                self.is_game_version_set = True
                self.game_version = i
                print(f"Game version is set as: {i}")
                self.killfeed_icons_ref = OW.get_killfeed_icons_ref(self.game_type, self.game_version)
                self.assist_icons_ref = OW.get_assist_icons_ref(self.game_type, self.game_version)
                self.ability_icons_ref = OW.get_ability_icons_ref(self.game_type, self.game_version)
                self.ult_charge_numbers_ref = OW.get_ult_charge_numbers_ref(
                    self.game_type, self.game_version)
                self.replay_icon_ref = OW.get_replay_icon_ref(self.game_type, self.game_version)
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

    def output_to_json(self):
        """

        Author: KomorebiL

        Args:
            None

        Returns:
            None 
        """
        # 这是一个开关
        self.json = True
        if self.json:
            data = {
                'team_names': self.team_names,
                'players_name': self.name_players,
                'frames': [frame.dict() for frame in self.frames],
            }
            filename, _ = self.output_path.split('.')
            filename = '{}_{}.txt'.format(filename, 'game')
            with open(filename, 'w') as f:
                dump(data, f, ensure_ascii=False, indent=4)

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

        # 3) 3rd rematching
        self._clean_chara_switching(players_list)
        self._freeze_death_status(players_list)
        self._correct_dva_status(players_list, self.frames)
        self._correct_ult_charge(players_list)
        self._clean_chara_switching(players_list)
        self._clear_killfeeds(players_list)

        for ind_frame, players in enumerate(players_list):
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
        # For replays, remove also ~0.7s after
        frames_tmp = []
        after_effect_frames_num = Math.ceil(OW.FRAME_VALIDATION_EFFECT_AFTER_TIME[
                self.game_type][self.game_version] / (1 / self.analyzer_fps))
        for ind_frame, frame in enumerate(self.frames):
            if frame.is_valid is True:
                if ind_frame < after_effect_frames_num:
                    frames_tmp.append(frame)
                    continue
                was_in_replay = -1
                for ind_frame_tmp in range(ind_frame - after_effect_frames_num, ind_frame + 1):
                    if self.frames[ind_frame_tmp].is_replay is True:
                        was_in_replay = ind_frame_tmp
                        break
                if was_in_replay == -1:
                    frames_tmp.append(frame)
                    continue

        self.frames = frames_tmp

    def _clear_killfeeds(self, players_list):
        for ind_frame, frame in enumerate(self.frames):
            if ind_frame >= 2:
                for kf in frame.killfeeds:
                    # TODO: write 1.2 into ow.py!!!
                    if players_list[ind_frame - 2][kf.player2['player']].is_dead \
                    and not (kf.player1['chara'] == OW.MERCY \
                        and kf.player1['team'] == kf.player2['team']) \
                    and frame.time - self.frames[ind_frame - 2].time <= 1.2:
                        # if the player is already dead, there's no need to kill him
                        kf.is_valid = False
                frame.killfeeds = [kf for kf in frame.killfeeds if kf.is_valid is True]

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
                if not players_list[ind - 1][ind_player] or not players_list[ind + 1][ind_player]:
                    return
                if players_list[ind - 1][ind_player].chara \
                == players_list[ind + 1][ind_player].chara:
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
                        players_list[ind][ind_player].is_dead = True

    def _rematch_killfeeds(self, players_list, is_death_validated):
        """ Rematch charas in killfeeds with charas in players
        
        For all killfeeds without a proper player name recognition, we fill in
        all the blanks here. Still, we do not write this into original results
        for a reason.
        
        This might bring errors if there's a kill event in the first frame. We
        skip the first frame instead.

        Author: KomorebiL, Appcell

        Args:
            players_list: a 2-D list of all (potentially) correct idents of
                players in each frame.

        Returns:
            killfeeds_ref: a 2-D list of all (potentially) correct idents of
                killfeeds in each frame.
        """
        for ind_frame, frame in enumerate(self.frames):
            if ind_frame > 0:
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
        # First make sure everyone is set as alive
        for players in players_list:
            for player in players:
                player.is_dead = False

        for ind_frame, frame in enumerate(frames):
            for killfeed in frame.killfeeds:
                if killfeed.player2['player'] != -1:
                    if killfeed.player1['chara'] == "mercy" \
                    and killfeed.player1['team'] == killfeed.player2['team']:
                        if players_list[ind_frame][killfeed.player2['player']].is_dead is True:
                            self._set_status_as_alive_after(
                                    players_list, frames, ind_frame, killfeed.player2['player'])
                    elif killfeed.player2['player'] != -1 \
                    and killfeed.player2['chara'] in OW.CHARACTER_LIST \
                    and players_list[ind_frame][killfeed.player2['player']].is_dead is not True:
                        # Here sometimes due to replay etc, killfeed is not reliable. Thus we have
                        # to determine based on common sense, i.e. without resurrection, deaths of
                        # same chara must not have a time gap of more than 10s.
                        last_death_frame_ind = -1
                        for ind_frame_tmp in range(ind_frame, 0, -1):
                            if players_list[ind_frame_tmp][
                                    killfeed.player2['player']].is_dead is True:
                                last_death_frame_ind = ind_frame_tmp
                                break
                        
                        if last_death_frame_ind != -1 \
                            and last_death_frame_ind < ind_frame\
                            and frames[ind_frame].time - frames[last_death_frame_ind].time \
                            < OW.MIN_RESPAWN_TIME:
                            # Death time gap is too small, find if there's any resurrection
                            last_resurrection_frame_ind = -1
                            for ind_frame_tmp in range(
                                    ind_frame, last_death_frame_ind, -1):
                                for killfeed_tmp in frames[ind_frame_tmp].killfeeds:
                                    if killfeed_tmp.player2['player'] == killfeed.player2['player']\
                                    and killfeed_tmp.player1['chara'] == OW.MERCY\
                                    and killfeed_tmp.player1['team'] == killfeed.player2['team']:
                                        last_resurrection_frame_ind = ind_frame_tmp
                                        break
                            if last_resurrection_frame_ind != -1:
                                self._set_status_as_dead_after(
                                    players_list, frames, ind_frame, killfeed.player2['player'])
                                continue
                        else:
                            self._set_status_as_dead_after(
                                players_list, frames, ind_frame, killfeed.player2['player'])
    
    def _set_status_as_alive_after(self, players_list, frames, ind_frame, player_ind):
        for ind_frame_tmp in range(
                ind_frame, 
                len(frames) - 1):
            players_list[ind_frame_tmp][player_ind].is_dead = False

    def _set_status_as_dead_after(self, players_list, frames, ind_frame, player_ind):
        ind_frame_tmp = ind_frame - 1
        if ind_frame == 0:
            ind_frame_tmp = 0
        elif frames[ind_frame].time - frames[ind_frame_tmp].time > 1 / self.analyzer_fps:
            ind_frame_tmp = ind_frame
        while ind_frame_tmp < len(frames) \
        and frames[ind_frame_tmp].time - frames[ind_frame].time \
        <= OW.MIN_RESPAWN_TIME:
            players_list[ind_frame_tmp][player_ind].is_dead = True
            ind_frame_tmp += 1

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
        However, as always, we preserve ult charge recog when charge == 100，
        since it's the only data sure to be accurate.

        Author: Appcell

        Args:
            players_list: a 2-D list of all (potentially) correct idents of
                players in each frame, should be ouput of 1st rematching.

        Returns:
            None
        """
        searched_frame_num = OW.MIN_SEARCH_TIME_FRAME * self.analyzer_fps
        players_list_len = len(players_list)

        # 1) Remove unnatually small charge nums
        for ind in range(12):
            for ind_frame in range(1, players_list_len - 1):
                if players_list[ind_frame][ind].ult_charge == 100:
                    continue
                # Special occasion: sometimes the analyzer doesn't capture
                # the frame where ult charge reaches 100, then player used
                # that ult immediately. In this case, we preserve original
                # recognition result, then add an artifical ult used event.
                if players_list[ind_frame][ind].ult_charge < 10 \
                and players_list[ind_frame - 1][ind].ult_charge > 95:
                    players_list[ind_frame - 1][ind].is_ult_ready = True
                    players_list[ind_frame][ind].is_ult_ready = False
                    continue
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
                            break
                    # 2) Is there a chara switching event?
                    flag_player_switched = False
                    for ind_frame_tmp in range(
                            ind_frame - searched_frame_num + 1, ind_frame + 1):
                        if players_list[ind_frame_tmp][ind].chara \
                        != players_list[ind_frame_tmp - 1][ind].chara:
                            flag_player_switched = True
                            break
                    # 3) For D.Va, is there a status change?
                    flag_dva_status_change = False
                    for ind_frame_tmp in range(
                            ind_frame - searched_frame_num + 1, 
                            min(players_list_len - 1, ind_frame + searched_frame_num)):
                        if players_list[ind_frame_tmp][ind].chara == OW.DVA \
                        and players_list[ind_frame_tmp][ind].dva_status \
                        != players_list[ind_frame_tmp - 1][ind].dva_status:
                            flag_dva_status_change = True
                            break
                    if (flag_ult_used or flag_player_switched or flag_dva_status_change) is False:
                        players_list[ind_frame][ind].ult_charge \
                            = players_list[ind_frame - 1][ind].ult_charge

        # 2) Remove unnatually large charge nums
        for ind in range(12):
            for ind_frame in range(1, players_list_len - 1):
                if players_list[ind_frame][ind].ult_charge == 100:
                    continue
                if players_list[ind_frame][ind].ult_charge \
                > players_list[ind_frame - 1][ind].ult_charge:
                    unnatural_frame_ind = ind_frame
                    while unnatural_frame_ind <= players_list_len - 1 \
                    and players_list[unnatural_frame_ind][ind].ult_charge != 100 \
                    and abs(players_list[unnatural_frame_ind][ind].ult_charge \
                        - players_list[ind_frame][ind].ult_charge) < 10:
                        unnatural_frame_ind = unnatural_frame_ind + 1
                    if unnatural_frame_ind <= players_list_len - 1 \
                    and unnatural_frame_ind - ind_frame < 5 \
                    and abs(players_list[unnatural_frame_ind][ind].ult_charge \
                        - players_list[ind_frame - 1][ind].ult_charge) < 15:
                        # 1) Is there an ult ability used?
                        flag_ult_used = False
                        for ind_frame_tmp in range(
                                ind_frame, unnatural_frame_ind):
                            if players_list[ind_frame_tmp][ind].is_ult_ready is False\
                            and players_list[ind_frame_tmp - 1][ind].is_ult_ready is True:
                                flag_ult_used = True
                                break
                        # 2) Is there a chara switching event?
                        flag_player_switched = False
                        for ind_frame_tmp in range(
                                ind_frame, unnatural_frame_ind):
                            if players_list[ind_frame_tmp][ind].chara \
                            != players_list[ind_frame_tmp - 1][ind].chara:
                                flag_player_switched = True
                                break
                        # 3) For D.Va, is there a status change?
                        flag_dva_status_change = False
                        for ind_frame_tmp in range(
                                ind_frame - searched_frame_num + 1, 
                                min(players_list_len - 1, ind_frame + searched_frame_num)):
                            if players_list[ind_frame_tmp][ind].chara == OW.DVA \
                            and players_list[ind_frame_tmp][ind].dva_status \
                            != players_list[ind_frame_tmp - 1][ind].dva_status:
                                flag_dva_status_change = True
                                break

                        if (flag_ult_used or flag_player_switched or flag_dva_status_change) is False:
                            for ind_frame_tmp in range(ind_frame, unnatural_frame_ind):
                                players_list[ind_frame_tmp][ind].ult_charge \
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
                        and killfeed.player2['player'] == ind_player:
                            flag_meka_down = True
                            break
                    # 2) detect ult usage
                    flag_ult_used = False
                    searched_frame_num = OW.MIN_SEARCH_TIME_FRAME * self.analyzer_fps
                    for ind_frame_tmp in range(
                            ind_frame - searched_frame_num + 1, ind_frame + 1):
                        if players_list[ind_frame_tmp][ind_player].is_ult_ready is False \
                        and players_list[ind_frame_tmp - 1][ind_player].is_ult_ready is True:
                            flag_ult_used = True
                            break

                    # 3) detect chara switching with ult charge changes
                    flag_chara_switched = False
                    if (players[ind_player].ult_charge <= 1 \
                        and players_list[ind_frame - 1][ind_player].ult_charge > 0 \
                        and players_list[ind_frame - 1][ind_player].dva_status \
                        == OW.IS_WITHOUT_MEKA) \
                    or (players_list[ind_frame - 1][ind_player].chara \
                        != players_list[ind_frame][ind_player].chara):
                        flag_chara_switched = True
                        break

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
                    if players[ind_player].dva_status == OW.IS_WITHOUT_MEKA \
                    and players[ind_player].is_ult_ready:
                        players[ind_player].is_ult_ready = False
                        players[ind_player].is_secondary_ult_ready = True