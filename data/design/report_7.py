# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'data/design/report_7.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(944, 899)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 911, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(500, 90, 460, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 90, 470, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(380, 10, 501, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.choice_date_2 = QtWidgets.QCalendarWidget(self.centralwidget)
        self.choice_date_2.setGeometry(QtCore.QRect(480, 120, 449, 310))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.choice_date_2.setFont(font)
        self.choice_date_2.setObjectName("choice_date_2")
        self.choice_date_1 = QtWidgets.QCalendarWidget(self.centralwidget)
        self.choice_date_1.setGeometry(QtCore.QRect(10, 120, 450, 310))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.choice_date_1.setFont(font)
        self.choice_date_1.setObjectName("choice_date_1")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(10, 440, 871, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.error_text = QtWidgets.QLabel(self.centralwidget)
        self.error_text.setGeometry(QtCore.QRect(19, 730, 711, 40))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.error_text.setFont(font)
        self.error_text.setStyleSheet("color: #FF0000")
        self.error_text.setText("")
        self.error_text.setObjectName("error_text")
        self.button = QtWidgets.QPushButton(self.centralwidget)
        self.button.setGeometry(QtCore.QRect(710, 820, 200, 40))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.button.setFont(font)
        self.button.setObjectName("button")
        self.scroll_doctor = QtWidgets.QTableWidget(self.centralwidget)
        self.scroll_doctor.setGeometry(QtCore.QRect(10, 480, 920, 330))
        self.scroll_doctor.setObjectName("scroll_doctor")
        self.scroll_doctor.setColumnCount(0)
        self.scroll_doctor.setRowCount(0)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 944, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "отчёт по нагрузке"))
        self.label_2.setText(_translate("MainWindow", "Выберите промежуток дней для выгрузки"))
        self.label_3.setText(_translate("MainWindow", "До какого дня (включительно)"))
        self.label_4.setText(_translate("MainWindow", "С какого дня (включительно)"))
        self.label.setText(_translate("MainWindow", "Отчёт по нагрузке"))
        self.label_6.setText(_translate("MainWindow", "Выберите специалистов, дял формирования отчёта"))
        self.button.setText(_translate("MainWindow", "Создать отчёт"))