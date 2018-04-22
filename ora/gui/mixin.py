from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


class MousePressChangeBackgroundMixin(object):
    def __init__(self):
        super(MousePressChangeBackgroundMixin, self).__init__()
        self.setMouseTracking(True)

    def mouseMoveEvent(self, QMouseEvent):
        pass

    def mousePressEvent(self, QMouseEvent):
        self.setStyleSheet("background-color: %s" % "#11283E")
        for c in self.children():
            if isinstance(c, QtWidgets.QLabel):
                c.setStyleSheet("background-color: %s" % "#11283E")

    def mouseReleaseEvent(self, QMouseEvent):
        self.setStyleSheet("background-color: %s" % "#14304A")
        for c in self.children():
            if isinstance(c, QtWidgets.QLabel):
                c.setStyleSheet("background-color: %s" % "#14304A")



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
