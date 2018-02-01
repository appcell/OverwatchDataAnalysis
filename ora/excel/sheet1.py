# -*- coding:utf-8 -*-
"""
@Author: Komorebi 
"""
import utils as utils
from openpyxl.utils import get_column_letter
from openpyxl.styles import (
    Alignment,
    Font,
    PatternFill,
)


SUBJECT = [
    'subject player',
    'subject hero',
]

OBJECT = [
    'object player',
    'object hero',
]

SUPPLEMENT = [
    'ability',
    'critical kill',
]

ASSIST = [
    'a player 1',
    'a hero 1',
    'a player 2',
    'a hero 2',
    'a player 3',
    'a hero 3',
    'a player 4',
    'a hero 4',
    'a player 5',
    'a hero 5',
]

TITLE = [
    'time',
    'action',
] + SUBJECT + OBJECT + SUPPLEMENT + ASSIST

PRINT_DATA_FORMAT = {t: i+1 for i, t in enumerate(TITLE + ['comments'])}

TITLE_TOP = [
    '',
    '',
    'subject',
    '',
    'object',
    '',
    '',
    '',
    'assist 1',
    '',
    'assist 2',
    '',
    'assist 3',
    '',
    'assist 4',
    '',
    'assist 5',
    '',
    'comments',
]

DIMENSIONS = {
    'time': 'A',
    'action': 'B',
    'subject player': 'C',
    'subject hero': 'D',
    'object player': 'E',
    'object hero': 'F',
    'ability': 'G',
    'critical kill': 'H',
    'a player 1': 'I',
    'a hero 1': 'J',
    'a player 2': 'K',
    'a hero 2': 'L',
    'a player 3': 'M',
    'a hero 3': 'N',
    'a player 4': 'O',
    'a hero 4': 'P',
    'a player 5': 'Q',
    'a hero 5': 'R',
    'comments': 'S',
}

TITLE_TOP_MERGE_CELL = {
    '': None,
    'subject': '{}1:{}1'.format(DIMENSIONS['subject player'], DIMENSIONS['subject hero']),
    'object': '{}1:{}1'.format(DIMENSIONS['object player'], DIMENSIONS['object hero']),
    'assist 1': '{}1:{}1'.format(DIMENSIONS['a player 1'], DIMENSIONS['a hero 1']),
    'assist 2': '{}1:{}1'.format(DIMENSIONS['a player 2'], DIMENSIONS['a hero 2']),
    'assist 3': '{}1:{}1'.format(DIMENSIONS['a player 3'], DIMENSIONS['a hero 3']),
    'assist 4': '{}1:{}1'.format(DIMENSIONS['a player 4'], DIMENSIONS['a hero 4']),
    'assist 5': '{}1:{}1'.format(DIMENSIONS['a player 5'], DIMENSIONS['a hero 5']),
    'comments': '{}1:{}2'.format(DIMENSIONS['comments'], DIMENSIONS['comments']),
}

PLAYER_WIDTH_CONFIG = {DIMENSIONS['a player {}'.format(i)]: 18 for i in range(1, 6)}
HERO_WIDTH_CONFIG = {DIMENSIONS['a hero {}'.format(i)]: 16 for i in range(1, 6)}
CELL_WIDTH_CONFIG = {
    DIMENSIONS['time']: 16.5,
    DIMENSIONS['action']: 20,
    DIMENSIONS['subject player']: 18,
    DIMENSIONS['subject hero']: 16,
    DIMENSIONS['object player']: 18,
    DIMENSIONS['object hero']: 16,
    DIMENSIONS['ability']: 14.5,
    DIMENSIONS['critical kill']: 14,
    DIMENSIONS['comments']: 45.5,
}
CELL_WIDTH_CONFIG.update(PLAYER_WIDTH_CONFIG)
CELL_WIDTH_CONFIG.update(HERO_WIDTH_CONFIG)


ABILITY_FORMAT = {
    0: 'Plain Attack',
    1: 'Shift',
    2: 'E',
    3: 'Ultimate 1',
    4: 'Ultimate 2',
    5: 'RMB',
    6: 'Passive',
}


def _cell_style():
    """
    sheet1 中 cell 的样式
    :return: None
    """
    d = {
        'font1': {
            'name': 'Microsoft YaHei',
            'size': 12,
            'bold': True,
            'vertAlign': 'baseline',
        },
        'font2': {
            'name': 'Microsoft YaHei',
            'size': 12,
            'bold': True,
            'vertAlign': 'baseline',
            'color': 'FFFFFF',
        },
        'alignment': {
            'horizontal': 'center',
            'vertical': 'center',
            'wrap_text': True,
        },
        'fill': {},
    }
    return d


def set_action(obj):
    """
    通过对 player1、player2 相关的判断来获取 action
    :param obj: killfeed类
    :return: action
    """
    player1, player2 = obj.player1, obj.player2
    if player1['chara'] == 'mercy' and player1['team'] == player2['team']:
        return 'Resurrect'
    elif player2['chara'] == 'meka':
        return 'Demech'
    elif player1['chara'] == 'empty' and player1['team'] == 'empty' and player2['chara'] is not None:
        return "Suicide"
    else:
        return 'Eliminate'


def set_comments(action):
    """
    通过 action 来将相应的信息转换成 comment
    :return: comment
    """
    table = {
        'Resurrect': 'Resurrect',
        'Demech': 'MEKA destroyed',
        'Eliminate': '',
        'Suicide': ''
    }
    return table[action]


def get_player_name(obj, index, charas, charas2):
    """
    通过英雄名以及队伍信息来查找玩家的名字。
    :param obj: 玩家信息
    :param index: 玩家队伍所处的位置， 1~6为左边的队伍, 7~12为右边的队伍。
    :param charas: 存储了当前所有玩家 玩家名、英雄名信息的 list， 格式为 [(player, chara)...]
    :param charas2: 存储了上一帧所有玩家 英雄名信息的list， 格式为[player1, ...] 
    :return: playername
    """
    name, chara = obj['player'], obj['chara']
    if name != 'empty':
        return name
    team_charas = charas[:6] if index <= 5 else charas[6:]
    for n, c in team_charas:
        if chara == c:
            return n

    team_charas2 = charas2[:6] if index <= 5 else charas2[6:]
    for i, c in enumerate(team_charas2):
        if chara == c:
            return team_charas[i][0]
    return None


def get_player_team_index(player_team, team_names):
    """
    获取玩家所在的队伍编号
    :param player_team: 玩家所处的队伍名
    :param team_names: 存储了主队客队队伍名的 dict，key 分别为'left', 'right'
    :return: 0 or 6
    """
    for key in ['left', 'right']:
        if team_names[key] == player_team:
            return 0 if key == 'left' else 6


class Config(object):
    cell_width = CELL_WIDTH_CONFIG
    cell_height = 18
    cell_style = _cell_style()
    merge_cell = TITLE_TOP_MERGE_CELL
    format = PRINT_DATA_FORMAT
    team_colors = {}
    title_top = TITLE_TOP
    title = TITLE
    ability = ABILITY_FORMAT
    peculiar_cell = []


class Save:
    def __init__(self, sheet, data):
        self.sheet = sheet
        self.data = data

    @staticmethod
    def _set_cell_style(cell, title):
        """
        将样式应用到 cell 中
        :param cell: sheet 中的 cell
        :param title: cell 坐标， 如 A1、B2 ..
        :return: None
        """
        style = Config.cell_style
        cell.font = Font(**style['font2']) if title in Config.peculiar_cell else Font(**style['font1'])
        cell.alignment = Alignment(**style['alignment'])
        if title in style['fill'].keys():
            cell.fill = PatternFill(**style['fill'][title])

    def _set_cells_style(self):
        """
        将样式应用到所有 cell 中 
        """
        max_row, max_column = self.sheet.max_row + 1, self.sheet.max_column + 1
        for r in range(1, max_row):
            self.sheet.row_dimensions[r].height = Config.cell_height
            for c in range(1, max_column):
                letter = get_column_letter(c)
                title = letter + str(r)
                self._set_cell_style(self.sheet[title], title)
                self.sheet.column_dimensions[letter].width = Config.cell_width[letter]

    def _set_cells_merge(self):
        """
        合并 cell 
        """
        merge_config = Config.merge_cell
        for key in Config.title_top:
            if merge_config[key] is not None:
                self.sheet.merge_cells(merge_config[key])

    def _append(self):
        """
        将 self.data 中的数据按照时间排序, 并导入到sheet中 
        """
        self.data.sort(key=lambda x: x['_time'])
        for data in self.data:
            if '_$color' in data.keys():
                color = data.pop('_$color')
                for k, v in color.items():
                    title = DIMENSIONS[k] + str(self.sheet.max_row + 1)
                    c, b = v
                    if b:
                        Config.peculiar_cell.append(title)
                    Config.cell_style['fill'][title] = {
                        'fill_type': 'solid',
                        'fgColor': c,
                    }
            self.sheet.append(self._format(data))

    @staticmethod
    def _format(data):
        """
        格式化输出信息
        :param data: {"字段名": value, ...}
        :return: [value, ...]
        """
        data['time'] = utils.time_format(data['time'])
        format_spec = Config.format
        result = [''] * (len(Config.title) + 1)
        for k, v in format_spec.items():
            if k in ['object hero', 'subject hero'] and k in data:
                data[k] = utils.chara_capitalize(data[k])
            if k in data:
                result[v-1] = data[k]

        for i, s in enumerate(result):
            if s == 'empty' or s == 'Empty':
                result[i] = ''
        return result

    def save(self):
        self._append()
        self._set_cells_style()
        self._set_cells_merge()


class Sheet:
    def __init__(self, wb, game):
        self.game = game
        self.sheet = wb['sheet1']
        # 初始化
        self.sheet.append(Config.title_top)
        self.sheet.append(Config.title)
        if self.game.team_colors is None:
            Config.team_colors[self.game.team_names['left']] = utils.to_hex([255, 255, 255])
            Config.team_colors[self.game.team_names['right']] = utils.to_hex([70, 70, 70])
        Config.team_colors[self.game.team_names['left']] = utils.to_hex(self.game.team_colors['left'])
        Config.team_colors[self.game.team_names['right']] = utils.to_hex(self.game.team_colors['right'])

        # 上一帧所有玩家的大招状况
        self.ultimate_status = {i: False for i in range(1, 13)}

        # 上一帧所有玩家的 chara
        self.previous_chara = [player.chara for player in self.game.frames[0].players]
        # 下一帧所有玩家的 chara
        self.next_chara = [player.chara for player in self.game.frames[1].players]

        # 当前所有玩家的 玩家名以及信息， 如[(player, chara), ...]
        self.player_and_chara = []

        self.data = []

    @staticmethod
    def _new_data(data):
        """
        为字典添加 _time key，用来排序
        """
        data['_time'] = data['time']
        return data

    def _append(self, **kwargs):
        """
        将所有数据添加到 self.data 中，以便后续处理
        """
        new_data = self._new_data(kwargs)
        self.data.append(new_data)

    def new(self):
        """
        遍历 frames， 提取相应的信息并保存
        """
        frames = self.game.frames
        for i, frame in enumerate(frames):
            self.player_and_chara = [(player.name, player.chara) for player in frame.players]
            # ultimate detection not working properly
            self._switch_hero_append(frame.players, frame.time, i)
            self._killfeed_append(frame.killfeeds, frame.time)
            self._ultimate_append(frame.players, frame.time)
        self.save()

    def _killfeed_append(self, killfeeds, time):
        """
        往 sheet 加入击杀相关的信息。
        """
        for obj in killfeeds:
            d = {}
            player1, player2 = obj.player1, obj.player2
            d['time'] = time
            d['action'] = set_action(obj)
            d['comments'] = set_comments(d['action'])
            # d['ability'] = Config.ability[obj.ability]
            d['subject hero'] = player1['chara']
            d['subject player'] = (get_player_name(player1,
                                                   get_player_team_index(player1['team'], self.game.team_names),
                                                   self.player_and_chara, self.previous_chara))
            d['object hero'] = player2['chara']
            d['object player'] = (get_player_name(player2,
                                                  get_player_team_index(player2['team'], self.game.team_names),
                                                  self.player_and_chara, self.previous_chara))
            if obj.is_headshot and d['action'] != 'Resurrect':
                d['critical kill'] = 'Y'
                d['PS'] = 'Head Shot'
            d['_$color'] = {}

            for i, p in enumerate([player1, player2]):
                if player2['chara'] != 'empty' and player2['team'] != 'empty':
                    if i == 0 and player1['team'] != 'empty':
                        d['_$color']['subject player'] = Config.team_colors[player1['team']]
                    else:
                        d['_$color']['object player'] = Config.team_colors[player2['team']]

            for i, assist in enumerate(obj.assists):
                d['a player {}'.format(i + 1)] = get_player_name(assist, get_player_team_index(assist['team'], self.game.team_names), self.player_and_chara, self.previous_chara)
                d['a hero {}'.format(i + 1)] = utils.chara_capitalize(assist['chara'])
                if assist['player'] != 'empty':
                    d['_$color']['a player {}'.format(i + 1)] = Config.team_colors[assist['team']]
            if (d['object player']) is not None:
                self._append(**d)

    def _ultimate_append(self, players, time):
        """
        判断此时的大招是否为刚充满/释放，并将刚充满/释放大招的选手名输出
        """
        status = self.ultimate_status
        for player in players:
            if player.is_dead:
                continue
            d = {
                'time': time,
                'subject player': player.name,
                'subject hero': player.chara,
                '_$color': {
                    'subject player': Config.team_colors[player.team]
                }
            }
            index = player.index + 1
            # TODO 判断是否为小dva，小dva死的情况下把对应的大招状态清空
            # 小dva活着的情况下判断is_ult_ready。
            if player.is_ult_ready and not status[index]:
                status[index] = True
                d['action'] = 'Ult ready'
                self._append(**d)
            elif not player.is_ult_ready and status[index]:
                status[index] = False
                d['action'] = 'Ult used'
                self._append(**d)

    def _switch_hero_append(self, players, time, index):
        """
        通过跟 self.previous_chara 的比对来判定玩家是否更换英雄
        同时这个函数维护着
        self.previous_chara 以及 self.next_chara
        作者目前没想到好的方法 把这个函数功能拆分成 
        1. 维护上面2个 list
        2. 通过上面2个 list以及当前英雄list 来判断英雄是否更换
        
        :param players: 12个player类构成的 list ， 对应12个玩家
        :param time: 当前时间
        :param index: frames 中的第n个 frame
        """
        frames = self.game.frames
        length = len(frames)
        if index == 0:
            return
        elif index >= length - 2:
            return
        else:
            for i, player in enumerate(players):
                top_chara = self.previous_chara[i]
                next_chara = self.next_chara[i]
                if player.is_dead:
                    continue
                elif top_chara != player.chara:
                    if top_chara == next_chara:
                        self.next_chara[i] = frames[index + 2].players[i].chara
                        continue
                    elif player.chara == next_chara:
                        d = {
                            'time': time - 2,
                            'action': 'Hero switch',
                            'subject player': player.name,
                            'subject hero': player.chara,
                            'comments': 'Switch from {} to {}'.format(utils.chara_capitalize(top_chara), utils.chara_capitalize(player.chara)),

                            '_$color': {
                                'subject player': Config.team_colors[player.team],
                            }
                        }
                        self._append(**d)
                        self.previous_chara[i] = player.chara
                        self.next_chara[i] = frames[index + 1].players[i].chara

    def get_end_charas(self):
        return [Chara(chara) for chara in self.previous_chara]

    def save(self):
        """
        对 sheet 中单元格应用样式并保存
        :return: None
        """
        Save(self.sheet, self.data).save()


class Chara(object):
    def __init__(self, chara):
        self.chara = chara
