# coding: utf-8
import os
import sys
import zipfile
import json
from copy import deepcopy

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
        self.player_arr = self.get_init_player_basic_data()

    def _get_actions(self, action,start_time=0, end_time=0,data=0):
        """通过action字段获取相应事件段里面的action列表
        Author:
            ForYou
        Args:
            action:事件类型
            start_time: start of the time range given in seconds
            end_time: end of the time range given in seconds
        Returns:
            对应action的事件list
        """
        if data == 0:
            res =[]
        if end_time == 0 and start_time == 0:
            for event in self.data_sheet1:
                if event['action'] == action:
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
                and self.event['action'] == action:
                    event['time'] = curr_time
                    res.append(event)
        return res


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
        return self._get_actions('Eliminate',start_time,end_time)

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
        return self._get_actions('Eliminate',start_time,end_time,data)

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
        return self._get_actions('Resurrect',start_time,end_time)

    def get_resurrects_incremented(self, data, start_time, end_time):
        """Append resurrects in given time range onto existed array
        
        Author:
            ForYou
        Args:
            data: list of given resurrects data
            start_time: start of the time range given in seconds
            end_time: end of the time range given in seconds
        Returns:
            A list of all resurrects in a given time range appended to original list.
        """
        return self._get_actions('Resurrect',start_time,end_time,data)

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
        return self._get_actions('Suicide',start_time,end_time)

    def get_suicides_incremented(self, data, start_time, end_time):
        """Append suicides in given time range onto existed array
        
        Author:
            ForYou
        Args:
            data: list of given suicides data
            start_time: start of the time range given in seconds
            end_time: end of the time range given in seconds
        Returns:
            A list of all suicides in a given time range appended to original list.
        """
        return self._get_actions('Suicide',start_time,end_time,data)

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
        return self._get_actions('Demech',start_time,end_time)

    def get_demechs_incremented(self, data, start_time, end_time):
        """Append demechs in given time range onto existed array
        
        Author:
            ForYou
        Args:
            data: list of given demechs data
            start_time: start of the time range given in seconds
            end_time: end of the time range given in seconds
        Returns:
            A list of all demechs in a given time range appended to original list.
        """
        return self._get_actions('Demech',start_time,end_time,data)

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

    def get_init_player_basic_data(self):
        '''
        根据data_sheet2初始化各个选手基本数据
        Author:
            ForYou
        Args：
        None
        Returns：
        player_arr：以选手player为单位的数组，共12个，每个player中包括以下内容：
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
        player_arr = []
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
                player_arr.append(player)
        return player_arr

    def get_player_basic_eliminates(self,start_time=0,end_time=0,data=0):
        '''
        获取在原数据基础上返回固定时间段内击杀相关数据粗加工
        Author:
            ForYou
        Args：
        start_time开始时间end_time结束时间data原数据
        Returns：
        同get_init_player_basic_data()返回值
        '''
        #提供了data原有数据就在原有数据累加，没有提供则在初始化的选手信息self.player_arr上添加
        if data == 0:
            player_arr = self.player_arr
        else:
            player_arr = data
        #提供了开始和结束时间则取时间内的击杀事件加工，没有提供则默认全部击杀事件
        if end_time == 0 and start_time == 0:
            eliminations = self.elims
        else:
            eliminations = self.get_eliminations(start_time,end_time)
        heros = {'chara':'','Eliminate':0,'assist':0,'Resurrect':0,'die':0,'Suicide':0,'Resurrected':0,'critical die':0,'critical kill':0,'assist die':0,'EliminateDetail':[],'assistDetail':[],'dieDetail':[]}
        #遍历提供的击杀事件，从其中提取信息
        for index, value in enumerate(eliminations):
            #遍历选手列表，找到信息对应的选手，循环中主要处理三类信息 1：击杀者  2：助攻  3：被击杀者
            for playerindex, playervalue in enumerate(player_arr):
                # 1：击杀者相关信息(1a 总击杀 1b爆头总击杀 1c 总击杀明细 1d 使用英雄击杀相关)
                if playervalue['name'] == value['subject']['player']:
                    # 1a 总击杀
                    player_arr[playerindex]['totalEliminate'] +=1
                    # 1b 爆头总击杀
                    if value['critical kill'] =='Y':
                        player_arr[playerindex]['totalcritical kill'] += 1
                    # 1c 总击杀明细 (敌方哪个英雄 几次)
                    hero_eliminate = 0
                    for  obj_hero_index , obj_hero_value in enumerate(playervalue['totalEliminateDetail']):
                        if obj_hero_value['chara'] == value['object']['chara']:
                            hero_eliminate = 1
                            player_arr[playerindex]['totalEliminateDetail'][obj_hero_index]['num'] += 1
                            break
                    # 击杀明细列表中 无此英雄则新增
                    if hero_eliminate == 0:
                        newhero_eliminate = {'chara':value['object']['chara'],'num':1}
                        player_arr[playerindex]['totalEliminateDetail'].append(newhero_eliminate)
                    # 1d 使用英雄击杀相关
                    heroisexsit = 0
                    #遍历已使用英雄
                    for  used_hero_index, used_hero_value in enumerate(playervalue['heros']):
                        #和选手总击杀类似，这里处理选手不同英雄的击杀数据
                        if used_hero_value['chara'] == value['subject']['chara']:
                            heroisexsit = 1
                            player_arr[playerindex]['heros'][used_hero_index]['Eliminate'] += 1
                            if value['critical kill'] == 'Y':
                                player_arr[playerindex]['heros'][used_hero_index]['critical kill'] += 1
                            hero_eliminate = 0
                            #击杀敌方英雄详情
                            for  hero_action_detail_index , hero_action_detail_value in enumerate(playervalue['heros']['EliminateDetail']):
                                if hero_action_detail_value['chara'] == value['object']['chara']:
                                    hero_eliminate = 1
                                    player_arr[playerindex]['heros'][used_hero_index]['EliminateDetail'][hero_action_detail_index]['num'] += 1
                                    break
                            if hero_eliminate == 0:
                                newhero_eliminate = {'chara':value['object']['chara'],'num':1}
                                player_arr[playerindex]['heros'][used_hero_index]['EliminateDetail'].append(newhero_eliminate)
                            break
                    #未使用过此英雄则新增
                    if heroisexsit == 0:
                        newhero = deepcopy(heros)
                        newhero['chara'] = value['subject']['chara']
                        newhero['Eliminate'] = 1
                        newhero_eliminate = {'chara':value['object']['chara'],'num':1}
                        newhero['EliminateDetail'].append(newhero_eliminate)
                        player_arr[playerindex]['totalhero'] +=  1
                        if value['critical kill'] == 'Y':
                            newhero['critical kill'] = 1
                        player_arr[playerindex]['heros'].append(newhero)
                # 2：助攻相关信息 total_assist_die字段记录这次击杀事件造成几个助攻，累加在选手的assist die和totalassist die上，assist die/die 可以看出敌方队伍集火目标
                total_assist_die = 0
                for assistplayer in value['assist']:
                    #遍历助攻列表 处理选手的 2a总助攻 2b总助攻明细 2c不同英雄助攻信息 
                    if playervalue['name'] == assist[assistplayer]['player']:
                        total_assist_die += 1
                        # 2a 总助攻
                        player_arr[playerindex]['totalassist'] += 1
                        # 2b 总助攻明细
                        heroassist = 0
                        for  obj_hero_index , obj_hero_value in enumerate(playervalue['totalassistDetail']):
                            if obj_hero_value['chara'] == value['object']['chara']:
                                heroassist = 1
                                player_arr[playerindex]['totalassistDetail'][obj_hero_index]['num'] += 1
                                break
                        if heroassist == 0:
                            newheroassist = {'chara':value['object']['chara'],'num':1}
                            player_arr[playerindex]['totalassistDetail'].append(newheroassist)
                        # 2c 遍历英雄更新助攻信息
                        heroisexsit = 0
                        for  used_hero_index, used_hero_value in enumerate(playervalue['heros']):
                            if used_hero_value['chara'] == assist[assistplayer]['hero']:
                                heroisexsit = 1
                                player_arr[playerindex]['heros'][used_hero_index]['assist'] += 1
                                #助攻击杀敌方英雄信息
                                heroassist = 0
                                for  hero_action_detail_index , hero_action_detail_value in enumerate(playervalue['heros']['assistDetail']):
                                    if hero_action_detail_value['chara'] == value['object']['chara']:
                                        heroassist = 1
                                        player_arr[playerindex]['heros'][used_hero_index]['assistDetail'][hero_action_detail_index]['num'] += 1
                                        break
                                if heroassist == 0:
                                    newheroassist = {'chara':value['object']['chara'],'num':1}
                                    player_arr[playerindex]['heros'][used_hero_index]['assistDetail'].append(newheroassist)
                                break
                        #使用英雄不存在则新增
                        if heroisexsit == 0:
                            newhero = deepcopy(heros)
                            newhero['chara'] = assist[assistplayer]['hero']
                            newhero['assist'] = 1
                            newheroassist = {'chara':value['object']['chara'],'num':1}
                            newhero['assistDetail'].append(newheroassist)
                            player_arr[playerindex]['totalhero'] +=  1
                            player_arr[playerindex]['heros'].append(newhero)
                # 3：被击杀者信息(3a 总死亡 3b总被助攻 3c 总被爆头击杀 3d 被击杀明细 3e 被击杀英雄相关)
                if playervalue['name'] == value['object']['player']:
                    #3a 总死亡
                    player_arr[playerindex]['totaldie'] += 1
                    #3b 总被助攻数
                    player_arr[playerindex]['totalassist die'] += total_assist_die
                    #3c 总被爆头击杀数
                    if value['critical kill'] == 'Y':
                        player_arr[playerindex]['totalcritical die'] += 1
                    #3d 被击杀明细 (造成击杀的敌方英雄构成及次数)
                    herodie = 0
                    for  obj_hero_index , obj_hero_value in enumerate(playervalue['totaldieDetail']):
                        if obj_hero_value['chara'] == value['subject']['chara']:
                            herodie = 1
                            player_arr[playerindex]['totaldieDetail'][obj_hero_index]['num'] += 1
                            break
                    if herodie == 0:
                        newherodie = {'chara':value['subject']['chara'],'num':1}
                        player_arr[playerindex]['totaldieDetail'].append(newherodie)
                    #3e 被击杀英雄(死亡构成) 数据结构与总数据类似
                    heroisexsit = 0
                    for  used_hero_index, used_hero_value in enumerate(playervalue['heros']):
                        if used_hero_value['chara'] ==  value['object']['chara']:
                            heroisexsit = 1
                            player_arr[playerindex]['heros'][used_hero_index]['die'] += 1
                            player_arr[playerindex]['heros'][used_hero_index]['assist die'] += total_assist_die
                            if value['critical kill'] == 'Y':
                                player_arr[playerindex]['heros'][used_hero_index]['critical die'] += 1
                            herodie = 0
                            for  hero_action_detail_index , hero_action_detail_value in enumerate(playervalue['heros']['dieDetail']):
                                if hero_action_detail_value['chara'] == value['subject']['chara']:
                                    herodie = 1
                                    player_arr[playerindex]['heros'][used_hero_index]['dieDetail'][hero_action_detail_index]['num'] += 1
                                    break
                            if herodie == 0:
                                newherodie = {'chara':value['subject']['chara'],'num':1}
                                player_arr[playerindex]['heros'][used_hero_index]['dieDetail'].append(newherodie)
                            break
                    #被击杀的英雄不存在则新增
                    if heroisexsit == 0:
                        newhero = deepcopy(heros)
                        newhero['chara'] = value['object']['chara']
                        newhero['die'] = 1
                        newherodie = {'chara':value['subject']['chara'],'num':1}
                        newhero['dieDetail'].append(newherodie)
                        newhero['assist die'] = total_assist_die
                        player_arr[playerindex]['totalhero'] += 1
                        if value['critical kill'] == 'Y':
                            newhero['critical die'] = 1
                        player_arr[playerindex]['heros'].append(newhero)

    def get_player_basic_resurrects(self,start_time=0,end_time=0,data=0):
        '''
        获取在原数据基础上返回固定时间段内复活相关数据粗加工
        Author:
            ForYou
        Args：
        start_time开始时间end_time结束时间data原数据
        Returns：
        同get_init_player_basic_data()返回值
        '''
        #提供了data原有数据就在原有数据累加，没有提供则在初始化的选手信息self.player_arr上添加
        if data == 0:
            player_arr = self.player_arr
        else:
            player_arr = data
        #提供了开始和结束时间则取时间内的复活事件加工，没有提供则默认全部复活事件
        if end_time == 0 and start_time == 0:
            resurrects = self.resurrects
        else:
            resurrects = self.get_resurrects(start_time,end_time)
        heros = {'chara':'','Eliminate':0,'assist':0,'Resurrect':0,'die':0,'Suicide':0,'Resurrected':0,'critical die':0,'critical kill':0,'assist die':0,'EliminateDetail':[],'assistDetail':[],'dieDetail':[]}
        #遍历提供的复活事件
        for index, value in enumerate(resurrects):
            #遍历选手列表 更新 1 复活数据  2 被复活数据
            for playerindex, playervalue in enumerate(player_arr):
                #复活数据 和击杀数据一样做了英雄分组 1是为了保持数据格式的一致性，2是防止出另外具有复活技能的英雄 
                if playervalue['name'] == value['subject']['player']:
                    player_arr[playerindex]['totalResurrect'] += 1
                    heroisexsit = 0
                    for  used_hero_index, used_hero_value in enumerate(playervalue['heros']):
                        if used_hero_value['chara'] ==  value['subject']['chara']:
                            heroisexsit = 1
                            player_arr[playerindex]['heros'][used_hero_index]['Resurrect'] += 1
                            break
                    if heroisexsit == 0:
                        newhero = deepcopy(heros)
                        newhero['chara'] = value['subject']['chara']
                        newhero['Resurrect'] = 1
                        player_arr[playerindex]['totalhero'] += 1
                        player_arr[playerindex]['heros'].append(newhero)
                #被复活数据
                if playervalue['name'] == value['object']['player']:
                    player_arr[playerindex]['totalResurrected'] += 1
                    heroisexsit = 0
                    for  used_hero_index, used_hero_value in enumerate(playervalue['heros']):
                        if used_hero_value['chara'] == value['object']['chara']:
                            heroisexsit = 1
                            player_arr[playerindex]['heros'][used_hero_index]['Resurrected'] += 1
                            break
                    if heroisexsit == 0:
                        newhero = deepcopy(heros)
                        newhero['chara'] = value['object']['chara']
                        newhero['Resurrected'] = 1
                        player_arr[playerindex]['totalhero'] += 1
                        player_arr[playerindex]['heros'].append(newhero)

    def get_player_basic_suicides(self,start_time=0,end_time=0,data=0):
        '''
        获取在原数据基础上返回固定时间段内自杀相关数据粗加工
        Author:
            ForYou
        Args：
        start_time开始时间end_time结束时间data原数据
        Returns：
        同get_init_player_basic_data()返回值
        '''
        #提供了data原有数据就在原有数据累加，没有提供则在初始化的选手信息self.player_arr上添加
        if data == 0:
            player_arr = self.player_arr
        else:
            player_arr = data
        #提供了开始和结束时间则取时间内的自杀事件加工，没有提供则默认全部自杀事件
        if end_time == 0 and start_time == 0:
            suicides = self.suicides
        else:
            suicides = self.get_suicides(start_time,end_time)
        heros = {'chara':'','Eliminate':0,'assist':0,'Resurrect':0,'die':0,'Suicide':0,'Resurrected':0,'critical die':0,'critical kill':0,'assist die':0,'EliminateDetail':[],'assistDetail':[],'dieDetail':[]}
        #遍历提供的自杀事件
        for index, value in enumerate(suicides):
            #遍历选手列表 更新自杀数据
            for playerindex, playervalue in enumerate(player_arr):
                if playervalue['name'] == value['object']['player']:
                    player_arr[playerindex]['totalSuicide'] += 1
                    heroisexsit = 0
                    for  used_hero_index, used_hero_value in enumerate(playervalue['heros']):
                        if used_hero_value['chara'] == value['object']['chara']:
                            heroisexsit = 1
                            player_arr[playerindex]['heros'][used_hero_index]['Suicide'] += 1
                            break
                    if heroisexsit == 0:
                        newhero = deepcopy(heros)
                        newhero['chara'] = value['object']['chara']
                        newhero['Suicide'] = 1
                        player_arr[playerindex]['totalhero'] += 1
                        player_arr[playerindex]['heros'].append(newhero)

    def get_player_basic_demechs(self,start_time=0,end_time=0,data=0):
        '''
        获取在原数据基础上返回固定时间段内机甲相关数据粗加工
        Author:
            ForYou
        Args：
        start_time开始时间end_time结束时间data原数据
        Returns：
        同get_init_player_basic_data()返回值
        '''
        #提供了data原有数据就在原有数据累加，没有提供则在初始化的选手信息self.player_arr上添加
        if data == 0:
            player_arr = self.player_arr
        else:
            player_arr = data
        #提供了开始和结束时间则取时间内的击杀机甲事件加工，没有提供则默认全部击杀机甲事件
        if end_time == 0 and start_time == 0:
            demechs = self.demechs
        else:
            demechs = self.get_suicides(start_time,end_time)
        heros = {'chara':'','Eliminate':0,'assist':0,'Resurrect':0,'die':0,'Suicide':0,'Resurrected':0,'critical die':0,'critical kill':0,'assist die':0,'EliminateDetail':[],'assistDetail':[],'dieDetail':[]}
        #遍历提供的击杀机甲事件 此函数与击杀事件get_player_basic_eliminates类似，注释会从简
        for index, value in enumerate(demechs):
            #遍历选手列表 处理选手的 1 拆机甲 2 助攻拆机甲 3 被拆机甲
            for playerindex, playervalue in enumerate(player_arr):
                # 1：拆机甲相关数据 拆机甲总数 爆头拆机甲总数  不同英雄拆机甲数据
                if playervalue['name'] == value['subject']['player']:
                    player_arr[playerindex]['totalDemech'] += 1
                    if value['critical kill'] == 'Y':
                        player_arr[playerindex]['totalDemechcritical kill'] += 1
                    heroisexsit = 0
                    for  used_hero_index, used_hero_value in enumerate(playervalue['heros']):
                        if used_hero_value['chara'] ==  value['subject']['chara']:
                            heroisexsit = 1
                            player_arr[playerindex]['heros'][used_hero_index]['Demech'] += 1
                            if value['critical kill'] == 'Y':
                                player_arr[playerindex]['heros'][used_hero_index]['Demechcritical kill'] += 1
                            break
                    if heroisexsit == 0:
                        newhero = deepcopy(heros)
                        newhero['chara'] = value['subject']['chara']
                        newhero['Demech'] = 1
                        player_arr[playerindex]['totalhero'] += 1
                        if value['critical kill'] == 'Y':
                            newhero['Demechcritical kill'] = 1
                        player_arr[playerindex]['heros'].append(newhero)
                #2：助攻拆机甲数据 遍历助攻列表 处理选手的 总助攻  不同英雄助攻信息
                total_demech_assistdie = 0
                for assistplayer in value['assist']:
                    if playervalue['name'] == assist[assistplayer]['player']:
                        total_demech_assistdie += 1
                        player_arr[playerindex]['totalDemechassist'] += 1
                        heroisexsit = 0
                        for  used_hero_index, used_hero_value in enumerate(playervalue['heros']):
                            if used_hero_value['chara'] == assist[assistplayer]['hero']:
                                heroisexsit = 1
                                player_arr[playerindex]['heros'][used_hero_index]['Demechassist'] += 1
                                break
                        if heroisexsit == 0:
                            newhero = deepcopy(heros)
                            newhero['chara'] = assist[assistplayer]['hero']
                            newhero['Demechassist'] = 1
                            player_arr[playerindex]['totalhero'] += 1
                            player_arr[playerindex]['heros'].append(newhero)
                #3:被拆机甲信息(总死亡 总被助攻 总被爆头击杀 被击杀英雄此处专指dva)
                if playervalue['name'] == value['object']['player']:
                    player_arr[playerindex]['totalDemechdie'] += 1
                    player_arr[playerindex]['totalDemechassist die'] += total_demech_assistdie
                    if value['critical kill'] == 'Y':
                        player_arr[playerindex]['totalDemechcritical die'] += 1
                    heroisexsit = 0
                    for  used_hero_index, used_hero_value in enumerate(playervalue['heros']):
                        #判断存疑 如果机甲的chara是 meta 这里面需要修改为dva 如果不是meta则不需要修改
                        if used_hero_value['chara'] ==  value['object']['chara']:
                            heroisexsit = 1
                            player_arr[playerindex]['heros'][used_hero_index]['Demechdie'] += 1
                            player_arr[playerindex]['heros'][used_hero_index]['Demechassist die'] += total_demech_assistdie
                            if value['critical kill'] == 'Y':
                                player_arr[playerindex]['heros'][used_hero_index]['Demechcritical die'] += 1
                            break
                    if heroisexsit == 0:
                        newhero = deepcopy(heros)
                        newhero['chara'] = value['object']['chara']
                        newhero['Demechdie'] = 1
                        newhero['Demechassist die'] = total_demech_assistdie
                        player_arr[playerindex]['totalhero'] += 1
                        if value['critical kill'] == 'Y':
                            newhero['Demechcritical die'] = 1
                        player_arr[playerindex]['heros'].append(newhero)
