# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'data/design/form_history.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.main_table = QtWidgets.QTableWidget(self.centralwidget)
        self.main_table.setGeometry(QtCore.QRect(30, 100, 740, 450))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.main_table.setFont(font)
        self.main_table.setRowCount(0)
        self.main_table.setColumnCount(3)
        self.main_table.setObjectName("main_table")
        self.exit_button = QtWidgets.QPushButton(self.centralwidget)
        self.exit_button.setGeometry(QtCore.QRect(30, 10, 160, 40))
        font = QtGui.QFont()
        font.setPointSize(19)
        self.exit_button.setFont(font)
        self.exit_button.setObjectName("exit_button")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(260, 20, 350, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "история"))
        self.exit_button.setText(_translate("MainWindow", "Выйти"))
        self.label.setText(_translate("MainWindow", "История ваших действий"))
