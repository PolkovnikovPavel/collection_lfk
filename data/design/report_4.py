# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'data/design/report_4.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(959, 522)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(370, 10, 600, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 60, 520, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.choice_date_1 = QtWidgets.QCalendarWidget(self.centralwidget)
        self.choice_date_1.setGeometry(QtCore.QRect(20, 100, 450, 310))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.choice_date_1.setFont(font)
        self.choice_date_1.setObjectName("choice_date_1")
        self.choice_date_2 = QtWidgets.QCalendarWidget(self.centralwidget)
        self.choice_date_2.setGeometry(QtCore.QRect(490, 100, 449, 310))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.choice_date_2.setFont(font)
        self.choice_date_2.setObjectName("choice_date_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(530, 60, 460, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.button = QtWidgets.QPushButton(self.centralwidget)
        self.button.setGeometry(QtCore.QRect(720, 420, 220, 40))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.button.setFont(font)
        self.button.setObjectName("button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 959, 18))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Карточки на период дней"))
        self.label_2.setText(_translate("MainWindow", "Выберите дату с какого дня начинать (включительно)"))
        self.label_3.setText(_translate("MainWindow", "Выберите дату до какого дня (включительно)"))
        self.button.setText(_translate("MainWindow", "Создать отчёт"))
