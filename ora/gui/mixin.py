from functools import partial

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from functions import set_background_color


class MousePressChangeBackgroundMixin(QtWidgets.QWidget):
    def __init__(self, normal_color="#143048", selected_color="#11293f"):
        super(MousePressChangeBackgroundMixin, self).__init__()
        self.setMouseTracking(True)
        self.normal_color = normal_color
        self.selected_color = selected_color

    @property
    def _color(self):
        return '#' + ''.join([str(hex(c)[2:]) for c in self.palette().color(self.backgroundRole()).toRgb().getRgb()[:3]])

    def is_selected(self):
        return True if self._color == self.selected_color else False

    def _set_color(self, color):
        self.setStyleSheet("background-color: %s" % color)
        for c in self.children():
            if isinstance(c, QtWidgets.QLabel):
                c.setStyleSheet("background-color: %s" % color)

    def enterEvent(self, QMouseEvent):
        pass

    def mouseMoveEvent(self, QMouseEvent):
        pass

    def mousePressEvent(self, QMouseEvent):
        color = self.normal_color if self.is_selected() else self.selected_color
        self._set_color(color)

    def mouseReleaseEvent(self, QMouseEvent):
        color = self._color
        self._set_color(color)


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
    def __init__(self):
        super(ControlButtonMixin, self).__init__()

    def set_control_button(self, min_button, max_button, exit_button, max_icon='', resize_icon='', bg_color='#000000'):
        # self.max_button = max_button
        # self.max_icon = max_icon
        self.resize_icon = resize_icon

        # map(partial(set_background_color, color=bg_color), [min_button, max_button, exit_button])
        min_button.clicked.connect(self.showMinimized)
        # max_button.clicked.connect(self._max_button_clicked)
        exit_button.clicked.connect(self.close)

    def _max_button_clicked(self):
        if self.isMaximized():
            self.showNormal()
            self.max_button.setText(self.resize_icon)
        else:
            self.showMaximized()
            self.max_button.setText(self.resize_icon)
