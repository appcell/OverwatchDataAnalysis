
from PyQt5 import uic, QtCore, QtWidgets, QtGui
from widget import *
from style import *
from functions import *
from gui_api import *

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
windowui, QtBaseClass = uic.loadUiType('main.ui')

SRC_PATH = './images'


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
    def _add_custome_item(listwidget, item_class, *args):
        citem = item_class(listwidget, *args)
        # citem.setObjectName('DyItem')
        item = QtWidgets.QListWidgetItem(listwidget)
        item.setSizeHint(citem.sizeHint())
        listwidget.addItem(item)
        listwidget.setItemWidget(item, citem)

    @staticmethod
    def _set_hover_icon(widget, normal_file, hover_file):
        set_full_icon(widget, normal_file, 'widgets')
        widget.setAttribute(Qt.WA_Hover, True)
        widget.setStyleSheet('background-image: url(%s)' % (SRC_PATH + '/widgets/' + hover_file))


class BeautiUi(windowui, WindowDragMixin, ControlButtonMixin):
    def __init__(self):
        super(BeautiUi, self).__init__()
        self.setupUi(self)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.set_control_button(self.min_button, self.max_button, self.close_button)

        self.tab_listwidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        # self.tab_listwidget.setSpacing(50)
        self.video_listwidget.setFrameShape(QtWidgets.QFrame.NoFrame)

        self._set_style()

        set_full_icon(self.publish_box, 'switch_on.png')

    def _set_style(self):
        for wi, bg in background_imgs.items():
            set_background_img(getattr(self, wi), bg)

        for wi, ic in button_icons.items():
            set_full_icon(getattr(self, wi), ic)

        for wi, cl in background_colors.items():
            set_background_color(getattr(self, wi), cl)

        for wi, tx in plain_text.items():
            set_plain_text(getattr(self, wi), tx)

        for label in get_qclass_child_widgets(self.stackedWidgetPage1, QtWidgets.QLineEdit):
            pass


class MainUi(QtWidgets.QMainWindow, BeautiUi, UiFunc):
    def __init__(self):
        super(MainUi, self).__init__()
        self._set_tab_listwidget_items([['1_normal.png', '1_selected.png'], ['2_normal.png', '2_selected.png'], ['3_normal.png', '3_selected.png']])
        self.tab_listwidget.setIconSize(QSize(100, 100))
        self._init_widget()
        self._init_connect()
        self._init_property()
        self._init_default()

    def _init_widget(self):
        self._add_custome_item(self.video_listwidget, VideoItem, '', '/path/1.mp4', 'WAITING', 'Shanghai Dragons', 'Dallas Fuel', 'replay.png')
        self._add_custome_item(self.video_listwidget, VideoItem, '', '/path/1.mp4', 'RUNNING', 'Shanghai Dragons', 'Dallas Fuel', 'replay.png')

    def _init_connect(self):
        self.tab_listwidget.itemClicked.connect(self._tab_listwidget_item_clicked)
        self.video_listwidget.customContextMenuRequested.connect(self._video_list_context_menu)

        self.team_left_lineedit.editingFinished.connect(lambda: self._team_name_edit_finished('left'))
        self.team_right_lineedit.editingFinished.connect(lambda: self._team_name_edit_finished('right'))

        self.save_button.clicked.connect(self.save_button_clicked)
        self.analyze_button.clicked.connect(self.analyze_button_clicked)
        self.analyze_button.clicked.connect(self.select_video)  # TODO: need connect to add video button

    def _init_property(self):

        # set player's text to property like self.player_left0_text
        for widget in get_qclass_child_widgets(self.team_setting_group, QtWidgets.QLineEdit):
            name = widget.objectName
            if name.startswith('player_'):
                setattr(self, name.rstrip('lineedit') + 'text', widget.text())

    def _init_default(self):
        self.tab_listwidget.setCurrentRow(0)
        self.main_stackedwidget.setCurrentIndex(0)

    def _set_tab_listwidget_items(self, pics):
        for pic in pics:
            item = QtWidgets.QListWidgetItem(QtGui.QIcon(SRC_PATH + '/tab_icons/' + pic[0]), '')
            item.normal_icon = QtGui.QIcon(SRC_PATH + '/tab_icons/' + pic[0])
            item.selected_icon = QtGui.QIcon(SRC_PATH + '/tab_icons/' + pic[1])
            self.tab_listwidget.addItem(item)

    def _set_tab_listwidget_normal_icon(self):
        for i in range(0, self.tab_listwidget.count()):
            item = self.tab_listwidget.item(i)
            item.setIcon(item.normal_icon)

    def _tab_listwidget_item_clicked(self, item):
        self.main_stackedwidget.setCurrentIndex(self.tab_listwidget.currentRow())
        self._set_tab_listwidget_normal_icon()
        item.setIcon(item.selected_icon)

    def _video_list_context_menu(self):
        menu = QtWidgets.QMenu()
        menu.addAction('删除', lambda: remove_listwidget_item(self.video_listwidget))
        menu.exec_(QtGui.QCursor.pos())

    def _team_name_edit_finished(self, team='left'):
        current_video_item = self.current_video_item
        setattr(current_video_item, 'set_team_%s_text' % team, getattr(self, 'input_team_%s_text' % team))

    def select_video(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, u'Select Video', filter="* (*.*)")
        self._set_new_video(filename)

    def _set_new_video(self, path):
        self._add_custome_item(self.video_listwidget, VideoItem, path, path, 'WAITING', 'Shanghai Dragons',
                               'Dallas Fuel', 'replay.png')

    def save_button_clicked(self):
        dirname = QtWidgets.QFileDialog.getExistingDirectory(self, u'Select Folder')
        self.path_lineedit.setText(dirname)

    def analyze_button_clicked(self):
        return analyze_button_clicked(self.is_owl, )

    @property
    def input_team_left_text(self):
        return self.team_left_lineedit.text()

    @property
    def input_team_right_text(self):
        return self.team_right_lineedit.text()

    @property
    def current_video_item(self):
        item = self.video_listwidget.currentItem()
        return self.video_listwidget.itemWidget(item)

    @property
    def is_published(self):
        return self.publish_box.isChecked()

    @property
    def is_owl(self):
        return True if self.type_owl_radiobutton.isChecked() else False

    @property
    def start_time(self):
        return self.start_time_lineedit.text()

    @property
    def end_time(self):
        return self.end_time_lineedit.text()

    @property
    def video_path_text(self):
        pass

    @property
    def output_path_text(self):
        pass

    @property
    def game_info(self):
        info = {
            "name_team_left": self.input_team_left_text,
            "name_team_right": self.input_team_right_text,
            "name_players_team_left": [],
            "name_players_team_right": [],
            "video_path": "/",
            "output_path": "/",
            "start_time": self.start_time,
            "end_time": self.end_time,
            "fps": 0,
            "game_type": 0,
            "game_version": 1
        }


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    with open('style.qss') as qss:
        app.setStyleSheet(qss.read())
    w = MainUi()
    w.show()
    sys.exit(app.exec_())