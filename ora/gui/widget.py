import sys

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt


class ListWidget(QtWidgets.QListWidget):
    def __init__(self, parent=None):
        super(ListWidget, self).__init__(parent)
        self.setFrameShape(QtWidgets.QFrame.NoFrame)


class VideoItem(QtWidgets.QWidget):
    def __init__(self, parent=None, up_left_str='', up_right_str='', down_left_str='', down_right_str='', icon_path=''):
        super(VideoItem, self).__init__(parent)

        self.textUpLayout = QtWidgets.QHBoxLayout()
        self.textUpLeftLabel = QtWidgets.QLabel()
        self.textUpRightLabel = QtWidgets.QLabel()
        self.textUpLayout.addWidget(self.textUpLeftLabel)
        self.textUpLayout.addWidget(self.textUpRightLabel)

        self.textDownLayout = QtWidgets.QHBoxLayout()
        self.textDownLabelTeam1 = QtWidgets.QLabel()
        self.textDownLeftLabel = QtWidgets.QLabel()
        self.textDownLabelTeam2 = QtWidgets.QLabel()
        self.textDownRightLabel = QtWidgets.QLabel()
        self.textDownLayout.addWidget(self.textDownLabelTeam1)
        self.textDownLayout.addWidget(self.textDownLeftLabel)
        self.textDownLayout.addWidget(self.textDownLabelTeam2)
        self.textDownLayout.addWidget(self.textDownRightLabel)

        self.allTextLayout = QtWidgets.QVBoxLayout()
        self.allTextLayout.addLayout(self.textUpLayout)
        self.allTextLayout.addLayout(self.textDownLayout)

        self.allQHBoxLayout = QtWidgets.QHBoxLayout()
        self.iconQLabel = QtWidgets.QLabel()
        self.allQHBoxLayout.addWidget(self.iconQLabel, 0)
        self.allQHBoxLayout.addLayout(self.allTextLayout, 1)
        self.setLayout(self.allQHBoxLayout)

        self.textUpLeftLabel.setStyleSheet('''
            color: rgb(0, 0, 255);
        ''')
        self.textUpRightLabel.setStyleSheet('''
            color: rgb(255, 0, 0);
        ''')

        self.setTextDown(down_left_str)
        self.setLabelText(self.textUpLeftLabel, up_left_str)
        self.setLabelText(self.textUpRightLabel, up_right_str)
        self.setLabelText(self.textDownLabelTeam1, "TEAM 1")
        self.setLabelText(self.textDownLeftLabel, down_left_str)
        self.setLabelText(self.textDownLabelTeam2, "TEAM 2")
        self.setLabelText(self.textDownRightLabel, down_right_str)

        if icon_path:
            self.setIcon(icon_path)

    @staticmethod
    def setLabelText(label, text):
        label.setText(text)

    def setTextUp (self, text):
        self.textUpLeftLabel.setText(text)

    def setTextDown (self, text):
        self.textUpRightLabel.setText(text)

    def setIcon (self, img_path):
        self.iconQLabel.setPixmap(QtGui.QPixmap(img_path))


class TabItem(QtWidgets.QWidget):
    def __init__(self, parent=None, text='', img_path=''):
        super(TabItem, self).__init__(parent)
        self.textLabel = QtWidgets.QLabel()
        self.iconLabel = QtWidgets.QLabel()
        self.textLabel.setText(text)
        self.iconLabel.setPixmap(QtGui.QPixmap(img_path))

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.iconLabel)
        self.layout.addWidget(self.textLabel)
        self.setLayout(self.layout)


class PicLabel(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super(PicLabel, self).__init__(parent)
        self.setStyleSheet("{background-color: rgb(14, 31, 51);}")
        self.setGeometry(0, 0, 120, 67)


class TextLabel(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super(TextLabel, self).__init__(parent)
        self.setStyleSheet("{background-color: rgb(14, 31, 51);}")
        self.setGeometry(0, 0, 120, 67)
        self.setText("123")


class LineEdit(QtWidgets.QLineEdit):
    pass


class ClickButton(QtWidgets.QPushButton):
    def __init__(self):
        super(ClickButton, self).__init__()
        self.setFlat(True)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(50, 50, 1200, 800)


class _MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(_MyWindow, self).__init__()
        self.listwidget = QtWidgets.QListWidget(self)
        citem = VideoItem(self, '/path/1.mp4', 'WAITING', 'Shanghai Dragons', 'Dallas Fuel', 'replay.png')
        item = QtWidgets.QListWidgetItem(self.listwidget)
        item.setSizeHint(citem.sizeHint())
        self.listwidget.addItem(item)
        self.listwidget.setItemWidget(item, citem)
        self.setCentralWidget(self.listwidget)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())




