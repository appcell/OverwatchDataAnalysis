import sys

from PyQt5 import QtGui
from PyQt5.Qt import QSize

from style import text_colors
from mixin import *


class ListWidget(QtWidgets.QListWidget):
    def __init__(self, parent=None):
        super(ListWidget, self).__init__(parent)
        self.setFrameShape(QtWidgets.QFrame.NoFrame)


class StackedWidget(QtWidgets.QStackedWidget):
    def __init__(self, parent=None):
        super(StackedWidget, self).__init__(parent)


class VideoItem(MousePressChangeBackgroundMixin):
    def __init__(self, parent=None, up_left_str='', up_right_str='', down_left_str='', down_right_str='', icon_path=''):
        super(VideoItem, self).__init__()

        self.textUpLayout = QtWidgets.QHBoxLayout()
        self.textUpLeftLabel = FullLabel()
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
        self.iconQLabel.setFixedSize(200, 110)
        self.allQHBoxLayout.addWidget(self.iconQLabel, 0)
        self.allQHBoxLayout.addLayout(self.allTextLayout, 1)
        self.allQHBoxLayout.setSpacing(0)
        self.allQHBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.allQHBoxLayout)


        self.setTextDown(down_left_str)
        self.setLabelText(self.textUpLeftLabel, up_left_str)
        self.setLabelText(self.textUpRightLabel, up_right_str)
        self.setLabelText(self.textDownLabelTeam1, "TEAM 1")
        self.setLabelText(self.textDownLeftLabel, down_left_str)
        self.setLabelText(self.textDownLabelTeam2, "TEAM 2")
        self.setLabelText(self.textDownRightLabel, down_right_str)

        self.setStyleSheet('border: None')

        if icon_path:
            # self.setIcon(icon_path)
            self.iconQLabel.setPixmap(QtGui.QPixmap(icon_path))
            self.iconQLabel.setScaledContents(True)

        for w, c in text_colors.items():
            self.set_text_color(getattr(self, w), c)

    @staticmethod
    def set_text_color(widget, color):
        widget.setStyleSheet("color: %s" % color)

    @staticmethod
    def setLabelText(label, text):
        label.setText(text)

    def setTextUp(self, text):
        self.textUpLeftLabel.setText(text)

    def setTextDown(self, text):
        self.textUpRightLabel.setText(text)

    def setIcon(self, img_path):
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
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)


class PicTabItem(QtWidgets.QWidget):
    def __init__(self, parent=None, normal_img='', selected_img=''):
        super(PicTabItem, self).__init__(parent)
        self.normal_img = normal_img
        self.selected_img = selected_img
        self.label = QtWidgets.QLabel()
        self.label.setPixmap(QtGui.QPixmap(normal_img))
        self.layout = QtWidgets.QGridLayout()
        self.layout.addWidget(self.label)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

    def to_selected_img(self):
        self.label.setPixmap(QtGui.QPixmap(self.selected_img))

    def to_normal_img(self):
        self.label.setPixmap(QtGui.QPixmap(self.normal_img))


class PicLabel(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super(PicLabel, self).__init__(parent)
        self.setStyleSheet("{background-color: rgb(14, 31, 51);}")
        self.setGeometry(0, 0, 120, 67)


class TextLabel(QtWidgets.QLabel):
    def __init__(self, parent=None, text=''):
        super(TextLabel, self).__init__(parent)
        self.setStyleSheet("{background-color: rgb(14, 31, 51);}")
        self.setGeometry(0, 0, 120, 67)
        self.setText(text)


class LineEdit(QtWidgets.QLineEdit):
    def __init__(self, parent=None, text=''):
        super(LineEdit, self).__init__(parent)
        self.setStyleSheet()



class ClickButton(QtWidgets.QPushButton):
    def __init__(self, parent=None, text='', icon_path=None):
        super(ClickButton, self).__init__(parent)
        self.setFlat(True)
        self.setText(text)
        if icon_path:
            self.setIcon(icon_path)
            self.setIconSize(QSize(100, 100))


class RadioButton(QtWidgets.QRadioButton):
    def __init__(self):
        super(RadioButton, self).__init__()


class CheckButton(QtWidgets.QCheckBox):
    def __init__(self):
        super(CheckButton, self).__init__()


class FullLabel(QtWidgets.QLabel):
    def __init__(self):
        super(FullLabel, self).__init__()

    def enterEvent(self, QEvent):
        QEvent.accept()


def click_button():
    button = ClickButton()


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




