# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 21:21:48 2018

@author: lovef
"""

import sys
from PyQt5 import QtCore, QtGui, QtPrintSupport , QtWidgets, uic
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, 
    QAction, QFileDialog, QApplication)

qtCreatorFile = "ora.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp( QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.addingVideo.clicked.connect(self.oraOpenFile)

        self.browseFile.clicked.connect(self.oraSaveFile)
        
        self.analyze.clicked.connect(self.ora)

        
#    def CalculateTax(self):
#        price = int(self.price_box.toPlainText())
#        tax = (self.tax_rate.value())
#        total_price = price  + ((tax / 100) * price)
#        total_price_string = "The total price with tax is: " + str(total_price)
#        self.results_window.setText(total_price_string)

    def oraOpenFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        
    def oraSaveFile(self):
        saveName = QFileDialog.getSaveFileName(self, 'Save file', '/home')
        self.savePosition.setText(str(saveName))
        
        
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())