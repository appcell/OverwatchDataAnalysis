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

    def append(self, data, sheet_name):
        self.__dict__[sheet_name].append(data)


class Sheet1:
    def __init__(self, wb):
        self._wb = wb
        self.config = {}
        self.sheet = self._init_sheet()
        self.ultimate_status = {i: False for i in range(1, 13)}

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
            # 存放队伍的颜色
            {'color': {'team1': None, 'team2': None, 'status': False}},
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
            if k in ['object hero', 'subject hero'] and k in data:
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
        kwargs = self._cell_color_config(kwargs)
        result = self._format(kwargs)
        self.sheet.append(result)

    def append(self, game_data):
        """
        解析 GameData, 并添加到 sheet 中
        """
        self._killfeed_append(game_data)
        self._ultimate_append(game_data)

    def _killfeed_append(self, game_data):
        """
        将 killfeed 中的属性替换成 change 中的，并添加到表中
        """
        change = self.config['change']
        d = {}
        for obj in game_data.killfeed:
            for r in change.keys():
                d[change[r]] = obj.__dict__[r]
            self._append(**d)

    def _ultimate_append(self, game_data):
        """
        判断此时的大招是否为刚充满，并将刚充满大招的选手名输出
        """
        ultimate = game_data.ultimate.ultimate
        status = self.ultimate_status
        true_list, false_list = ultimate['True'], ultimate['False']
        result = []
        for i in true_list:
            if status[i] is False:
                result.append(i)
                status[i] = True

        for i in false_list:
            # 以后可能要扩展成判断大招是否释放，不过这里先写死
            status[i] = False

        for i in result:
            d = {
                'action': 'ult ready',
                'time': game_data.ultimate.time,
                'subject player': i,
            }
            d.update(utlis_color(game_data, self.config['color'], 'subject player', i))
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


def utlis_color(game_data, config, name, value):
    game = game_data.game
    if config['status'] is False:
        config['team1'], config['team2'] = to_hex(*game.color_team1), to_hex(*game.color_team2)
        config['status'] = True
    color = config['team1'] if value <= 6 else config['team2']
    return {'_$color': {name: color}}


def to_hex(r, g, b):
    if (int(r) + int(g) + int(b))/3 < 90:
        return 'FFFFFF'
    else:
        return (hex(r) + hex(g)[2:] + hex(b)[2:]).upper()[2:]
