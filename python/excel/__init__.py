# -*- coding:utf-8 -*-
from openpyxl import Workbook
from openpyxl.styles import (
    Alignment,
    Font,
    PatternFill,
)
from openpyxl.utils import get_column_letter
import excel.sheet1_config as sheet1_config


def create_sheet():
    wb = Workbook()
    wb.active.title = 'sheet1'
    wb.create_sheet('sheet2')
    return wb


class Excel(object):
    def __init__(self):
        self._wb = create_sheet()
        self.sheet1 = Sheet1(self._wb)

    def save(self, filename='text', postfix='xlsx'):
        self.sheet1.save()
        self._wb.save('{}.{}'.format(filename, postfix))


class Sheet1:
    def __init__(self, wb):
        self._wb = wb
        self.config = {}
        self.sheet = self._init_sheet()

    def _init_sheet(self):
        sheet = self._wb['sheet1']
        self._init_config()
        sheet.append(self.config['title_top'])
        sheet.append(self.config['title'])
        return sheet

    def _init_config(self):
        lt = [
            {'cell_width': sheet1_config.CELL_WIDTH_CONFIG},
            {'style': self._style_config()},
            {'title_top': sheet1_config.TITLE_TOP},
            {'merge_cell': sheet1_config.TITLE_TOP_MERGE_CELL},
            {'title': sheet1_config.TITLE},
            # 这是对 title 中标题在哪一格的标记，方便从一个 list 中替换数据。
            {'format': sheet1_config.PRINT_DATA_FORMAT},
            # 将 KillFeed 类的属性转换成输出格式
            # 比如说 character1 ——> subject player
            {'change': sheet1_config.API_CHANGE_CONFIG},
        ]
        for d in lt:
            self.config.update(d)

    @staticmethod
    def _style_config():
        d = {
            'style_font': {
                'name': 'Microsoft YaHei',
                'size': 12,
                'bold': True,
                'vertAlign': 'baseline',
            },
            'style_alignment': {
                'horizontal': 'center',
                'vertical': 'center',
                'wrap_text': True,
            },
            'color': {},
        }
        return d

    def _cell_style(self, cell):
        style = self.config['style']
        cell.font = Font(**style['style_font'])
        cell.alignment = Alignment(**style['style_alignment'])

    def _setting_cells_style(self):
        max_row, max_column = self.sheet.max_row + 1, self.sheet.max_column + 1
        for r in range(1, max_row):
            self.sheet.row_dimensions[r].height = 18
            for c in range(1, max_column):
                letter = get_column_letter(c)
                cell = '{}{}'.format(letter, str(r))

                self._cell_style(self.sheet[cell])
                self.sheet.column_dimensions[letter].width = self.config['cell_width'][letter]

    def _merge_cells(self):
        merge_config = self.config['merge_cell']
        for key in self.config['title_top']:
            if merge_config[key] is not None:
                self.sheet.merge_cells(merge_config[key])

    def save(self):
        self._setting_cells_style()
        self._setting_cell_color()
        self._merge_cells()

    def _format(self, data):
        data['time'] = time_format(data['time'] / 30)
        format_spec = self.config['format']
        result = [''] * len(self.config['title'])
        for k, v in format_spec.items():
            if k in ['object hero', 'subject hero']:
                data[k] = capitalize(data[k])

            if k in data:
                result[v-1] = data[k]
        return result

    def _cell_color_config(self, data):
        if '_$color' in data.keys():
            r = self.sheet.max_row + 1
            color = data.pop('_$color')
            for k, v in color.items():
                s = '{}{}'.format(sheet1_config.DIMENSIONS[k], r)
                self.config['style']['color'][s] = v
        return data

    def _setting_cell_color(self):
        color = self.config['style']['color']
        for k, v in color.items():
            self.sheet[k].fill = PatternFill(
                fill_type='solid',
                fgColor=v,
            )

    def _append(self, **kwargs):
        """
        格式化输出并加入到 sheet中
        :param kwargs: key为单元格的title value为单元格的值 
                    如果 kwargs 中 包含 '_$color' ，则 _$color 的 key 为字段名， value 为颜色
                    value 必须为 aRGB hex
        :return: None
        """
        # 这里假设 OverwatchGame
        kwargs = self._cell_color_config(kwargs)
        result = self._format(kwargs)
        self.sheet.append(result)

    def append(self, game_data):
        """
        解析 GameData, 并添加到 sheet 中
        考虑到表格的模板，东西都会在 killfeed 中。
        因此我这么写
        由于英雄识别还没出，所以我暂时先不处理颜色。
        :param gama_data: 一个 GameData 类，聚合了各种数据
        :return: None
        """
        change = self.config['change']
        for obj in game_data.killfeed_list:
            d = {}
            for r in change.keys():
                d[change[r]] = obj.__dict__[r]
            self._append(**d)


def time_format(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%02d:%02d:%02d" % (h, m, s)


def capitalize(s):
    if s == 'dva':
        return 'D. Va'
    else:
        return None if s is None else s.capitalize()
