"""
@Author: Komorebi 
"""
from openpyxl import Workbook
from .sheet1 import Sheet as Sheet1
from .sheet2 import Sheet as Sheet2
from .sheet3 import Sheet as Sheet3


def create_sheet():
    wb = Workbook()
    wb.active.title = 'sheet1'
    wb.create_sheet('sheet2')
    wb.create_sheet('sheet3')
    return wb


class Excel(object):
    def __init__(self, game):
        self._wb = create_sheet()
        self.game = game
        self.sheet1 = Sheet1(self._wb, game)
        self.sheet2 = Sheet2(self._wb, game)
        self.sheet3 = Sheet3(self._wb, game)

    def save(self):
        self.sheet1.new()
        self.sheet2.new()
        self.sheet3.new()
        self._wb.save(self.game.output_path)
        if self.game.json:
            self.json()

    def json(self):
        file, _ = self.game.output_path.split('.')
        self.sheet1.json('{}_{}.txt'.format(file, 'sheet1_json'))
        self.sheet2.json('{}_{}.txt'.format(file, 'sheet2_json'))
        self.sheet3.json('{}_{}.txt'.format(file, 'sheet3_json'))
