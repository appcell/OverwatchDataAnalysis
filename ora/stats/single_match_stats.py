import os
import sys
import zipfile
import json
import copy

sys.path.append('../utils')
from utils import StatsUtils

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
        self.data_metainfo = json.loads(archive.read('metainfo.json'))
        self.data_frames = json.loads(archive.read('frames.json'))
        self.data_sheet1 = json.loads(archive.read('data_sheet1.json'))
        self.data_sheet2 = json.loads(archive.read('data_sheet1.json'))
        self.data_sheet3 = json.loads(archive.read('data_sheet1.json'))
        self.elims = self.get_eliminations()
        self.teamfight_separations = self.get_teamfight_separations()

    def get_eliminations(self, start_time=0, end_time=0):
        """Get all eliminatins in a given time range.

        If start_time == 0 and end_time == 0, return full elim list.

        Author:
            Appcell

        Args:
            start_time: start of the time range given in seconds
            end_time: end of the time range given in seconds

        Returns:
            A list of all eliminatins in a given time range.
        """
        res = []
        if end_time == 0 and start_time == 0:
            for event in self.data_sheet1:
                if event['action'] == 'Eliminate':
                    time_arr = event['time'].split(':')
                    curr_time = StatsUtils.hms_to_seconds(time_arr[0], 
                        time_arr[1], time_arr[2])
                    event['time'] = curr_time
                    res.append(event)
        else:
            for event in self.data_sheet1:
                time_arr = event['time'].split(':')
                curr_time = StatsUtils.hms_to_seconds(time_arr[0], 
                    time_arr[1], time_arr[2])
                if curr_time >= start_time and curr_time >= end_time \
                and self.event['action'] == 'Eliminate':
                    event['time'] = curr_time
                    res.append(event)
        return res

    def get_eliminations_incremented(self, data, start_time, end_time):
        """Append eliminations in given time range onto existed array
        
        Author:
            Appcell

        Args:
            data: list of given elimination data
            start_time: start of the time range given in seconds
            end_time: end of the time range given in seconds

        Returns:
            A list of all eliminatins in a given time range appended to original list.
        """
        return data.append(self.get_eliminations(start_time, end_time))


    def get_teamfight_index(self, time):
        """Get index of team-fight happening at given timestamp.
        
        A temporary standard for separating team-fights:

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
            A list of all timestamps marking separations between each teamfight.
        """
        res = [0]
        if len(self.elims) > 1:
            for ind_elim in range(1, len(self.elims)):
                if self.elims[ind_elim]['time'] \
                - self.elims[ind_elim - 1]['time'] > 14:
                    res.append((self.elims[ind_elim]['time'] \
                        + self.elims[ind_elim - 1]['time']) / 2)
        return res

    def get_ults(self, start_time=0, end_time=0):
        '''
                根据data_sheet3.json 输入开始时间和结束时间 输出该时间段内每个英雄的大招能量变化
                Author:
                    maocili
                Args:
                    start:开始时间
                    end:结束时间
                Returns:
                    ult_list [{'time': 10.0, 'ult_info': {1: {'team': 0, 'name': 'Player1', 'chara': 'Lucio', 'ults': 1}, ...}}]
                '''

        res = []
        if end_time == 0 and start_time == 0:

            # 选手队伍信息
            key_name = {}
            player_info = {}
            for name, line in zip(self.data_sheet2, range(len(self.data_sheet2))):
                for players in name['players']:
                    key_name['team'] = line
                    key_name['name'] = players['name']
                    player_info[players['index']] = key_name.copy()

            for event in self.data_sheet3:
                time_arr = event['time'].split(':')
                curr_time = StatsUtils.hms_to_seconds(time_arr[0],
                                                      time_arr[1], time_arr[2])
                event['time'] = curr_time
                res.append(event)
            return player_info, res
        else:
            ult_change = {}
            player_info = self.player_info.copy()
            for i in self.ults:
                time = i['time']
                if start_time <= time and time <= end_time:
                    ult_change['time'] = time
                    for ult in i['players']:
                        player_info[ult['index']]['chara'] = ult['chara']
                        player_info[ult['index']]['ults'] = ult['ults']
                    ult_change['ult_info'] = player_info.copy()
                    res.append(copy.deepcopy(ult_change))
            return res

    def get_ult_vary(self, data, start_time, end_time):

        '''
               输入一个包含每个英雄大招能量变化的array 开始时间 结束时间 修改这个array使其表示出在array的基础上 经过开始-结束这段时间之后 每个英雄的大招能量变化
                Author:
                    maocili
                Args:
                    start:开始时间
                    end:停止时间
                    data:包含每个英雄大招能量变化的array
                Returns:
                    res {'start_time': 20.0, 'end_time': 40.0, 'ult_info': [{'team': 0, 'player': 'Player1', 'ult_varitation': 38},....]}
                '''

        data = data.copy()
        res = {}
        startTime = {}
        endTime = {}
        arr_time = {}

        res['start_time'] = start_time
        res['end_time'] = end_time

        for data_info in data:
            if start_time == data_info['time']:
                startTime = data_info
            if end_time == data_info['time']:
                endTime = data_info
        ult_info = {}
        info_list = []
        for s_index in startTime['ult_info']:
            varitation = endTime['ult_info'][s_index]['ults'] - startTime['ult_info'][s_index]['ults']

            ult_info['team'] = startTime['ult_info'][s_index]['team']
            ult_info['player'] = startTime['ult_info'][s_index]['name']
            ult_info['ult_varitation'] = varitation
            info_list.append(ult_info.copy())
        res['ult_info'] = copy.deepcopy(info_list)
        return res


    def get_arr_varitation(self, data, start_time, end_time):
        '''
              输入开始和结束时间 输出一个包含这段时间内每个人每一帧的大招能量的array
               Author:
                   maocili
               Args:
                   start:开始时间
                   end:停止时间
                   data:包含每个英雄大招能量变化的array
               Returns:
                   {'start_time': 20.0, 'end_time': 40.0, 'ult_charge': [{'team': 1, 'player': 'Player12', 'ult_charge': [6, 6, 17, 18, 22,]},...]}//包含12个}
               '''
        data = data.copy()
        res = {
            'start_time': start_time,
            'end_time': end_time,
            'ult_charge': []
        }

        ult_info = []
        info_dict = {}
        for index in range(1, 13):
            info_dict['team'] = data[0]['ult_info'][index]['team']
            info_dict['player'] = data[0]['ult_info'][index]['name']
            info_dict['ult_charge'] = []
            for data_info in data:
                if start_time <= data_info['time'] and data_info['time'] <= end_time:
                    for i in data_info['ult_info']:
                        if data_info['ult_info'][i]['name'] == info_dict['player']:
                            info_dict['ult_charge'].append(data_info['ult_info'][i]['ults'])
            res['ult_charge'].append(info_dict)

        return res
