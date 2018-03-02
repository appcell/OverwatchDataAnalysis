# -*- coding:utf-8 -*-
"""
@Author: Rigel
"""
from . import utils
from openpyxl.utils import get_column_letter
from openpyxl.styles import (
    Alignment,
    Font,
    PatternFill,
)
from openpyxl.utils import get_column_letter
from openpyxl.styles import (
    Alignment,
    Font,
    PatternFill,
    Border,
    Side,
)


TITLE = ['time'] + \
        ['player',
         'HP',
         'ult'] * 12


def combine_player_names(name_players_team_left, name_players_team_right):
    return name_players_team_left + name_players_team_right

class Sheet:
    def __init__(self, wb, game):
        self.game = game
        self.frames = game.frames
        self.sheet = wb['sheet3']
        self.player_names = combine_player_names(game.name_players_team_left, game.name_players_team_right)

    def new(self):
        frames = self.game.frames
        self._set_title()
        for i, frame in enumerate(frames):
            self._hp_ult_charge_append(frame.players, frame.time)
        #self.save()
        return

    def _set_title(self):
        for i in range(12):
            TITLE[1 + 3 * i] = self.player_names[i]
        self.sheet.append(TITLE)
        return

    def _hp_ult_charge_append(self, players, time):
        hp_ult_charge_row = [utils.time_format(time)]
        for player in players:
            chara = utils.chara_capitalize(player.chara)
            hp = 0 if player.is_dead else 100  # Only an indication of dead or alive now
            ult_charge = player.ult_charge
            hp_ult_charge_row += [chara, hp, ult_charge]
        self.sheet.append(hp_ult_charge_row)
        return
