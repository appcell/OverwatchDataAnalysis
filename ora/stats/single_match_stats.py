# coding: utf-8
import os
import sys
import zipfile
import json
from copy import deepcopy
from statistics import mean
import ora.overwatch as OW

sys.path.append('../utils')
from utils import stats

def time_to_frame(time):
    pass


class PlayerStats:

    def __init__(self, index, frame_index = 0, tf_index = 0, prev_data = None):

        if prev_data != None:
            self = deepcopy(prev_data)
        else:
            self.num_charas_used = 0
            self.charas_list = []

            self.elims = 0
            self.deaths = 0
            self.resurrects = 0
            self.resurrected = 0
            self.ult_charge = 0

            self.tf_elims_list = [0]
            self.tf_deaths_list = [0]
            self.tf_elim_index_list = [0]
            self.tf_death_index_list = [0]
            self.avg_tf_elims = 0
            self.avg_tf_deaths = 0
            self.avg_tf_elim_index = 0
            self.avg_tf_death_index = 0

            self.first_elims = 0
            self.first_elimed = 0

            self.elims_per_10min = 0
            self.deaths_per_10min = 0
            self.dps_elims = 0
            self.elimed_by_dps = 0
            self.tank_elims = 0
            self.elimed_by_tank = 0
            self.healer_elims = 0
            self.elimed_by_healer = 0

            self.critical_elims = 0
            self.ratio_critical_elim = 0


        self.index = index
        self.tf_index = tf_index
        self.frame_index = frame_index
        self.prev_data = prev_data
        return

    def update(self):
        self._update_charas()
        self._update_elims()
        self._update_deaths()
        self._update_resurrects()
        self._update_resurrected()
        self._update_ult_charge()

        self._update_critical_elims()

        # 必须得在_update_elims和_update_critical_elims后面
        # 输出为%前的整数 不含%
        self._update_ratio_critical_elim()

        # 得在_update_elims后执行
        self._update_elims_per_10min()

        # 得在_update_deaths后执行
        self._update_deaths_per_10min()

        self._update_dps_elims()
        self._update_tank_elims()
        self._update_support_elims()
        self._update_elimed_by_dps()
        self._update_elimed_by_tank()
        self._update_elimed_by_support()

        self._update_tf()
        self._update_avg_tf_elims()
        self._update_avg_tf_deaths()
        self._update_avg_elim_index()
        self._update_avg_death_index()
        
    def _update_tf(self):
        if self.tf_index != self.prev_data.tf_index:
            self.tf_elims_list.append(0)
            self.tf_deaths_list.append(0)
            self.tf_elim_index_list.append(0)
            self.tf_death_index_list.append(0)

        flag_first_elim = False
        flag_first_death = False

        for event in EventsData[self.frame_index]:
            if event["action"] == "Eliminate" and event['subject']['player_ind'] == self.index:
                self.tf_elims_list[-1] += 1
                if tf_elim_index_list[-1] == 0:
                    flag_first_elim = True
            if event["action"] == "Eliminate" and event['object']['player_ind'] == self.index:
                self.tf_deaths_list[-1] += 1
                if tf_death_index_list[-1] == 0:
                    flag_first_elim = True

        # Go over previous frames, calculate team-wise elim/death index
        if flag_first_elim:
            total_team_tf_elim = 0
            starting_frame_ind = TeamfightStats.data[self.tf_index]["starting_frame"]
            if self.tf_index == len(TeamfightStats.data) - 1:
                ending_frame_ind = len(EventsData) - 1
            for frame_ind in range(starting_frame_ind, self.frame_index):
                frame = EventsData[frame_ind]
                for event in frame:
                    if event["action"] == "Eliminate" \
                    and ((event['subject']['player_ind'] < 6 and self.index < 6) \
                    or (event['subject']['player_ind'] >= 6 and self.index >= 6)):
                     total_team_tf_elim += 1
            self.tf_elim_index_list[-1] = total_team_tf_elim + 1

        if flag_first_death:
            total_team_tf_death = 0
            starting_frame_ind = TeamfightStats.data[self.tf_index]["starting_frame"]
            if self.tf_index == len(TeamfightStats.data) - 1:
                ending_frame_ind = len(EventsData) - 1
            for frame_ind in range(starting_frame_ind, self.frame_index):
                frame = EventsData[frame_ind]
                for event in frame:
                    if event["action"] == "Eliminate" \
                    and ((event['object']['player_ind'] < 6 and self.index < 6) \
                    or (event['oject']['player_ind'] >= 6 and self.index >= 6)):
                     total_team_tf_death += 1
            self.tf_death_index_list[-1] = total_team_tf_death + 1

    def _update_avg_tf_elims(self):
        return mean(self.tf_elims_list)

    def _update_avg_tf_deaths(self):
        return mean(self.tf_deaths_list)

    def _update_avg_elim_index(self):
        return mean(self.tf_elim_index_list)

    def _update_avg_death_index(self):
        return mean(self.tf_death_index_list)

    def _update_charas(self):
        curr_chara = FramesData[self.frame_index]["players"][self.index]["chara"]
        if num_charas_used > 0:
            if curr_chara != charas_list[-1]:
                charas_list.append(curr_chara)
                if ~(curr_chara in charas_list):
                    num_charas_used += 1
        else:
            num_charas_used += 1
            charas_list.append(curr_chara)

    def _update_elims(self):
        for event in EventsData[self.frame_index]:
            if event["action"] == "Eliminate" and event['subject']['player_ind'] == self.index:
                self.elims += 1

    def _update_deaths(self):
        for event in EventsData[self.frame_index]:
            if event["action"] == "Eliminate" and event['object']['player_ind'] == self.index:
                self.deaths += 1

    def _update_resurrects(self):
        for event in EventsData[self.frame_index]:
            if event["action"] == "Resurrect" and event['subject']['player_ind'] == self.index:
                self.resurrects += 1

    def _update_resurrected(self):
        for event in EventsData[self.frame_index]:
            if event["action"] == "Resurrect" and event['object']['player_ind'] == self.index:
                self.resurrected += 1

    def _update_ult_charge():
        self.ult_charge = FramesData[self.frame_index]["players"][self.index]["ult_charge"]

    def _update_critical_elims(self):
        for event in EventsData[self.frame_index]:
            if event["action"] == "Eliminate" and event['subject']['player_ind'] == self.index \
            and elim['critical kill'] == 'Y':
                self.critical_elims += 1

    def _update_ratio_critical_elim(self):
        self.ratio_critical_elim = self.critical_elims * 100 / self.elims

    def _update_elims_per_10min(self):
        self.elims_per_10min = self.elims * 10 * 60/self.time

    def _update_deaths_per_10min(self):
        self.deaths_per_10min = self.deaths * 10 * 60/self.time

    def _update_dps_elims(self):
        for event in EventsData[self.frame_index]:
            if event["action"] == "Eliminate" and event['subject']['player_ind'] == self.index\
                    and event['subject']['chara'] in OW.DPS_LIST:
                self.dps_elims += 1

    def _update_tank_elims(self):
        for event in EventsData[self.frame_index]:
            if event["action"] == "Eliminate" and event['subject']['player_ind'] == self.index\
                    and event['subject']['chara'] in OW.TANK_LIST:
                self.tank_elims += 1

    def _update_support_elims(self):
        for event in EventsData[self.frame_index]:
            if event["action"] == "Eliminate" and event['subject']['player_ind'] == self.index\
                    and event['subject']['chara'] in OW.SUPPORT_LIST:
                self.support_elims += 1

    def _update_elimed_by_dps(self):
        for event in EventsData[self.frame_index]:
            if event["action"] == "Eliminate" and event['object']['player_ind'] == self.index\
                    and event['subject']['chara'] in OW.DPS_LIST:
                self.elimed_by_dps += 1

    def _update_elimed_by_tank(self):
        for event in EventsData[self.frame_index]:
            if event["action"] == "Eliminate" and event['object']['player_ind'] == self.index\
                    and event['subject']['chara'] in OW.TANK_LIST:
                self.elimed_by_tank += 1

    def _update_elimed_by_support(self):
        for event in EventsData[self.frame_index]:
            if event["action"] == "Eliminate" and event['object']['player_ind'] == self.index\
                    and event['subject']['chara'] in OW.SUPPORT_LIST:
                self.elimed_by_healer += 1

class BasicStats:

    def __init__(self):
        self.first_elims = [0, 0] # [team1, team2]
        self.normal_elims = [0, 0]
        self.immediate_elims = [0, 0]
        self.ability_elims = [0, 0]
        self.ult_elims = [0, 0]

        self.first_elim_tf_win_ratio = [0, 0]
        self.player_with_most_first_elims = [0, 0]

        self.total_ults_used = 0
        self.total_ults_used_per_tf = 0
        self.global_avg_elims_per_ult = 0
        self.avg_elims_per_ult = [0, 0]

        self.player_with_most_elims = [0, 0, 0, 0] # [player_ind_of_team1, #_of_elims_of_team1, player_ind_of_team2, #_of_elims_of_team2]
        self.chara_with_most_elims = [0, 0, 0, 0] # [chara_ind_of_team1, #_of_elims_of_team1, chara_ind_of_team2, #_of_elims_of_team2]

        self.player_with_most_deaths = [0, 0, 0, 0]
        self.chara_with_most_deaths = [0, 0, 0, 0]

        self.player_with_least_deaths = [0, 0, 0, 0]
        self.chara_with_least_deaths = [0, 0, 0, 0]

        return

class SingleTeamFightStats:

    def __init__(self, start_time=0, end_time=0):
        self.start_time = start_time
        self.end_time = end_time
        self.turning_point = 0
        self.ults_used_per_team = [0, 0]
        self.ults_used_total = 0
        self.elims_list = []
        return

class TeamfightStats:

    def __init__(self):
        self.data = []
        return

    def _new_teamfight(self):
        self.data.append(SingleTeamFightStats())
        return


class FrameStats:
    def __init__(self, frame, last_frame_data=None):
        self.frame = frame
        if last_frame_data:
            self.last_frame_data = deepcopy(last_frame_data)
            self.players = self.last_frame_data['players']
            self.time = self.last_frame_data['time']
            return

        self.last_frame_data = None
        self.players = []
        for i in range(12):
            self.players.append(PlayerStats(i))

        self.basics = BasicStats()
        self.time = 0
        self.tf_index = 0 # index of current teamfight

    def _update_player(self, player):







class SingleMatchStats:
    """Class of a SingleMatchStats object.

    Retrieves and stores all stats listed in 
    competitive_stats_rating_list.xlsx.

    Attributes:
        data_metainfo: Raw data in metainfo.json in dict format
        data_frames: Raw data in frames.json in dict format
        data_sheet1: Raw data in data_sheet1.json in dict format
        data_sheet1: Raw data in data_sheet2.json in dict format
        data_sheet1: Raw data in data_sheet3.json in dict format
        elims: List of all eliminations in the game, with 'time' expressed in
               seconds, not in hh:mm:ss
        teamfight_separations: List of teamfight separation points
        teamfight: List of all event in teamfight
    """

    def __init__(self, zip_path):
        """Parse JSON zip pack and return corresponding dicts

        Author:
            Appcell

        Args:
            zip_path: path of the .zip file needs to be analyzed

        Returns:
            None
        """
        archive = zipfile.ZipFile(zip_path, 'r')
        self._data_metainfo = json.loads(archive.read('metainfo.json'))
        self._data_frames = json.loads(archive.read('frames.json'))
        self._data_sheet1 = json.loads(archive.read('data_sheet1.json'))
        self._data_sheet2 = json.loads(archive.read('data_sheet2.json'))
        self._data_sheet3 = json.loads(archive.read('data_sheet3.json'))
        self._elims = self.get_eliminations()
        self._resurrects = self.get_resurrects()
        self._suicides = self.get_suicides()
        self._demechs = self.get_demechs()
        self._teamfight_separations = self.get_teamfight_separations()
        self._teamfight = self.get_all_teamfight()


        self.players_arr = self.get_init_player_basic_data()

    def add_new_frame(self):

        # All data contained in one flame includes:
        # Players (12 in total), CURRENT teamfight data, CURRENT global data
        player = {
            "index": 0,
            'num_charas_used': 0,

            "elims": 0,
            "deaths": 0,
            "resurrects": 0,
            "resurrected": 0,
            "ult_charge": 0,

            "avg_elims_during_tf": 0,
            "avg_deaths_during_tf": 0,

            "avg_elim_ind_during_tf": 0,
            "avg_death_ind_during_tf": 0,

            "elims_per_10min": 0,
            "deaths_per_10min": 0,

            "dps_elims": 0,
            "elimed_by_dps": 0,

            "tank_elims": 0,
            "elimed_by_tank": 0,

            "healer_elims": 0,
            "elimed_by_healer": 0,

            "first_elims": 0,
            "first_elimed": 0,           

            "critical_elims": 0,
            "ratio_critical_elim": 0,

            "immediate_elimed": 0,
            "ult_elims": 0
        }

        basics = {
            "first_elims": [0, 0],
            "normal_elims": [0, 0],
            "immediate_elims": [0, 0],
            "ability_elims": [0, 0],
            "ult_elims": [0, 0],

            "first_elim_tf_win_ratio": [0, 0],
            "player_with_most_first_elims": [0, 0],

            "total_ults_used": 0,
            "total_ults_used_per_tf": 0,
            "global_avg_elims_per_ult": 0,
            "avg_elims_per_ult": [0, 0],

            "player_with_most_elims": [0, 0, 0, 0],
            "chara_with_most_elims": [0, 0, 0, 0],

            "player_with_most_deaths": [0, 0, 0, 0],
            "chara_with_most_deaths": [0, 0, 0, 0],

            "player_with_least_deaths": [0, 0, 0, 0],
            "chara_with_least_deaths": [0, 0, 0, 0]
        }



        teamfight_data = {
            "start_time": 0,
            "end_time": 0,
            "turning_point": 0,
            
            "ults_used_per_team": [0, 0],
            "ults_used_total": 0,
            "elims_list": [
                [{
                    "subject_player": "PlayerA",
                    "subject_chara": "Tracer",
                    "subject_index": 1,
                    "global_elim_ind": 0,
                    "team_elim_ind": 0,
                    "time": 21.5
                },
                {
                    "object_player": "PlayerB",
                    "object_chara": "Tracer",
                    "object_index": 7,
                    "global_elimed_ind": 0,
                    "team_elimed_ind": 0,
                    "time": 21
                },
                {
                    "object_player": "PlayerC",
                    "object_chara": "Zenyatta",
                    "object_index": 9,
                    "global_elimed_ind": 1,
                    "team_elimed_ind": 1,
                    "time": 22
                }
                ],
                [{
                    "subject_player": "PlayerD",
                    "subject_chara": "Roadhog",
                    "subject_index": 8,
                    "global_elim_ind": 2,
                    "team_elim_ind": 1,
                    "time": 28
                },
                {
                    "object_player": "PlayerE",
                    "object_chara": "Mccree",
                    "object_index": 2,
                    "global_elimed_ind": 2,
                    "team_elimed_ind": 1,
                    "time": 28
                }],

            ],
        }


    def get_eliminations(self, start_frame=0, end_frame=0):
        """Get all eliminatins in a given time range.

        If start_frame == 0 and end_frame == 0, return full elim list.

        Author:
            Appcell

        Args:
            start_frame: start of the time range given in seconds
            end_frame: end of the time range given in seconds

        Returns:
            A list of all eliminatins in a given time range.
        """
        return self._get_actions('Eliminate',start_frame,end_frame)

    def get_eliminations_incremented(self, data, start_frame, end_frame):
        """Append eliminations in given time range onto existed array
        
        Author:
            Appcell

        Args:
            data: list of given elimination data
            start_frame: start of the time range given in seconds
            end_frame: end of the time range given in seconds

        Returns:
            A list of all eliminatins in a given time range appended to original list.
        """
        return self._get_actions('Eliminate',start_frame,end_frame,data)

    def get_resurrects(self, start_frame=0, end_frame=0):
        """Get all resurrects in a given time range.

        If start_frame == 0 and end_frame == 0, return full resurrect list.

        Author:
            ForYou

        Args:
            start_frame: start of the time range given in seconds
            end_frame: end of the time range given in seconds

        Returns:
            A list of all resurrects in a given time range.
        """
        return self._get_actions('Resurrect',start_frame,end_frame)

    def get_resurrects_incremented(self, data, start_frame, end_frame):
        """Append resurrects in given time range onto existed array
        
        Author:
            ForYou

        Args:
            data: list of given resurrects data
            start_frame: start of the time range given in seconds
            end_frame: end of the time range given in seconds

        Returns:
            A list of all resurrects in a given time range appended to 
            original list.
        """
        return self._get_actions('Resurrect',start_frame,end_frame,data)

    def get_suicides(self, start_frame=0, end_frame=0):
        """Get all suicides in a given time range.

        If start_frame == 0 and end_frame == 0, return full suicide list.

        Author:
            ForYou

        Args:
            start_frame: start of the time range given in seconds
            end_frame: end of the time range given in seconds

        Returns:
            A list of all suicides in a given time range.
        """
        return self._get_actions('Suicide',start_frame,end_frame)

    def get_suicides_incremented(self, data, start_frame, end_frame):
        """Append suicides in given time range onto existed array
        
        Author:
            ForYou

        Args:
            data: list of given suicides data
            start_frame: start of the time range given in seconds
            end_frame: end of the time range given in seconds

        Returns:
            A list of all suicides in a given time range appended to original list.
        """
        return self._get_actions('Suicide',start_frame,end_frame,data)

    def get_demechs(self, start_frame=0, end_frame=0):
        """Get all demechs in a given time range.
        If start_frame == 0 and end_frame == 0, return full demech list.

        Author:
            ForYou

        Args:
            start_frame: start of the time range given in seconds
            end_frame: end of the time range given in seconds

        Returns:
            A list of all demechs in a given time range.
        """
        return self._get_actions('Demech',start_frame,end_frame)

    def get_demechs_incremented(self, data, start_frame, end_frame):
        """Append demechs in given time range onto existed array
        
        Author:
            ForYou

        Args:
            data: list of given demechs data
            start_frame: start of the time range given in seconds
            end_frame: end of the time range given in seconds

        Returns:
            A list of all demechs in a given time range appended to original list.
        """
        return self._get_actions('Demech',start_frame,end_frame,data)

    def get_teamfight_index(self, time):
        """Get index of team-fight happening at given timestamp.

        Author:
            ForYou

        Args:
            time: current time in seconds

        Returns:
            Index of team-fight happening at 'time'.
        """
        if len(self.teamfight_separations) <= 1:
            return 1
        else:
            for ind_timestamp in range(1, len(self.teamfight_separations)):
                if time < self.teamfight_separations[ind_timestamp] \
                and time > self.teamfight_separations[ind_timestamp - 1]:
                    return ind_timestamp
            if time > self.teamfight_separations[-1]:
                return len(self.teamfight_separations) + 1
        

    def get_teamfight_separations(self):
        """Get a list of all separation timestamps between each teamfight.
        
        Author:
            Appcell

        Args:
            None

        Returns:
            A list of all timestamps marking separations between each
            teamfight.
        """
        res = [0]
        if len(self.elims) > 1:
            for ind_elim in range(1, len(self.elims)):
                if self.elims[ind_elim]['time'] \
                - self.elims[ind_elim - 1]['time'] > 14:
                    res.append((self.elims[ind_elim]['time'] \
                        + self.elims[ind_elim - 1]['time']) / 2)
        return res


    def get_ults(self,start_frame, end_frame):
        """Output all data in sheet3 in a given timerange.

        Author:
            maocili

        Args:
            start_frame: start time
            end_frame: end time

        Returns:
            All data in sheet3 from start_frame to end_frame
        """

        res=[]

        for i,data in enumerate(self.data_sheet3):
            if not type(data['time']) == float:
                time_arr = data['time'].split(':')
                curr_time = stats.hms_to_seconds(time_arr[0],
                                                      time_arr[1], time_arr[2])
                data['time'] = curr_time
            if start_frame <= data['time'] and end_frame >= data['time']:
                res.append(data)
            elif end_frame <= data['time']:
                break

        return res

    def get_arr_varitation(self, start_frame, end_frame):

        """根据self.data_sheet3 输出时间段中的大招能量变化

        Author:
            maocili
        Args:
            start_frame : 开始时间
            end_frame : 结束时间
        Returns:
            res : 包含大招能量变化的dict
        """

        res = {
            'start_frame': start_frame,
            'end_frame': end_frame,
            'ult_charge': []
        }

        start = self.get_ults(start_frame,start_frame)
        end = self.get_ults(end_frame,end_frame)

        for i in end:
            for index,player in enumerate(i['players']):
                end[0]['players'][index]['ults'] = end[0]['players'][index]['ults'] - start[0]['players'][index]['ults']

        end[0]['time'] = [start_frame,end_frame]
        return end

    def get_ult_vary(self, data, start_frame, end_frame):

        """在data的基础上加上新时间段的变化
                Author:
                    maocili
                Args:
                    data : 时间段的大招能量变化
                    start_frame : 开始时间
                    end_frame : 结束时间
                Returns:
                    res : 两个时间段的大招能量变化
                """

        new_data= self.get_arr_varitation(start_frame,end_frame)[0]

        for index,player in enumerate(new_data['players']):
            new_data['players'][index]['ults'] = new_data['players'][index]['ults'] + data[0]['players'][index]['ults']
        new_data['time'] = [data[0]['time'], new_data['time']]
        return new_data
    
    def get_total_time(self):
        """get the time of the game

        Author:
            ngc7293

        Args:
            None

        Returns:
            float : the timestamps of the game
        """
        return self.data_frames[-1]['time']

    def get_all_eliminations(self):
        """get the total eliminations

        Author:
            ngc7293

        Args:
            None
            
        Returns:
            int: number of total eliminations
        """
    
        return len(self.elims)
    
    def get_all_deaths(self):
        """Get # of total deaths

        Author:
            ngc7293

        Args:
            None

        Returns:
            int: number of total deaths
        """
        death_num = 0
        
        for events in self.data_sheet1:
            if events['action'] == 'Eliminate' or events['action'] == 'Suicide':
                death_num += 1
            elif events['action'] == 'Resurrect':
                death_num -= 1
        
        return death_num
    
    def get_most_elim_player(self):
        """Get the most eliminations players

        Author:
            ngc7293

        Args:
            None

        Returns:
            dict: the player with most elims(number,name,the number of eliminations)
        """
        mep_dict = {}
        for events in self.elims:
            if events['action'] == 'Eliminate':
                if events['subject']['player'] in mep_dict:
                    mep_dict[events['subject']['player']] += 1
                else:
                    mep_dict[events['subject']['player']] = 1
        name = max(mep_dict,key=mep_dict.get)
        for i in range(12):
            if name == self.data_metainfo['player_names'][i]:
                index_of_player = i
                break
        res = {
            'index' :index_of_player,
            'player' :name,
            'elims' :mep_dict[name]
        }
    
        return res
    
    def get_highest_kd_player(self):
        """Get the player with highest kd ratio

        Author:
            ngc7293

        Args:
            None

        Returns:
            str: name of the player with highest kd ratio
        """
        player_dict = {}
        for events in self.data_sheet1:
            if events['action'] == 'Eliminate':
                if events['subject']['player'] in player_dict:
                    player_dict[events['subject']['player']]['elim'] += 1
                else:
                    player_dict[events['subject']['player']] = {
                        'elim':1,
                        'dead':0
                    }
                if events['object']['player'] in player_dict:
                    player_dict[events['object']['player']]['dead'] += 1
                else:
                    player_dict[events['object']['player']] = {
                        'elim':0,
                        'dead':1
                    }
        mkp_dict = {}
        for player in player_dict:
            if player_dict[player]['dead'] == 0:
                player_dict[player]['dead'] = 1
            mkp_dict[player] = player_dict[player]['elim']/player_dict[player]['dead']
        
        return max(mkp_dict, key=mkp_dict.get)
    
    def get_all_teamfight(self):
        """Get a list of all teamfights in full match

        Author:
            ngc7293

        Args:
            None
            
        Returns:
            list: a list of all teamfights
        """
        if self.teamfight_separations == [0]:
            sep = [0,self.get_total_time()]
        res = []
        start_frame_target = 0
        end_frame_target = 1
        one_fight = []
        for event in self.elims:
            if event['action'] == 'Eliminate' and \
                    event['time'] >= sep[start_frame_target] and \
                    event['time'] <= sep[end_frame_target]:
                one_fight.append(event)
            elif event['time'] >= sep[end_frame_target]:
                start_frame_target += 1
                end_frame_target += 1
                res.append(one_fight)
                one_fight = []
        res.append(one_fight)
        return res
            
    def get_average_teamfight_time(self):
        """Get the avg teamfight time computed across the whole game

        Author:
            ngc7293

        Args:
            None

        Returns:
            float: avg teamfight time
        """
        fight_time = [fight[-1]['time']-fight[0]['time']+7 for fight in self.teamfight]
        return sum(fight_time)/len(fight_time)

    def get_totalnum_teamfight(self):
        """Get the teamfights' count

        Author:
            ngc7293

        Args:
            None

        Returns:
            int: the # of teamfight
        """
        return len(self.teamfight)

    def _get_actions(self, action, start_frame = 0, end_frame = 0, data = None):
        """Get action list via "action" key-value pairs in events list.

        Author:
            ForYou

        Args:
            action: action type
            start_frame: start of the time range given in seconds
            end_frame: end of the time range given in seconds

        Returns:
            List of all actions
        """
        res = data if data else []
        if end_frame == 0 and start_frame == 0:
            for event in self.data_sheet1:
                if event['action'] == action:
                    time_arr = event['time'].split(':')
                    curr_time = stats.hms_to_seconds(
                        time_arr[0], time_arr[1], time_arr[2])
                    event['frame_ind'] = curr_time
                    res.append(event)
        else:
            for event in self.data_sheet1:
                time_arr = event['time'].split(':')
                curr_time = stats.hms_to_seconds(time_arr[0],
                    time_arr[1], time_arr[2])
                if curr_time >= start_frame and curr_time >= end_frame \
                and self.event['action'] == action:
                    event['time'] = curr_time
                    res.append(event)
        return res



    def get_init_player_basic_data(self):
        """ Initialize data according to data_sheet2

        Author:
            ForYou

        Args：
            None

        Returns：
        players_arr：以选手player为单位的数组，共12个，每个player中包括以下内容：
             team：队伍名称
             team_status：队伍进攻或防守
             index：编号从左往右
             name：选手id
             starting lineup：首先使用的英雄
             final lineup：最后使用的英雄
             totalhero：使用的英雄数量
    
             totalEliminate：击杀总数(不含助攻即最后一击)
             totalEliminateDetail:击杀来源(数组)
                chara：英雄名
                num：击杀次数
             totalassist：助攻总数
             totalassistDetail:助攻来源(数组)
                chara：英雄名
                num：助攻次数
             totalResurrect：复活总数
             totaldie：死亡总数
             totaldieDetail:死亡来源(数组)
                chara：英雄名
                num：死亡次数
             totalcritical die：被爆头击杀总数
             totalSuicide：自杀总数
             totalResurrected：被复活总数
             totalcritical kill：爆头击杀总数
             totalassist die：被助攻总数(集火目标)
             机甲相关
             totalDemech：击杀机甲总数(不含助攻即最后一击)
             totalDemechassist：助攻机甲总数
             totalDemechdie：机甲死亡总数
             totalDemechcritical die：机甲被爆头击杀总数
             totalDemechcritical kill：爆头击杀机甲总数
             totalDemechassist die：机甲被助攻总数(集火目标)
             heros：（数组）使用的英雄明细如下
                chara：英雄名
                Eliminate：击杀总数(不含助攻即最后一击)
                EliminateDetail:击杀来源(数组)
                    chara：英雄名
                    num：击杀次数
                assist：助攻总数
                assistDetail:助攻来源(数组)
                    chara：英雄名
                    num：助攻次数
                Resurrect：复活总数
                die：死亡总数
                dieDetail:死亡来源(数组)
                    chara：英雄名
                    num：死亡次数
                critical die：被爆头击杀总数
                Suicide：自杀总数
                Resurrected：被复活总数
                critical kill：爆头击杀总数
                assist die：被助攻总数(集火目标)
                机甲相关
                Demech：击杀机甲总数(不含助攻即最后一击)
                Demechassist：助攻机甲总数
                Demechdie：机甲死亡总数
                Demechcritical die：机甲被爆头击杀总数
                Demechcritical kill：爆头击杀机甲总数
                Demechassist die：机甲被助攻总数(集火目标)
        """
        heros = {
            'chara':'',
            'Eliminate':0,
            'assist':0,
            'Resurrect':0,
            'die':0,
            'Suicide':0,
            'Resurrected':0,
            'critical die':0,
            'critical kill':0,
            'assist die':0,
            'EliminateDetail':[],
            'assistDetail':[],
            'dieDetail':[]}

        total = {
            'totalhero':1,
            'totalEliminate':0,
            'totalassist':0,
            'totalResurrect':0,
            'totaldie':0,
            'totalSuicide':0,
            'totalResurrected':0,
            'totalcritical die':0,
            'totalcritical kill':0,
            'totalassist die':0,
            'totalDemech':0,
            'totalDemechassist':0,
            'totalDemechdie':0,
            'totalDemechcritical die':0,
            'totalDemechcritical kill':0,
            'totalDemechassist die':0,
            'totalEliminateDetail':[],
            'totalassistDetail':[],
            'totaldieDetail':[]}

        players_arr = []

        for teamindex, teamvalue in enumerate(self.data_sheet2):
            for player in teamvalue['players']:
                hero = player['starting lineup']
                heros['chara'] = hero
                player['heros'] = []
                player['heros'].append(heros)
                player['team'] = teamvalue['team']
                player['team_status'] = teamvalue['team_status']
                for key in total:
                    player[key] = total[key]
                players_arr.append(player)

        return players_arr


    def get_player_basic_eliminates(self, start_frame=0, end_frame=0, data=None):
        """获取在原数据基础上返回固定时间段内击杀相关数据粗加工

        Author:
            ForYou

        Args：
            start_frame开始时间end_frame结束时间data原数据

        Returns：
            同get_init_player_basic_data()返回值
        """

        #提供了data原有数据就在原有数据累加，没有提供则在初始化的选手信息self.players_arr上添加
        if data == 0:
            players_arr = self.players_arr
        else:
            players_arr = data

        #提供了开始和结束时间则取时间内的击杀事件加工，没有提供则默认全部击杀事件
        if end_frame == 0 and start_frame == 0:
            eliminations = self.elims
        else:
            eliminations = self.get_eliminations(start_frame, end_frame)

        heros = {
        'chara':'',
        'Eliminate':0,
        'assist':0,
        'Resurrect':0,
        'die':0,
        'Suicide':0,
        'Resurrected':0,
        'critical die':0,
        'critical kill':0,
        'assist die':0,
        'EliminateDetail':[],
        'assistDetail':[],
        'dieDetail':[]}

        #遍历提供的击杀事件，从其中提取信息
        for elim_ind, elim in enumerate(eliminations):
            #遍历选手列表，找到信息对应的选手，循环中主要处理三类信息 1：击杀者  2：助攻  3：被击杀者
            for player_ind, player in enumerate(players_arr):
                # 1：击杀者相关信息(1a 总击杀 1b爆头总击杀 1c 总击杀明细 1d 使用英雄击杀相关)
                if player['name'] == elim['subject']['player']:
                    # 1a 总击杀
                    players_arr[player_ind]['totalEliminate'] += 1
                    # 1b 爆头总击杀
                    if elim['critical kill'] == 'Y':
                        players_arr[player_ind]['totalcritical kill'] += 1
                    # 1c 总击杀明细 (敌方哪个英雄 几次)
                    hero_eliminate = 0
                    for  obj_hero_index , obj_hero_value in enumerate(player['totalEliminateDetail']):
                        if obj_hero_value['chara'] == elim['object']['chara']:
                            hero_eliminate = 1
                            players_arr[player_ind]['totalEliminateDetail'][obj_hero_index]['num'] += 1
                            break
                    # 击杀明细列表中 无此英雄则新增
                    if hero_eliminate == 0:
                        newhero_eliminate = {'chara':elim['object']['chara'],'num':1}
                        players_arr[player_ind]['totalEliminateDetail'].append(newhero_eliminate)
                    # 1d 使用英雄击杀相关
                    heroisexsit = 0
                    #遍历已使用英雄
                    for  used_hero_index, used_hero_value in enumerate(player['heros']):
                        #和选手总击杀类似，这里处理选手不同英雄的击杀数据
                        if used_hero_value['chara'] == elim['subject']['chara']:
                            heroisexsit = 1
                            players_arr[player_ind]['heros'][used_hero_index]['Eliminate'] += 1
                            if elim['critical kill'] == 'Y':
                                players_arr[player_ind]['heros'][used_hero_index]['critical kill'] += 1
                            hero_eliminate = 0
                            #击杀敌方英雄详情
                            for  hero_action_detail_index , hero_action_detail_value in enumerate(player['heros']['EliminateDetail']):
                                if hero_action_detail_value['chara'] == elim['object']['chara']:
                                    hero_eliminate = 1
                                    players_arr[player_ind]['heros'][used_hero_index]['EliminateDetail'][hero_action_detail_index]['num'] += 1
                                    break
                            if hero_eliminate == 0:
                                newhero_eliminate = {'chara':elim['object']['chara'],'num':1}
                                players_arr[player_ind]['heros'][used_hero_index]['EliminateDetail'].append(newhero_eliminate)
                            break
                    #未使用过此英雄则新增
                    if heroisexsit == 0:
                        newhero = deepcopy(heros)
                        newhero['chara'] = elim['subject']['chara']
                        newhero['Eliminate'] = 1
                        newhero_eliminate = {'chara':elim['object']['chara'],'num':1}
                        newhero['EliminateDetail'].append(newhero_eliminate)
                        players_arr[player_ind]['totalhero'] +=  1
                        if elim['critical kill'] == 'Y':
                            newhero['critical kill'] = 1
                        players_arr[player_ind]['heros'].append(newhero)
                # 2：助攻相关信息 total_assist_die字段记录这次击杀事件造成几个助攻，累加在选手的assist die和totalassist die上，assist die/die 可以看出敌方队伍集火目标
                total_assist_die = 0
                for assistplayer in elim['assist']:
                    #遍历助攻列表 处理选手的 2a总助攻 2b总助攻明细 2c不同英雄助攻信息 
                    if player['name'] == assist[assistplayer]['player']:
                        total_assist_die += 1
                        # 2a 总助攻
                        players_arr[player_ind]['totalassist'] += 1
                        # 2b 总助攻明细
                        heroassist = 0
                        for  obj_hero_index , obj_hero_value in enumerate(player['totalassistDetail']):
                            if obj_hero_value['chara'] == elim['object']['chara']:
                                heroassist = 1
                                players_arr[player_ind]['totalassistDetail'][obj_hero_index]['num'] += 1
                                break
                        if heroassist == 0:
                            newheroassist = {'chara':elim['object']['chara'],'num':1}
                            players_arr[player_ind]['totalassistDetail'].append(newheroassist)
                        # 2c 遍历英雄更新助攻信息
                        heroisexsit = 0
                        for  used_hero_index, used_hero_value in enumerate(player['heros']):
                            if used_hero_value['chara'] == assist[assistplayer]['hero']:
                                heroisexsit = 1
                                players_arr[player_ind]['heros'][used_hero_index]['assist'] += 1
                                #助攻击杀敌方英雄信息
                                heroassist = 0
                                for  hero_action_detail_index , hero_action_detail_value in enumerate(player['heros']['assistDetail']):
                                    if hero_action_detail_value['chara'] == elim['object']['chara']:
                                        heroassist = 1
                                        players_arr[player_ind]['heros'][used_hero_index]['assistDetail'][hero_action_detail_index]['num'] += 1
                                        break
                                if heroassist == 0:
                                    newheroassist = {'chara':elim['object']['chara'],'num':1}
                                    players_arr[player_ind]['heros'][used_hero_index]['assistDetail'].append(newheroassist)
                                break
                        #使用英雄不存在则新增
                        if heroisexsit == 0:
                            newhero = deepcopy(heros)
                            newhero['chara'] = assist[assistplayer]['hero']
                            newhero['assist'] = 1
                            newheroassist = {'chara':elim['object']['chara'],'num':1}
                            newhero['assistDetail'].append(newheroassist)
                            players_arr[player_ind]['totalhero'] +=  1
                            players_arr[player_ind]['heros'].append(newhero)
                # 3：被击杀者信息(3a 总死亡 3b总被助攻 3c 总被爆头击杀 3d 被击杀明细 3e 被击杀英雄相关)
                if player['name'] == elim['object']['player']:
                    #3a 总死亡
                    players_arr[player_ind]['totaldie'] += 1
                    #3b 总被助攻数
                    players_arr[player_ind]['totalassist die'] += total_assist_die
                    #3c 总被爆头击杀数
                    if elim['critical kill'] == 'Y':
                        players_arr[player_ind]['totalcritical die'] += 1
                    #3d 被击杀明细 (造成击杀的敌方英雄构成及次数)
                    herodie = 0
                    for  obj_hero_index , obj_hero_value in enumerate(player['totaldieDetail']):
                        if obj_hero_value['chara'] == elim['subject']['chara']:
                            herodie = 1
                            players_arr[player_ind]['totaldieDetail'][obj_hero_index]['num'] += 1
                            break
                    if herodie == 0:
                        newherodie = {'chara':elim['subject']['chara'],'num':1}
                        players_arr[player_ind]['totaldieDetail'].append(newherodie)
                    #3e 被击杀英雄(死亡构成) 数据结构与总数据类似
                    heroisexsit = 0
                    for  used_hero_index, used_hero_value in enumerate(player['heros']):
                        if used_hero_value['chara'] ==  elim['object']['chara']:
                            heroisexsit = 1
                            players_arr[player_ind]['heros'][used_hero_index]['die'] += 1
                            players_arr[player_ind]['heros'][used_hero_index]['assist die'] += total_assist_die
                            if elim['critical kill'] == 'Y':
                                players_arr[player_ind]['heros'][used_hero_index]['critical die'] += 1
                            herodie = 0
                            for  hero_action_detail_index , hero_action_detail_value in enumerate(player['heros']['dieDetail']):
                                if hero_action_detail_value['chara'] == elim['subject']['chara']:
                                    herodie = 1
                                    players_arr[player_ind]['heros'][used_hero_index]['dieDetail'][hero_action_detail_index]['num'] += 1
                                    break
                            if herodie == 0:
                                newherodie = {'chara':elim['subject']['chara'],'num':1}
                                players_arr[player_ind]['heros'][used_hero_index]['dieDetail'].append(newherodie)
                            break
                    #被击杀的英雄不存在则新增
                    if heroisexsit == 0:
                        newhero = deepcopy(heros)
                        newhero['chara'] = elim['object']['chara']
                        newhero['die'] = 1
                        newherodie = {'chara':elim['subject']['chara'],'num':1}
                        newhero['dieDetail'].append(newherodie)
                        newhero['assist die'] = total_assist_die
                        players_arr[player_ind]['totalhero'] += 1
                        if elim['critical kill'] == 'Y':
                            newhero['critical die'] = 1
                        players_arr[player_ind]['heros'].append(newhero)

    def get_player_basic_resurrects(self, start_frame=0, end_frame=0, data=0):
        '''
        获取在原数据基础上返回固定时间段内复活相关数据粗加工
        Author:
            ForYou
        Args：
        start_frame开始时间end_frame结束时间data原数据
        Returns：
        同get_init_player_basic_data()返回值
        '''
        #提供了data原有数据就在原有数据累加，没有提供则在初始化的选手信息self.players_arr上添加
        if data == 0:
            players_arr = self.players_arr
        else:
            players_arr = data
        #提供了开始和结束时间则取时间内的复活事件加工，没有提供则默认全部复活事件
        if end_frame == 0 and start_frame == 0:
            resurrects = self.resurrects
        else:
            resurrects = self.get_resurrects(start_frame,end_frame)
        heros = {'chara':'','Eliminate':0,'assist':0,'Resurrect':0,'die':0,'Suicide':0,'Resurrected':0,'critical die':0,'critical kill':0,'assist die':0,'EliminateDetail':[],'assistDetail':[],'dieDetail':[]}
        #遍历提供的复活事件
        for index, value in enumerate(resurrects):
            #遍历选手列表 更新 1 复活数据  2 被复活数据
            for player_ind, playervalue in enumerate(players_arr):
                #复活数据 和击杀数据一样做了英雄分组 1是为了保持数据格式的一致性，2是防止出另外具有复活技能的英雄 
                if playervalue['name'] == value['subject']['player']:
                    players_arr[player_ind]['totalResurrect'] += 1
                    heroisexsit = 0
                    for  used_hero_index, used_hero_value in enumerate(playervalue['heros']):
                        if used_hero_value['chara'] ==  value['subject']['chara']:
                            heroisexsit = 1
                            players_arr[player_ind]['heros'][used_hero_index]['Resurrect'] += 1
                            break
                    if heroisexsit == 0:
                        newhero = deepcopy(heros)
                        newhero['chara'] = value['subject']['chara']
                        newhero['Resurrect'] = 1
                        players_arr[player_ind]['totalhero'] += 1
                        players_arr[player_ind]['heros'].append(newhero)
                #被复活数据
                if playervalue['name'] == value['object']['player']:
                    players_arr[player_ind]['totalResurrected'] += 1
                    heroisexsit = 0
                    for  used_hero_index, used_hero_value in enumerate(playervalue['heros']):
                        if used_hero_value['chara'] == value['object']['chara']:
                            heroisexsit = 1
                            players_arr[player_ind]['heros'][used_hero_index]['Resurrected'] += 1
                            break
                    if heroisexsit == 0:
                        newhero = deepcopy(heros)
                        newhero['chara'] = value['object']['chara']
                        newhero['Resurrected'] = 1
                        players_arr[player_ind]['totalhero'] += 1
                        players_arr[player_ind]['heros'].append(newhero)

    def get_player_basic_suicides(self,start_frame=0,end_frame=0,data=0):
        '''
        获取在原数据基础上返回固定时间段内自杀相关数据粗加工
        Author:
            ForYou
        Args：
        start_frame开始时间end_frame结束时间data原数据
        Returns：
        同get_init_player_basic_data()返回值
        '''
        #提供了data原有数据就在原有数据累加，没有提供则在初始化的选手信息self.players_arr上添加
        if data == 0:
            players_arr = self.players_arr
        else:
            players_arr = data
        #提供了开始和结束时间则取时间内的自杀事件加工，没有提供则默认全部自杀事件
        if end_frame == 0 and start_frame == 0:
            suicides = self.suicides
        else:
            suicides = self.get_suicides(start_frame,end_frame)
        heros = {'chara':'','Eliminate':0,'assist':0,'Resurrect':0,'die':0,'Suicide':0,'Resurrected':0,'critical die':0,'critical kill':0,'assist die':0,'EliminateDetail':[],'assistDetail':[],'dieDetail':[]}
        #遍历提供的自杀事件
        for index, value in enumerate(suicides):
            #遍历选手列表 更新自杀数据
            for player_ind, playervalue in enumerate(players_arr):
                if playervalue['name'] == value['object']['player']:
                    players_arr[player_ind]['totalSuicide'] += 1
                    heroisexsit = 0
                    for  used_hero_index, used_hero_value in enumerate(playervalue['heros']):
                        if used_hero_value['chara'] == value['object']['chara']:
                            heroisexsit = 1
                            players_arr[player_ind]['heros'][used_hero_index]['Suicide'] += 1
                            break
                    if heroisexsit == 0:
                        newhero = deepcopy(heros)
                        newhero['chara'] = value['object']['chara']
                        newhero['Suicide'] = 1
                        players_arr[player_ind]['totalhero'] += 1
                        players_arr[player_ind]['heros'].append(newhero)

    def get_player_basic_demechs(self,start_frame=0,end_frame=0,data=0):
        '''
        获取在原数据基础上返回固定时间段内机甲相关数据粗加工
        Author:
            ForYou
        Args：
        start_frame开始时间end_frame结束时间data原数据
        Returns：
        同get_init_player_basic_data()返回值
        '''
        #提供了data原有数据就在原有数据累加，没有提供则在初始化的选手信息self.players_arr上添加
        if data == 0:
            players_arr = self.players_arr
        else:
            players_arr = data
        #提供了开始和结束时间则取时间内的击杀机甲事件加工，没有提供则默认全部击杀机甲事件
        if end_frame == 0 and start_frame == 0:
            demechs = self.demechs
        else:
            demechs = self.get_suicides(start_frame,end_frame)
        heros = {'chara':'','Eliminate':0,'assist':0,'Resurrect':0,'die':0,'Suicide':0,'Resurrected':0,'critical die':0,'critical kill':0,'assist die':0,'EliminateDetail':[],'assistDetail':[],'dieDetail':[]}
        #遍历提供的击杀机甲事件 此函数与击杀事件get_player_basic_eliminates类似，注释会从简
        for index, value in enumerate(demechs):
            #遍历选手列表 处理选手的 1 拆机甲 2 助攻拆机甲 3 被拆机甲
            for player_ind, playervalue in enumerate(players_arr):
                # 1：拆机甲相关数据 拆机甲总数 爆头拆机甲总数  不同英雄拆机甲数据
                if playervalue['name'] == value['subject']['player']:
                    players_arr[player_ind]['totalDemech'] += 1
                    if value['critical kill'] == 'Y':
                        players_arr[player_ind]['totalDemechcritical kill'] += 1
                    heroisexsit = 0
                    for  used_hero_index, used_hero_value in enumerate(playervalue['heros']):
                        if used_hero_value['chara'] ==  value['subject']['chara']:
                            heroisexsit = 1
                            players_arr[player_ind]['heros'][used_hero_index]['Demech'] += 1
                            if value['critical kill'] == 'Y':
                                players_arr[player_ind]['heros'][used_hero_index]['Demechcritical kill'] += 1
                            break
                    if heroisexsit == 0:
                        newhero = deepcopy(heros)
                        newhero['chara'] = value['subject']['chara']
                        newhero['Demech'] = 1
                        players_arr[player_ind]['totalhero'] += 1
                        if value['critical kill'] == 'Y':
                            newhero['Demechcritical kill'] = 1
                        players_arr[player_ind]['heros'].append(newhero)
                #2：助攻拆机甲数据 遍历助攻列表 处理选手的 总助攻  不同英雄助攻信息
                total_demech_assistdie = 0
                for assistplayer in value['assist']:
                    if playervalue['name'] == assist[assistplayer]['player']:
                        total_demech_assistdie += 1
                        players_arr[player_ind]['totalDemechassist'] += 1
                        heroisexsit = 0
                        for  used_hero_index, used_hero_value in enumerate(playervalue['heros']):
                            if used_hero_value['chara'] == assist[assistplayer]['hero']:
                                heroisexsit = 1
                                players_arr[player_ind]['heros'][used_hero_index]['Demechassist'] += 1
                                break
                        if heroisexsit == 0:
                            newhero = deepcopy(heros)
                            newhero['chara'] = assist[assistplayer]['hero']
                            newhero['Demechassist'] = 1
                            players_arr[player_ind]['totalhero'] += 1
                            players_arr[player_ind]['heros'].append(newhero)
                #3:被拆机甲信息(总死亡 总被助攻 总被爆头击杀 被击杀英雄此处专指dva)
                if playervalue['name'] == value['object']['player']:
                    players_arr[player_ind]['totalDemechdie'] += 1
                    players_arr[player_ind]['totalDemechassist die'] += total_demech_assistdie
                    if value['critical kill'] == 'Y':
                        players_arr[player_ind]['totalDemechcritical die'] += 1
                    heroisexsit = 0
                    for  used_hero_index, used_hero_value in enumerate(playervalue['heros']):
                        #判断存疑 如果机甲的chara是 meta 这里面需要修改为dva 如果不是meta则不需要修改
                        if used_hero_value['chara'] ==  value['object']['chara']:
                            heroisexsit = 1
                            players_arr[player_ind]['heros'][used_hero_index]['Demechdie'] += 1
                            players_arr[player_ind]['heros'][used_hero_index]['Demechassist die'] += total_demech_assistdie
                            if value['critical kill'] == 'Y':
                                players_arr[player_ind]['heros'][used_hero_index]['Demechcritical die'] += 1
                            break
                    if heroisexsit == 0:
                        newhero = deepcopy(heros)
                        newhero['chara'] = value['object']['chara']
                        newhero['Demechdie'] = 1
                        newhero['Demechassist die'] = total_demech_assistdie
                        players_arr[player_ind]['totalhero'] += 1
                        if value['critical kill'] == 'Y':
                            newhero['Demechcritical die'] = 1
                        players_arr[player_ind]['heros'].append(newhero)
