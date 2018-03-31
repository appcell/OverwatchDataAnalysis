from os.path import join

from PyQt5 import uic, QtWidgets
from PyQt5.Qt import QIcon

from widget import *

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
    def _get_icon(file_name):
        return QIcon(join(SRC_PATH, 'icons', file_name))

    @staticmethod
    def _set_background_img(widget, file_name):
        widget.setStyleSheet("background-image: url(%s)" % (SRC_PATH + '/bgs/' + file_name))

    @staticmethod
    def dynamic_base_class(instance, cls, cls_name):
        instance.__class__ = type(cls_name, (cls, instance.__class__), {})
        return instance


class BeautiUi(windowui, UiFunc, WindowDragMixin, ControlButtonMixin):
    def __init__(self):
        super(BeautiUi, self).__init__()
        self.setupUi(self)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.set_control_button(self.min_button, self.max_button, self.close_button)

        self.tab_listwidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.video_listwidget.setFrameShape(QtWidgets.QFrame.NoFrame)

        self._set_background_img(self.left_group, 'left_bg.png')
        self._set_background_img(self.top_group, 'top_bg.png')
        self._set_background_img(self.analyze_group, 'analyze_bg.png')
        self._set_background_img(self.video_title_group, 'column_title_bg.png')
        self._set_background_img(self.team_title_group, 'column_title_bg.png')
        self._set_background_img(self.video_setting_group, 'right_bg.png')
        self._set_background_img(self.team_setting_group, 'right_bg.png')
        self._set_background_img(self.left_shadow_label, 'left_bg_shadow.png')



class MainUi(QtWidgets.QMainWindow, BeautiUi):
    def __init__(self):
        super(MainUi, self).__init__()
        self._add_custome_item(self.video_listwidget, VideoItem, '/path/1.mp4', 'WAITING', 'Shanghai Dragons', 'Dallas Fuel', 'replay.png')
        self._add_custome_item(self.video_listwidget, VideoItem, '/path/1.mp4', 'RUNNING', 'Shanghai Dragons', 'Dallas Fuel',
                               'replay.png')

        self._add_custome_item(self.tab_listwidget, PicTabItem, SRC_PATH+'/tab_icons/1_normal.png', SRC_PATH + '/tab_icons/1_selected.png')

        #self._add_custome_item(self.tab_listwidget, TabItem, "ANALYSIS", 'replay.png')
        #self._add_custome_item(self.tab_listwidget, TabItem, "VIDEO PALY", 'replay.png')
        #self._add_custome_item(self.tab_listwidget, TabItem, "SETTINGS", 'replay.png')


        self._init_connect()

    def _init_connect(self):
        self.tab_listwidget.clicked.connect(lambda: self.main_stackedwidget.setCurrentIndex(self.tab_listwidget.currentRow()))

    def _init_default(self):
        self.tab_listwidget.setCurrentRow(0)
        self.main_stackedwidget.setCurrentIndex(2)

    @staticmethod
    def _add_custome_item(listwidget, item_class, *args):
        citem = item_class(listwidget, *args)
        item = QtWidgets.QListWidgetItem(listwidget)
        item.setSizeHint(citem.sizeHint())
        listwidget.addItem(item)
        listwidget.setItemWidget(item, citem)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainUi()
    w.show()
    sys.exit(app.exec_())