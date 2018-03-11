import sys

from PyQt5 import QtGui, QtWidgets


class CustomeItem(QtWidgets.QWidget):
    def __init__(self, parent=None, up_str='', down_str='', icon_path=''):
        super(CustomeItem, self).__init__(parent)
        self.textQVBoxLayout = QtWidgets.QVBoxLayout()
        self.textUpQLabel = QtWidgets.QLabel()
        self.textDownQLabel = QtWidgets.QLabel()
        self.textQVBoxLayout.addWidget(self.textUpQLabel)
        self.textQVBoxLayout.addWidget(self.textDownQLabel)
        self.allQHBoxLayout = QtWidgets.QHBoxLayout()
        self.iconQLabel = QtWidgets.QLabel()
        self.allQHBoxLayout.addWidget(self.iconQLabel, 0)
        self.allQHBoxLayout.addLayout(self.textQVBoxLayout, 1)
        self.setLayout(self.allQHBoxLayout)
        # setStyleSheet
        self.textUpQLabel.setStyleSheet('''
            color: rgb(0, 0, 255);
        ''')
        self.textDownQLabel.setStyleSheet('''
            color: rgb(255, 0, 0);
        ''')

        self.setTextUp(up_str)
        self.setTextDown(down_str)
        if icon_path:
            self.setIcon(icon_path)

    def setTextUp (self, text):
        self.textUpQLabel.setText(text)

    def setTextDown (self, text):
        self.textDownQLabel.setText(text)

    def setIcon (self, img_path):
        self.iconQLabel.setPixmap(QtGui.QPixmap(img_path))


class _MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(_MyWindow, self).__init__()
        self.listwidget = QtWidgets.QListWidget(self)
        citem = CustomeItem(self, '123', '456', 'replay.png')
        item = QtWidgets.QListWidgetItem(self)
        item.setSizeHint(citem.sizeHint())
        self.listwidget.addItem(item)
        self.listwidget.setItemWidget(item, citem)
        self.setCentralWidget(self.listwidget)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = _MyWindow()
    w.show()
    sys.exit(app.exec_())




