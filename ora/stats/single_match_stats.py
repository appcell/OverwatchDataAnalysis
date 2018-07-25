# coding: utf-8
import os
import sys
import zipfile
import json

sys.path.append('../utils')
from utils import stats


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
        self.data_metainfo = json.loads(archive.read('metainfo.json'))
        self.data_frames = json.loads(archive.read('frames.json'))
        self.data_sheet1 = json.loads(archive.read('data_sheet1.json'))
        self.data_sheet2 = json.loads(archive.read('data_sheet2.json'))
        self.data_sheet3 = json.loads(archive.read('data_sheet3.json'))
        self.elims = self.get_eliminations()
        self.resurrects = self.get_resurrects()
        self.suicides = self.get_suicides()
        self.demechs = self.get_demechs()
        self.teamfight_separations = self.get_teamfight_separations()
        self.teamfight = self.get_all_teamfight()
        self.playerArr = self.get_init_plarer_basic_data()

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
                    curr_time = stats.hms_to_seconds(time_arr[0],
                        time_arr[1], time_arr[2])
                    event['time'] = curr_time
                    res.append(event)
        else:
            for event in self.data_sheet1:
                time_arr = event['time'].split(':')
                curr_time = stats.hms_to_seconds(time_arr[0],
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


    def get_ults(self,start_time, end_time):
        """输出时间段内的data_sheet3
        Author:
            maocili
        Args:
            start_time : 开始时间
            end_time : 结束时间
        Returns:
            res : 包含data_sheet3的list
        """

        res=[]

        for i,data in enumerate(self.data_sheet3):
            if not type(data['time']) == float:
                time_arr = data['time'].split(':')
                curr_time = stats.hms_to_seconds(time_arr[0],
                                                      time_arr[1], time_arr[2])
                data['time'] = curr_time
            if start_time <= data['time'] and end_time >= data['time']:
                res.append(data)
            elif end_time <= data['time']:
                break

        return res

    def get_arr_varitation(self, start_time, end_time):

        """根据self.data_sheet3 输出时间段中的大招能量变化
        Author:
            maocili
        Args:
            start_time : 开始时间
            end_time : 结束时间
        Returns:
            res : 包含大招能量变化的dict
        """

        res = {
            'start_time': start_time,
            'end_time': end_time,
            'ult_charge': []
        }

        start = self.get_ults(start_time,start_time)
        end = self.get_ults(end_time,end_time)

        for i in end:
            for index,player in enumerate(i['players']):
                end[0]['players'][index]['ults'] = end[0]['players'][index]['ults'] - start[0]['players'][index]['ults']

        end[0]['time'] = [start_time,end_time]
        return end

    def get_ult_vary(self, data, start_time, end_time):

        """在data的基础上加上新时间段的变化
                Author:
                    maocili
                Args:
                    data : 时间段的大招能量变化
                    start_time : 开始时间
                    end_time : 结束时间
                Returns:
                    res : 两个时间段的大招能量变化
                """

        new_data= self.get_arr_varitation(start_time,end_time)[0]

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
        """get the total deaths
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
        """get the most eliminations players
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
    
    def get_most_kda_player(self):
        """get the most kd-rate players
        Author:
            ngc7293
        Args:
            None
        Returns:
            str: the player have most kd-rate
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
        
        return max(mkp_dict,key=mkp_dict.get)
    
    def get_all_teamfight(self):
        """get the teamfight in whole game
        Author:
            ngc7293
        Args:
            None
        Returns:
            list: the list of all teamfights
        """
        if self.teamfight_separations == [0]:
            sep = [0,self.get_total_time()]
        res = []
        start_time_target = 0
        end_time_target = 1
        one_fight = []
        for event in self.elims:
            if event['action'] == 'Eliminate' and \
                    event['time'] >= sep[start_time_target] and \
                    event['time'] <= sep[end_time_target]:
                one_fight.append(event)
            elif event['time'] >= sep[end_time_target]:
                start_time_target += 1
                end_time_target += 1
                res.append(one_fight)
                one_fight = []
        res.append(one_fight)
        return res
            
    def get_avgtime_teamfight(self):
        """get the avg teamfight time in whole game
        Author:
            ngc7293
        Args:
            None
        Returns:
            float: the avgtime of all teamfight
        """
        fight_time = [fight[-1]['time']-fight[0]['time']+7 for fight in self.teamfight]
        return sum(fight_time)/len(fight_time)

    def get_count_teamfight(self):
        """get the teamfights' count
        Author:
            ngc7293
        Args:
            None
        Returns:
            int: the  count of teamfight
        """
        return len(self.teamfight)

    def get_init_plarer_basic_data(self):
        '''
        根据data_sheet2初始化各个选手基本数据
        Author:
            ForYou
        Args：
        None
        Returns：
        playerArr：以选手player为单位的数组，共12个，每个player中包括以下内容：
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

        '''
        heros = {'chara':'','Eliminate':0,'assist':0,'Resurrect':0,'die':0,'Suicide':0,'Resurrected':0,'critical die':0,'critical kill':0,'assist die':0,'EliminateDetail':[],'assistDetail':[],'dieDetail':[]}
        total = {'totalhero':1,'totalEliminate':0,'totalassist':0,'totalResurrect':0,'totaldie':0,'totalSuicide':0,'totalResurrected':0,'totalcritical die':0,'totalcritical kill':0,'totalassist die':0,'totalDemech':0,'totalDemechassist':0,'totalDemechdie':0,'totalDemechcritical die':0,'totalDemechcritical kill':0,'totalDemechassist die':0,'totalEliminateDetail':[],'totalassistDetail':[],'totaldieDetail':[]}
        playerArr = []
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
                playerArr.append(player)
        return playerArr

    def get_resurrects(self, start_time=0, end_time=0):
        """Get all resurrects in a given time range.
        If start_time == 0 and end_time == 0, return full resurrect list.
        Author:
            ForYou
        Args:
            start_time: start of the time range given in seconds
            end_time: end of the time range given in seconds
        Returns:
            A list of all resurrects in a given time range.
        """
        res = []
        if end_time == 0 and start_time == 0:
            for event in self.data_sheet1:
                if event['action'] == 'Resurrect':
                    time_arr = event['time'].split(':')
                    curr_time = stats.hms_to_seconds(time_arr[0],
                        time_arr[1], time_arr[2])
                    event['time'] = curr_time
                    res.append(event)
        else:
            for event in self.data_sheet1:
                time_arr = event['time'].split(':')
                curr_time = stats.hms_to_seconds(time_arr[0],
                    time_arr[1], time_arr[2])
                if curr_time >= start_time and curr_time >= end_time \
                and self.event['action'] == 'Resurrect':
                    event['time'] = curr_time
                    res.append(event)
        return res

    def get_suicides(self, start_time=0, end_time=0):
        """Get all suicides in a given time range.
        If start_time == 0 and end_time == 0, return full suicide list.
        Author:
            ForYou
        Args:
            start_time: start of the time range given in seconds
            end_time: end of the time range given in seconds
        Returns:
            A list of all suicides in a given time range.
        """
        res = []
        if end_time == 0 and start_time == 0:
            for event in self.data_sheet1:
                if event['action'] == 'Suicide':
                    time_arr = event['time'].split(':')
                    curr_time = stats.hms_to_seconds(time_arr[0],
                        time_arr[1], time_arr[2])
                    event['time'] = curr_time
                    res.append(event)
        else:
            for event in self.data_sheet1:
                time_arr = event['time'].split(':')
                curr_time = stats.hms_to_seconds(time_arr[0],
                    time_arr[1], time_arr[2])
                if curr_time >= start_time and curr_time >= end_time \
                and self.event['action'] == 'Suicide':
                    event['time'] = curr_time
                    res.append(event)
        return res

    def get_demechs(self, start_time=0, end_time=0):
        """Get all demechs in a given time range.
        If start_time == 0 and end_time == 0, return full demech list.
        Author:
            ForYou
        Args:
            start_time: start of the time range given in seconds
            end_time: end of the time range given in seconds
        Returns:
            A list of all demechs in a given time range.
        """
        res = []
        if end_time == 0 and start_time == 0:
            for event in self.data_sheet1:
                if event['action'] == 'Demech':
                    time_arr = event['time'].split(':')
                    curr_time = stats.hms_to_seconds(time_arr[0],
                        time_arr[1], time_arr[2])
                    event['time'] = curr_time
                    res.append(event)
        else:
            for event in self.data_sheet1:
                time_arr = event['time'].split(':')
                curr_time = stats.hms_to_seconds(time_arr[0],
                    time_arr[1], time_arr[2])
                if curr_time >= start_time and curr_time >= end_time \
                and self.event['action'] == 'Demech':
                    event['time'] = curr_time
                    res.append(event)
        return res

    def get_player_basic_eliminates(self,start_time=0,end_time=0,data=0):
        '''
        获取在原数据基础上返回固定时间段内击杀相关数据粗加工
        Author:
            ForYou
        Args：
        start_time开始时间end_time结束时间data原数据
        Returns：
        同get_init_plarer_basic_data()返回值
        '''
        if data == 0:
            playerArr = self.playerArr
        else:
            playerArr = data
        if end_time == 0 and start_time == 0:
            eliminations = self.elims
        else:
            eliminations = self.get_eliminations(start_time,end_time)
        heros = {'chara':'','Eliminate':0,'assist':0,'Resurrect':0,'die':0,'Suicide':0,'Resurrected':0,'critical die':0,'critical kill':0,'assist die':0,'EliminateDetail':[],'assistDetail':[],'dieDetail':[]}
        for index, value in enumerate(eliminations):
            for index1, value1 in enumerate(playerArr):
                if value1['name'] == value['subject']['player']:
                    playerArr[index1]['totalEliminate'] = playerArr[index1]['totalEliminate']+1
                    if value['critical kill'] =='Y':
                        playerArr[index1]['totalcritical kill'] = playerArr[index1]['totalcritical kill']+1
                    heroEliminate = 0
                    for  index3 , value3 in enumerate(value1['totalEliminateDetail']):
                        if value3['chara'] == value['object']['chara']:
                            heroEliminate = 1
                            playerArr[index1]['totalEliminateDetail'][index3]['num'] = playerArr[index1]['totalEliminateDetail'][index3]['num']+1
                            break
                    if heroEliminate == 0:
                        newheroEliminate = {'chara':value['object']['chara'],'num':1}
                        playerArr[index1]['totalEliminateDetail'].append(newheroEliminate)
                    heroisexsit = 0
                    for  index2, value2 in enumerate(value1['heros']):
                        if value2['chara'] == value['subject']['chara']:
                            heroisexsit = 1
                            playerArr[index1]['heros'][index2]['Eliminate'] = playerArr[index1]['heros'][index2]['Eliminate']+1
                            if value['critical kill'] == 'Y':
                                playerArr[index1]['heros'][index2]['critical kill'] = playerArr[index1]['heros'][index2]['critical kill']+1
                            heroEliminate = 0
                            for  index4 , value4 in enumerate(value1['heros']['EliminateDetail']):
                                if value4['chara'] == value['object']['chara']:
                                    heroEliminate = 1
                                    playerArr[index1]['heros'][index2]['EliminateDetail'][index4]['num'] = playerArr[index1]['heros'][index2]['EliminateDetail'][index4]['num']+1
                                    break
                            if heroEliminate == 0:
                                newheroEliminate = {'chara':value['object']['chara'],'num':1}
                                playerArr[index1]['heros'][index2]['EliminateDetail'].append(newheroEliminate)
                            break
                    if heroisexsit == 0:
                        newhero = deepcopy(heros)
                        newhero['chara'] = value['subject']['chara']
                        newhero['Eliminate'] = 1
                        newheroEliminate = {'chara':value['object']['chara'],'num':1}
                        newhero['EliminateDetail'].append(newheroEliminate)
                        playerArr[index1]['totalhero'] = playerArr[index1]['totalhero'] + 1
                        if value['critical kill'] == 'Y':
                            newhero['critical kill'] = 1
                        playerArr[index1]['heros'].append(newhero)
                totalassistdie = 0
                for assistplayer in value['assist']:
                    if value1['name'] == assist[assistplayer]['player']:
                        totalassistdie = totalassistdie + 1
                        playerArr[index1]['totalassist'] = playerArr[index1]['totalassist']+1
                        heroassist = 0
                        for  index3 , value3 in enumerate(value1['totalassistDetail']):
                            if value3['chara'] == value['object']['chara']:
                                heroassist = 1
                                playerArr[index1]['totalassistDetail'][index3]['num'] = playerArr[index1]['totalassistDetail'][index3]['num']+1
                                break
                        if heroassist == 0:
                            newheroassist = {'chara':value['object']['chara'],'num':1}
                            playerArr[index1]['totalassistDetail'].append(newheroassist)
                        heroisexsit = 0
                        for  index2, value2 in enumerate(value1['heros']):
                            if value2['chara'] == assist[assistplayer]['hero']:
                                heroisexsit = 1
                                playerArr[index1]['heros'][index2]['assist'] = playerArr[index1]['heros'][index2]['assist']+1
                                heroassist = 0
                                for  index4 , value4 in enumerate(value1['heros']['assistDetail']):
                                    if value4['chara'] == value['object']['chara']:
                                        heroassist = 1
                                        playerArr[index1]['heros'][index2]['assistDetail'][index4]['num'] = playerArr[index1]['heros'][index2]['assistDetail'][index4]['num']+1
                                        break
                                if heroassist == 0:
                                    newheroassist = {'chara':value['object']['chara'],'num':1}
                                    playerArr[index1]['heros'][index2]['assistDetail'].append(newheroassist)
                                break
                        if heroisexsit == 0:
                            newhero = deepcopy(heros)
                            newhero['chara'] = assist[assistplayer]['hero']
                            newhero['assist'] = 1
                            newheroassist = {'chara':value['object']['chara'],'num':1}
                            newhero['assistDetail'].append(newheroassist)
                            playerArr[index1]['totalhero'] = playerArr[index1]['totalhero'] + 1
                            playerArr[index1]['heros'].append(newhero)
                if value1['name'] == value['object']['player']:
                    playerArr[index1]['totaldie'] = playerArr[index1]['totaldie'] + 1
                    playerArr[index1]['totalassist die'] = playerArr[index1]['totalassist die'] + totalassistdie
                    if value['critical kill'] == 'Y':
                        playerArr[index1]['totalcritical die'] =playerArr[index1]['totalcritical die'] + 1
                    herodie = 0
                    for  index3 , value3 in enumerate(value1['totaldieDetail']):
                        if value3['chara'] == value['subject']['chara']:
                            herodie = 1
                            playerArr[index1]['totaldieDetail'][index3]['num'] = playerArr[index1]['totaldieDetail'][index3]['num']+1
                            break
                    if herodie == 0:
                        newherodie = {'chara':value['object']['chara'],'num':1}
                        playerArr[index1]['totaldieDetail'].append(newherodie)
                    heroisexsit = 0
                    for  index2, value2 in enumerate(value1['heros']):
                        if value2['chara'] ==  value['object']['chara']:
                            heroisexsit = 1
                            playerArr[index1]['heros'][index2]['die'] = playerArr[index1]['heros'][index2]['die'] + 1
                            playerArr[index1]['heros'][index2]['assist die'] = playerArr[index1]['heros'][index2]['assist die'] + totalassistdie
                            if value['critical kill'] == 'Y':
                                playerArr[index1]['heros'][index2]['critical die'] = playerArr[index1]['heros'][index2]['critical die'] + 1
                            herodie = 0
                            for  index4 , value4 in enumerate(value1['heros']['dieDetail']):
                                if value4['chara'] == value['subject']['chara']:
                                    herodie = 1
                                    playerArr[index1]['heros'][index2]['dieDetail'][index4]['num'] = playerArr[index1]['heros'][index2]['dieDetail'][index4]['num'] + 1
                                    break
                            if herodie == 0:
                                newherodie = {'chara':value['object']['chara'],'num':1}
                                playerArr[index1]['heros'][index2]['dieDetail'].append(newherodie)
                            break
                    if heroisexsit == 0:
                        newhero = deepcopy(heros)
                        newhero['chara'] = value['object']['chara']
                        newhero['die'] = 1
                        newherodie = {'chara':value['subject']['chara'],'num':1}
                        newhero['dieDetail'].append(newherodie)
                        newhero['assist die'] = totalassistdie
                        playerArr[index1]['totalhero'] = playerArr[index1]['totalhero'] + 1
                        if value['critical kill'] == 'Y':
                            newhero['critical die'] = 1
                        playerArr[index1]['heros'].append(newhero)

    def get_player_basic_resurrects(self,start_time=0,end_time=0,data=0):
        '''
        获取在原数据基础上返回固定时间段内复活相关数据粗加工
        Author:
            ForYou
        Args：
        start_time开始时间end_time结束时间data原数据
        Returns：
        同get_init_plarer_basic_data()返回值
        '''
        if data == 0:
            playerArr = self.playerArr
        else:
            playerArr = data
        if end_time == 0 and start_time == 0:
            resurrects = self.resurrects
        else:
            resurrects = self.get_resurrects(start_time,end_time)
        heros = {'chara':'','Eliminate':0,'assist':0,'Resurrect':0,'die':0,'Suicide':0,'Resurrected':0,'critical die':0,'critical kill':0,'assist die':0,'EliminateDetail':[],'assistDetail':[],'dieDetail':[]}
        for index, value in enumerate(resurrects):
            for index1, value1 in enumerate(playerArr):
                if value1['name'] == value['subject']['player']:
                    playerArr[index1]['totalResurrect'] = playerArr[index1]['totalResurrect'] + 1
                    heroisexsit = 0
                    for  index2, value2 in enumerate(value1['heros']):
                        if value2['chara'] ==  value['subject']['chara']:
                            heroisexsit = 1
                            playerArr[index1]['heros'][index2]['Resurrect'] = playerArr[index1]['heros'][index2]['Resurrect'] + 1
                            break
                    if heroisexsit == 0:
                        newhero = deepcopy(heros)
                        newhero['chara'] = value['subject']['chara']
                        newhero['Resurrect'] = 1
                        playerArr[index1]['totalhero'] = playerArr[index1]['totalhero'] + 1
                        playerArr[index1]['heros'].append(newhero)
                if value1['name'] == value['object']['player']:
                    playerArr[index1]['totalResurrected'] = playerArr[index1]['totalResurrected'] + 1
                    heroisexsit = 0
                    for  index2, value2 in enumerate(value1['heros']):
                        if value2['chara'] == value['object']['chara']:
                            heroisexsit = 1
                            playerArr[index1]['heros'][index2]['Resurrected'] = playerArr[index1]['heros'][index2]['Resurrected']+1
                            break
                    if heroisexsit == 0:
                        newhero = deepcopy(heros)
                        newhero['chara'] = value['object']['chara']
                        newhero['Resurrected'] = 1
                        playerArr[index1]['totalhero'] = playerArr[index1]['totalhero'] + 1
                        playerArr[index1]['heros'].append(newhero)

    def get_player_basic_suicides(self,start_time=0,end_time=0,data=0):
        '''
        获取在原数据基础上返回固定时间段内自杀相关数据粗加工
        Author:
            ForYou
        Args：
        start_time开始时间end_time结束时间data原数据
        Returns：
        同get_init_plarer_basic_data()返回值
        '''
        if data == 0:
            playerArr = self.playerArr
        else:
            playerArr = data
        if end_time == 0 and start_time == 0:
            suicides = self.suicides
        else:
            suicides = self.get_suicides(start_time,end_time)
        heros = {'chara':'','Eliminate':0,'assist':0,'Resurrect':0,'die':0,'Suicide':0,'Resurrected':0,'critical die':0,'critical kill':0,'assist die':0,'EliminateDetail':[],'assistDetail':[],'dieDetail':[]}
        for index, value in enumerate(suicides):
            for index1, value1 in enumerate(playerArr):
                if value1['name'] == value['object']['player']:
                    playerArr[index1]['totalSuicide'] = playerArr[index1]['totalSuicide']+1
                    heroisexsit = 0
                    for  index2, value2 in enumerate(value1['heros']):
                        if value2['chara'] == value['object']['chara']:
                            heroisexsit = 1
                            playerArr[index1]['heros'][index2]['Suicide'] = playerArr[index1]['heros'][index2]['Suicide'] + 1
                            break
                    if heroisexsit == 0:
                        newhero = deepcopy(heros)
                        newhero['chara'] = value['object']['chara']
                        newhero['Suicide'] = 1
                        playerArr[index1]['totalhero'] = playerArr[index1]['totalhero']+1
                        playerArr[index1]['heros'].append(newhero)

    def get_player_basic_demechs(self,start_time=0,end_time=0,data=0):
        '''
        获取在原数据基础上返回固定时间段内机甲相关数据粗加工
        Author:
            ForYou
        Args：
        start_time开始时间end_time结束时间data原数据
        Returns：
        同get_init_plarer_basic_data()返回值
        '''
        if data == 0:
            playerArr = self.playerArr
        else:
            playerArr = data
        if end_time == 0 and start_time == 0:
            demechs = self.demechs
        else:
            demechs = self.get_suicides(start_time,end_time)
        heros = {'chara':'','Eliminate':0,'assist':0,'Resurrect':0,'die':0,'Suicide':0,'Resurrected':0,'critical die':0,'critical kill':0,'assist die':0,'EliminateDetail':[],'assistDetail':[],'dieDetail':[]}
        for index, value in enumerate(demechs):
            for index1, value1 in enumerate(playerArr):
                if value1['name'] == value['subject']['player']:
                    playerArr[index1]['totalDemech'] = playerArr[index1]['totalDemech']+1
                    if value['critical kill'] == 'Y':
                        playerArr[index1]['totalDemechcritical kill'] = playerArr[index1]['totalDemechcritical kill']+1
                    heroisexsit = 0
                    for  index2, value2 in enumerate(value1['heros']):
                        if value2['chara'] ==  value['subject']['chara']:
                            heroisexsit = 1
                            playerArr[index1]['heros'][index2]['Demech'] = playerArr[index1]['heros'][index2]['Demech'] + 1
                            if value['critical kill'] == 'Y':
                                playerArr[index1]['heros'][index2]['Demechcritical kill'] = playerArr[index1]['heros'][index2]['Demechcritical kill']+1
                            break
                    if heroisexsit == 0:
                        newhero = deepcopy(heros)
                        newhero['chara'] = value['subject']['chara']
                        newhero['Demech'] = 1
                        playerArr[index1]['totalhero'] = playerArr[index1]['totalhero']+1
                        if value['critical kill'] == 'Y':
                            newhero['Demechcritical kill'] = 1
                        playerArr[index1]['heros'].append(newhero)
                totalDemechassistdie = 0
                for assistplayer in value['assist']:
                    if value1['name'] == assist[assistplayer]['player']:
                        totalDemechassistdie = totalDemechassistdie + 1
                        playerArr[index1]['totalDemechassist'] = playerArr[index1]['totalDemechassist'] + 1
                        heroisexsit = 0
                        for  index2, value2 in enumerate(value1['heros']):
                            if value2['chara'] ==  assist[assistplayer]['hero']:
                                heroisexsit = 1
                                playerArr[index1]['heros'][index2]['Demechassist'] = playerArr[index1]['heros'][index2]['Demechassist'] + 1
                                break
                        if heroisexsit == 0:
                            newhero = deepcopy(heros)
                            newhero['chara'] = assist[assistplayer]['hero']
                            newhero['Demechassist'] = 1
                            playerArr[index1]['totalhero'] = playerArr[index1]['totalhero'] + 1
                            playerArr[index1]['heros'].append(newhero)
                if value1['name'] == value['object']['player']:
                    playerArr[index1]['totalDemechdie'] = playerArr[index1]['totalDemechdie'] + 1
                    playerArr[index1]['totalDemechassist die'] = playerArr[index1]['totalDemechassist die']+totalDemechassistdie
                    if value['critical kill'] == 'Y':
                        playerArr[index1]['totalDemechcritical die'] = playerArr[index1]['totalDemechcritical die'] + 1
                    heroisexsit = 0
                    for  index2, value2 in enumerate(value1['heros']):
                        if value2['chara'] ==  value['object']['chara']:
                            heroisexsit = 1
                            playerArr[index1]['heros'][index2]['Demechdie'] = playerArr[index1]['heros'][index2]['Demechdie'] + 1
                            playerArr[index1]['heros'][index2]['Demechassist die'] = playerArr[index1]['heros'][index2]['Demechassist die'] + totalDemechassistdie
                            if value['critical kill'] == 'Y':
                                playerArr[index1]['heros'][index2]['Demechcritical die'] =playerArr[index1]['heros'][index2]['Demechcritical die'] + 1
                            break
                    if heroisexsit == 0:
                        newhero = deepcopy(heros)
                        newhero['chara'] = value['object']['chara']
                        newhero['Demechdie'] = 1
                        newhero['Demechassist die'] = totalDemechassistdie
                        playerArr[index1]['totalhero'] = playerArr[index1]['totalhero'] + 1
                        if value['critical kill'] == 'Y':
                            newhero['Demechcritical die'] = 1
                        playerArr[index1]['heros'].append(newhero)
