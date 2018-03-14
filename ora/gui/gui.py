

from widget import *


class MainUiBaseWidget(MainWindow):
    def __init__(self):
        super(MainUiBaseWidget, self).__init__()
        layout = QtWidgets.QGridLayout()
        self.videoListWidget = ListWidget(self)
        self.videoListWidget.setGeometry(120, 67, 620, 640)
        self.tabListWidget = QtWidgets.QListWidget(self)
        self.tabListWidget.setGeometry(0, 0, 0, 0)
        layout.addWidget(self.videoListWidget)
        self.setLayout(layout)


class MainUi(MainUiBaseWidget):
    def __init__(self):
        super(MainUi, self).__init__()
        self._add_custome_item(self.videoListWidget, VideoItem, '/path/1.mp4', 'WAITING', 'Shanghai Dragons', 'Dallas Fuel', 'replay.png')
        self._add_custome_item(self.videoListWidget, VideoItem, '/path/1.mp4', 'RUNNING', 'Shanghai Dragons', 'Dallas Fuel',
                               'replay.png')

        self._add_custome_item(self.tabListWidget, TabItem, "ANALYSIS", 'replay.png')
        self._add_custome_item(self.tabListWidget, TabItem, "VIDEO PALY", 'replay.png')
        self._add_custome_item(self.tabListWidget, TabItem, "SETTINGS", 'replay.png')


        # self._init_connect()

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