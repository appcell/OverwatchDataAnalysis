import sys

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.Qt import QSize


class ListWidget(QtWidgets.QListWidget):
    def __init__(self, parent=None):
        super(ListWidget, self).__init__(parent)
        self.setFrameShape(QtWidgets.QFrame.NoFrame)


class StackedWidget(QtWidgets.QStackedWidget):
    def __init__(self, parent=None):
        super(StackedWidget, self).__init__(parent)


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


class WindowDragMixin(object):
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, QMouseEvent):
        if QMouseEvent.buttons() and Qt.LeftButton:
            self.move(QMouseEvent.globalPos() - self.m_DragPosition)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag = False


class ControlButtonMixin(QtWidgets.QWidget):
    def __init__(self, ):
        super(ControlButtonMixin, self).__init__()

    def set_control_button(self, min_button, max_button, exit_button, max_icon='', resize_icon=''):
        self.max_button = max_button
        self.max_icon = max_icon
        self.resize_icon = resize_icon

        min_button.clicked.connect(self.showMinimized)
        max_button.clicked.connect(self._max_button_clicked)
        exit_button.clicked.connect(self.close)

    def _max_button_clicked(self):
        if self.isMaximized():
            self.showNormal()
            self.max_button.setText(self.resize_icon)
        else:
            self.showMaximized()
            self.max_button.setText(self.resize_icon)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())




