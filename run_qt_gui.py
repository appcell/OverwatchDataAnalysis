import sys
from PyQt5 import QtWidgets
from ora.gui.gui import MainUi

sys._excepthook = sys.excepthook
def exception_hook(exctype, value, traceback):
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)
sys.excepthook = exception_hook

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    with open('./ora/gui/style.qss') as qss:
        app.setStyleSheet(qss.read())
    w = MainUi()
    w.show()
    sys.exit(app.exec_())