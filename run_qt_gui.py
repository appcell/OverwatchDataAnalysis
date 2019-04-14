import sys
from PyQt5 import QtWidgets
from ora.gui.gui import MainUi

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    with open('./ora/gui/style.qss') as qss:
        app.setStyleSheet(qss.read())
    w = MainUi()
    w.show()
    sys.exit(app.exec_())