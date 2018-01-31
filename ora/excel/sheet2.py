# -*- coding:utf-8 -*-
"""
@Author: Komorebi 
"""
from utils import (
    chara_capitalize,
    upper,
)
from openpyxl.styles import (
    Alignment,
    Font,
    PatternFill,
    Border,
    Side,
)


PLAYER = [
    'title',
    'team_name',
    'player1',
    'player2',
    'player3',
    'player4',
    'player5',
    'player6',
]

START_CHARA = [
    'title',
    'empty',
    'chara1',
    'chara2',
    'chara3',
    'chara4',
    'chara5',
    'chara6',
]

END_CHARA = [
    'title',
    'empty',
    'chara1',
    'chara2',
    'chara3',
    'chara4',
    'chara5',
    'chara6',
]

ULT_NUMBER = [
    'title',
    'empty',
    'number1',
    'number2',
    'number3',
    'number4',
    'number5',
    'number6',
]


def f(x, i):
    return chr(ord(x) + i)


def cell_width_and_height(start):
    """
    从 start 开始单元格的宽高
    :param start: 起始坐标 如 A1、 B1
    :return: {'A': width, ...}, {1: 18, ...}
    """
    col, row = start[0], int(start[1:])
    width = {f(col, i): s for i, s in enumerate([20, 14.25, 14.25, 9.75])}
    height = {row + i: s for i, s in enumerate([18] * len(PLAYER))}
    return width, height


def create_table(start):
    """
    通过起点 生成矩形的 cells 
    :param start: 起始坐标 如 A1、 B1
    :return: cells 坐标信息
    """
    col, row = start[0], int(start[1:])
    config = {
        'player': {s: col + str(row + i) for i, s in enumerate(PLAYER)},
        'start_chara': {s: f(col, 1) + str(row + i) for i, s in enumerate(START_CHARA)},
        'end_chara': {s: f(col, 2) + str(row + i) for i, s in enumerate(END_CHARA)},
        'ult_number': {s: f(col, 3) + str(row + i) for i, s in enumerate(ULT_NUMBER)},
    }
    return config


t = 'C3'


class Config(object):
    LEFT = create_table(t)
    RIGHT = create_table('{}{}'.format(t[0], int(t[1:]) + 8))
    font = Font(name='Microsoft YaHei',
                size=12,
                bold=True,
                vertAlign='baseline',
                color='44546A',
                )
    fill = PatternFill(fgColor='D9E1F2',
                       fill_type='solid',
                       )
    border = Border(
        left=Side(style='thin',
                  color='FF000000'),
        bottom=Side(style='thin',
                    color='FF000000'),
    )
    width, height = cell_width_and_height(t)


class Sheet:
    def __init__(self, wb, game):
        self.frames = game.frames
        self.sheet = wb['sheet2']

    def new(self, end_charas):
        start, end = self.frames[0], self.frames[-1]
        self._append_player(start.players)
        self._append_chara(start.players, 'start')
        self._append_chara(end_charas, 'end')
        self._append_ult_number(end.players)
        self._set_cell_team()
        self._set_cell_title()
        self._set_cell_width_and_height()

    def _append_player(self, players):
        """
        将玩家名字导入到 sheet 中 
        """
        for i, player in enumerate(players):
            s = '{:0>2d} {}'.format(i + 1, upper(player.name.encode('utf-8')))
            if i < 6:
                cell = Config.LEFT['player']['player{}'.format(i + 1)]
            else:
                cell = Config.RIGHT['player']['player{}'.format(i - 5)]
            self.set_cell_value(cell, s, 1)

    def _set_cell_team(self):
        """
        将队伍信息导入到 sheet 中 
        """
        team1, team2 = self.frames[0].players[0].team, self.frames[0].players[-1].team
        self.set_cell_value(Config.LEFT['player']['team_name'], team1)
        self.set_cell_value(Config.RIGHT['player']['team_name'], team2)

    def _set_cell_title(self):
        """
        将基本信息导入到 sheet 中 
        """
        left, right = Config.LEFT, Config.RIGHT
        for c in [left, right]:
            self.set_cell_value(c['start_chara']['title'], 'Starting lineup')
            self.set_cell_value(c['start_chara']['empty'], '')
            self.set_cell_value(c['end_chara']['title'], 'Final lineup')
            self.set_cell_value(c['end_chara']['empty'], '')
            self.set_cell_value(c['ult_number']['title'], 'Final ult charge')
            self.set_cell_value(c['ult_number']['empty'], '')
        self.set_cell_value(left['player']['title'], 'Team A (away)')
        self.set_cell_value(right['player']['title'], 'Team B (home)')

    def set_cell_value(self, cell, value, flag=0):
        """
        给 cell 设置值，并应用样式
        :param cell: 坐标，如 A1、B1
        :param value: value
        :param flag: 对齐的样式
        """
        self.sheet[cell].value = value
        self.sheet[cell].font = Config.font
        self.sheet[cell].fill = Config.fill
        self.sheet[cell].border = Config.border
        o = {
            0: {'horizontal': 'center',
                'vertical': 'center',
                },
            1: {'horizontal': 'left',
                'vertical': 'center',
                },
            2: {
                'horizontal': 'right',
                'vertical': 'center',
            }
        }
        self.sheet[cell].alignment = Alignment(**o.get(flag))

    def _set_cell_width_and_height(self):
        """
        设置 cell 宽高
        """
        for k, v in Config.height.items():
            self.sheet.row_dimensions[k].height = v
        for k, v in Config.width.items():
            self.sheet.column_dimensions[k].width = v

    def _append_chara(self, players, flag):
        """
        添加 player 的 chara 信息
        :param players: 12个 player类组成的 list
        :param flag: 是否为起点
        """
        key = 'start_chara' if flag == 'start' else 'end_chara'
        for i, player in enumerate(players):
            if i < 6:
                cell = Config.LEFT[key]['chara{}'.format(i + 1)]
            else:
                cell = Config.RIGHT[key]['chara{}'.format(i - 5)]
            self.set_cell_value(cell, chara_capitalize(player.chara), 1)

    def _append_ult_number(self, players):
        """
        导入最终大招能量
        """
        for i, player in enumerate(players):
            if i < 6:
                cell = Config.LEFT['ult_number']['number{}'.format(i + 1)]
            else:
                cell = Config.RIGHT['ult_number']['number{}'.format(i - 5)]
            self.set_cell_value(cell, '', 2)
