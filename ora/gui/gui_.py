
from PyQt5 import uic, QtCore

from widget import *
from style import *
from functions import *

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

    def _set_hover_icon(self, widget, normal_file, hover_file):
        set_full_icon(widget, normal_file, 'widgets')
        widget.setAttribute(Qt.WA_Hover, True)
        widget.setStyleSheet('background-image: url(%s)' % (SRC_PATH + '/widgets/' + hover_file))


class BeautiUi(windowui, UiFunc, WindowDragMixin, ControlButtonMixin):
    def __init__(self):
        super(BeautiUi, self).__init__()
        self.setupUi(self)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.set_control_button(self.min_button, self.max_button, self.close_button)

        self.tab_listwidget.setFrameShape(QtWidgets.QFrame.NoFrame)
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

        for label in get_qclass_child_widgets(self.stackedWidgetPage1, QtWidgets.QLineEdit):
            pass





        #for wi, ics in hover_icons.items():
        #    self._set_hover_icon(getattr(self, wi), *ics)


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
        citem.setObjectName('DyItem')
        item = QtWidgets.QListWidgetItem(listwidget)
        item.setSizeHint(citem.sizeHint())
        listwidget.addItem(item)
        listwidget.setItemWidget(item, citem)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    with open('style.qss') as qss:
        app.setStyleSheet(qss.read())
    w = MainUi()
    w.show()
    sys.exit(app.exec_())