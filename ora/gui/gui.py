

from widget import *


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


class MainUiBaseWidget(MainWindow, UiFunc, WindowDragMixin, ControlButtonMixin):
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
        self.set_button(self.min_button, self.max_button, self.close_button, '[]', '{}')
        # ControlButtonMixin.__init__(self.min_button, self.max_button, self.exit_button)

    def _init_base_widget(self):
        self.tab_layout = QtWidgets.QVBoxLayout()
        # self.tab_layout.setGeometry((0, 0, 120, 620))
        self._add_widget_item(self, self.tab_layout, PicLabel, geometry=(0, 0, 120, 67))
        self.tab_listwidget = self._add_widget_item(self, self.tab_layout, ListWidget, geometry=(0, 67, 120, 620))
        self._add_list_item(self.tab_listwidget, TabItem, "ANALYSIS", 'replay.png')
        self._add_list_item(self.tab_listwidget, TabItem, "VIDEO PALY", 'replay.png')
        self._add_list_item(self.tab_listwidget, TabItem, "SETTINGS", 'replay.png')

        self.top_layout = QtWidgets.QHBoxLayout()
        self.back_button = self._add_widget_item(self, self.top_layout, ClickButton, geometry=(140, 0, 47, 67), text='<')
        self.help_button = self._add_widget_item(self, self.top_layout, ClickButton, geometry=(1000, 0, 47, 67), text='?')
        self.min_button = self._add_widget_item(self, self.top_layout, ClickButton, geometry=(1050, 0, 47, 67), text='-')
        self.max_button = self._add_widget_item(self, self.top_layout, ClickButton, geometry=(1100, 0, 47, 67), text='[]')
        self.close_button = self._add_widget_item(self, self.top_layout, ClickButton, geometry=(1150, 0, 47, 67), text='X')

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

        self._add_list_item(self.video_listwidget, VideoItem, '/path/1.mp4', 'WAITING', 'Shanghai Dragons', 'Dallas Fuel', 'replay.png')
        self._add_list_item(self.video_listwidget, VideoItem, '/path/1.mp4', 'RUNNING', 'Shanghai Dragons', 'Dallas Fuel', 'replay.png')

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