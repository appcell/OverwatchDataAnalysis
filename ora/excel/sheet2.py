# -*- coding:utf-8 -*-
"""
@Author: Komorebi 
"""
from utils import (
    capitalize,
    upper,
)
from openpyxl.utils import get_column_letter
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
    col, row = start[0], int(start[1:])
    width = {f(col, i): s for i, s in enumerate([20, 14.25, 14.25, 9.75])}
    height = {row + i: s for i, s in enumerate([18] * len(PLAYER))}
    return width, height


def create_table(start):
    col, row = start[0], int(start[1:])
    config = {
        'player': {s: '{}{}'.format(col, row + i) for i, s in enumerate(PLAYER)},
        'start_chara': {s: '{}{}'.format(f(col, 1), row + i) for i, s in enumerate(START_CHARA)},
        'end_chara': {s: '{}{}'.format(f(col, 2), row + i) for i, s in enumerate(END_CHARA)},
        'ult_number': {s: '{}{}'.format(f(col, 3), row + i) for i, s in enumerate(ULT_NUMBER)},
    }
    return config


t = 'T1'


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
        self.sheet = wb['sheet1']

    def new(self):
        start, end = self.frames[0], self.frames[-1]
        self._append_player(start.players)
        self._append_chara(start.players, 'start')
        self._append_chara(end.players, 'end')
        self._append_ult_number(end.players)
        self._set_cell_team()
        self._set_cell_title()
        self._set_cell_width_and_height()

    def _append_player(self, players):
        for i, player in enumerate(players):
            s = '{:0>2d} {}'.format(i + 1, upper(player.name.encode('utf-8')))
            if i < 6:
                cell = Config.LEFT['player']['player{}'.format(i + 1)]
            else:
                cell = Config.RIGHT['player']['player{}'.format(i - 5)]
            self.set_cell_value(cell, s, 1)

    def _set_cell_team(self):
        team1, team2 = self.frames[0].players[0].team, self.frames[0].players[-1].team
        self.set_cell_value(Config.LEFT['player']['team_name'], team1)
        self.set_cell_value(Config.RIGHT['player']['team_name'], team2)

    def _set_cell_title(self):
        left, right = Config.LEFT, Config.RIGHT
        for c in [left, right]:
            self.set_cell_value(c['start_chara']['title'], '首发阵容')
            self.set_cell_value(c['start_chara']['empty'], '')
            self.set_cell_value(c['end_chara']['title'], '最终阵容')
            self.set_cell_value(c['end_chara']['empty'], '')
            self.set_cell_value(c['ult_number']['title'], '最终能量')
            self.set_cell_value(c['ult_number']['empty'], '')
        self.set_cell_value(left['player']['title'], '战队1 客场')
        self.set_cell_value(right['player']['title'], '战队2 主场')

    def set_cell_value(self, cell, value, flag=0):
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
        for k, v in Config.height.items():
            self.sheet.row_dimensions[k].height = v
        for k, v in Config.width.items():
            self.sheet.column_dimensions[k].width = v

    def _append_chara(self, players, flag):
        key = 'start_chara' if flag == 'start' else 'end_chara'
        for i, player in enumerate(players):
            if i < 6:
                cell = Config.LEFT[key]['chara{}'.format(i + 1)]
            else:
                cell = Config.RIGHT[key]['chara{}'.format(i - 5)]
            self.set_cell_value(cell, capitalize(player.chara), 1)

    def _append_ult_number(self, players):
        for i, player in enumerate(players):
            if i < 6:
                cell = Config.LEFT['ult_number']['number{}'.format(i + 1)]
            else:
                cell = Config.RIGHT['ult_number']['number{}'.format(i - 5)]
            self.set_cell_value(cell, '', 2)
