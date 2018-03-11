from PyQt5 import uic

from widget import *

windowui, QtBaseClass = uic.loadUiType('main.ui')


class MainUi(QtWidgets.QMainWindow, windowui):
    def __init__(self):
        super(MainUi, self).__init__()
        self.setupUi(self)
        self._add_custome_item(self.video_listwidget, '111', '222', 'replay.png')
        self._init_connect()

    def _init_connect(self):
        self.label_listwidget.clicked.connect(lambda: self.main_stackedwidget.setCurrentIndex(self.label_listwidget.currentRow()))

    def _init_default(self):
        self.label_listwidget.setCurrentRow(0)
        self.main_stackedwidget.setCurrentIndex(0)

    @staticmethod
    def _add_custome_item(listwidget, up_str, down_str, icon_path):
        citem = CustomeItem(listwidget, up_str, down_str, icon_path)
        item = QtWidgets.QListWidgetItem(listwidget)
        item.setSizeHint(citem.sizeHint())
        listwidget.addItem(item)
        listwidget.setItemWidget(item, citem)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainUi()
    w.show()
    sys.exit(app.exec_())