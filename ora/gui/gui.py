
from os.path import join

from PyQt5.Qt import QIcon

from widget import *


SRC_PATH = 'D:/GitHub/OverwatchDataAnalysis/ui_design/images'


class UiFunc(object):
    @staticmethod
    def _add_list_item(listwidget, item_class, *args):
        citem = item_class(listwidget, *args)
        item = QtWidgets.QListWidgetItem(listwidget)
        item.setSizeHint(citem.sizeHint())
        listwidget.addItem(item)
        listwidget.setItemWidget(item, citem)

    @staticmethod
    def _add_widget_item(parent, layout, widget_class, geometry, *args, **kwargs):
        widget = widget_class(parent, *args, **kwargs)
        widget.setGeometry(*geometry)
        if not layout:
            layout = parent.layout
        layout.addWidget(widget)
        return widget

    @staticmethod
    def _get_icon(file_name):
        return QIcon(join(SRC_PATH, 'icons', file_name))

    @staticmethod
    def _set_background_img(widget, file_name):
        widget.setStyleSheet("background-image: url(%s)" % (SRC_PATH + '/bgs/' + file_name))


class UiWidget(UiFunc):
    def line_edit_with_label(self, text=''):
        label = TextLabel(self)
        line_edit = LineEdit(self)
        self._set_background_img(line_edit, '')
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(label)
        layout.addWidget(line_edit)
        self.layout.addChildLayout(layout)

    def label_with_radio_buttons(self):
        label = TextLabel()
        button0 = RadioButton()
        button1 = RadioButton()
        button_group = QtWidgets.QButtonGroup()
        button_group.addButton(button0)
        button_group.addButton(button1)
        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(label)
        layout.addWidget(button0)
        layout.addWidget(button1)

    def label_with_check_button(self):
        label = TextLabel()
        button = CheckButton()


class MainUiBaseWidget(MainWindow, UiWidget, WindowDragMixin, ControlButtonMixin):
    def __init__(self):
        super(MainUiBaseWidget, self).__init__()
        # MainWindow.__init__(self)
        # UiFunc.__init__(self)
        self._init_widget()
        self._init_connect()

    def _init_widget(self):
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)
        self._init_base_widget()

    def _init_connect(self):
        self.tab_listwidget.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(self.tab_listwidget.currentRow()))
        self.set_control_button(self.min_button, self.max_button, self.close_button, '[]', '{}')
        # ControlButtonMixin.__init__(self.min_button, self.max_button, self.exit_button)

    def _init_base_widget(self):
        self.tab_layout = QtWidgets.QVBoxLayout()
        # self.tab_layout.setGeometry((0, 0, 120, 620))
        self._add_widget_item(self, self.tab_layout, PicLabel, geometry=(0, 0, 120, 67))
        self.tab_listwidget = self._add_widget_item(self, self.tab_layout, ListWidget, geometry=(0, 67, 120, 620))
        self._set_background_img(self.tab_listwidget, 'left_bg.png')
        self._add_list_item(self.tab_listwidget, TabItem, "ANALYSIS", 'replay.png')
        self._add_list_item(self.tab_listwidget, TabItem, "VIDEO PALY", 'replay.png')
        self._add_list_item(self.tab_listwidget, TabItem, "SETTINGS", 'replay.png')

        self.top_layout = QtWidgets.QHBoxLayout()
        self.top_group = QtWidgets.QGroupBox(self)
        self.top_group.setLayout(self.top_layout)
        self._set_background_img(self.top_group, 'top_bg.png')
        self.back_button = self._add_widget_item(self.top_group, self.top_layout, ClickButton, geometry=(140, 0, 47, 67), icon_path=self._get_icon('design_03'))
        self.help_button = self._add_widget_item(self, self.top_layout, ClickButton, geometry=(1000, 0, 47, 67), icon_path=self._get_icon('design_05'))
        self.min_button = self._add_widget_item(self, self.top_layout, ClickButton, geometry=(1050, 0, 47, 67), icon_path=self._get_icon('design_07'))
        self.max_button = self._add_widget_item(self, self.top_layout, ClickButton, geometry=(1100, 0, 47, 67), icon_path=self._get_icon('design_08'))
        self.close_button = self._add_widget_item(self, self.top_layout, ClickButton, geometry=(1150, 0, 47, 67), icon_path=self._get_icon('design_09'))

        self.stacked_widget = self._add_widget_item(self, None, StackedWidget, geometry=(120, 67, 1080, 733))
        self._init_analysis_tab()
        self._init_play_tab()
        self._init_setting_tab()

        self.stacked_widget.addWidget(self.analysis_widget)
        self.stacked_widget.addWidget(self.play_widget)
        self.stacked_widget.addWidget(self.setting_widget)
        #self.stacked_widget.setCurrentIndex(1)

    def _init_analysis_tab(self):
        self.analysis_widget = QtWidgets.QWidget(self.stacked_widget)
        self.analysis_layout = QtWidgets.QGridLayout()
        self.analysis_layout.addWidget(self.analysis_widget)
        self.video_listwidget = self._add_widget_item(self.analysis_widget, self.analysis_layout, ListWidget, geometry=(0, 0, 620, 640))
        # self._set_background_img(self.video_listwidget, )

        self._add_list_item(self.video_listwidget, VideoItem, '/path/1.mp4', 'WAITING', 'Shanghai Dragons', 'Dallas Fuel', 'replay.png')
        self._add_list_item(self.video_listwidget, VideoItem, '/path/1.mp4', 'RUNNING', 'Shanghai Dragons', 'Dallas Fuel', 'replay.png')

        self.line_edit_with_label()

    def _init_play_tab(self):
        self.play_widget = QtWidgets.QWidget(self.stacked_widget)
        self.play_layout = QtWidgets.QGridLayout()
        self.play_layout.addWidget(self.play_widget)
        self._add_widget_item(self.play_widget, self.play_layout, TextLabel, geometry=(0, 0, 100, 100), text='PALY')

    def _init_setting_tab(self):
        self.setting_widget = QtWidgets.QWidget(self.stacked_widget)
        self.setting_layout = QtWidgets.QGridLayout()
        self.setting_layout.addWidget(self.setting_widget)
        self._add_widget_item(self.setting_widget, self.setting_layout, TextLabel, geometry=(0, 0, 100, 100), text='SETTTING')


class MainUi(MainUiBaseWidget):
    def __init__(self):
        super(MainUi, self).__init__()

    def _init_default(self):
        self.tab_listwidget.setCurrentRow(0)
        self.stacked_widget.setCurrentIndex(2)







if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainUi()
    w.show()
    sys.exit(app.exec_())