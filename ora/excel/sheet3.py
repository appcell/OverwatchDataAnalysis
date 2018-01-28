# -*- coding:utf-8 -*-
"""
@Author: Rigel
"""
import utils as utils
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


class Sheet:
    def __init__(self, wb, game):
        self.game = game
        self.frames = game.frames
        self.sheet = wb['sheet3']
        self.player = None
        self.chara = None
        self.ult_charge = None

    def new(self):
        frames = self.game.frames
        for i, frame in enumerate(frames):
            self._ult_charge_append(frame.players, frame.time)
        #self.save()
        return

    def _ult_charge_append(self, players, time):
        ult_charge_row = [utils.time_format(time)]
        for player in players:
            chara = player.chara
            ult_charge = player.ult_charge
            ult_charge_row += [chara,ult_charge]
        self.sheet.append(ult_charge_row)
        return
