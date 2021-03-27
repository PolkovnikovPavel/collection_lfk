# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'data/design/report_5.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(956, 796)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(390, 10, 501, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 50, 911, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(530, 80, 460, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.choice_date_2 = QtWidgets.QCalendarWidget(self.centralwidget)
        self.choice_date_2.setGeometry(QtCore.QRect(490, 120, 449, 310))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.choice_date_2.setFont(font)
        self.choice_date_2.setObjectName("choice_date_2")
        self.choice_date_1 = QtWidgets.QCalendarWidget(self.centralwidget)
        self.choice_date_1.setGeometry(QtCore.QRect(20, 120, 450, 310))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.choice_date_1.setFont(font)
        self.choice_date_1.setObjectName("choice_date_1")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(20, 90, 460, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.button = QtWidgets.QPushButton(self.centralwidget)
        self.button.setGeometry(QtCore.QRect(730, 710, 200, 40))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.button.setFont(font)
        self.button.setObjectName("button")
        self.scroll_places = QtWidgets.QScrollArea(self.centralwidget)
        self.scroll_places.setGeometry(QtCore.QRect(30, 480, 310, 220))
        self.scroll_places.setWidgetResizable(True)
        self.scroll_places.setObjectName("scroll_places")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 308, 218))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scroll_places.setWidget(self.scrollAreaWidgetContents)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(30, 450, 391, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.scroll_doctor = QtWidgets.QScrollArea(self.centralwidget)
        self.scroll_doctor.setGeometry(QtCore.QRect(520, 480, 410, 220))
        self.scroll_doctor.setWidgetResizable(True)
        self.scroll_doctor.setObjectName("scroll_doctor")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 408, 218))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.scroll_doctor.setWidget(self.scrollAreaWidgetContents_2)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(520, 450, 470, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.error_text = QtWidgets.QLabel(self.centralwidget)
        self.error_text.setGeometry(QtCore.QRect(30, 710, 700, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.error_text.setFont(font)
        self.error_text.setStyleSheet("color: #FF0000")
        self.error_text.setText("")
        self.error_text.setObjectName("error_text")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 956, 18))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Сборный отчёт"))
        self.label.setText(_translate("MainWindow", "Сборный отчёт"))
        self.label_2.setText(_translate("MainWindow", "Выберите промежуток дней, в котором были проведены операции у пациентов"))
        self.label_3.setText(_translate("MainWindow", "До какого дня (включительно)"))
        self.label_4.setText(_translate("MainWindow", "С какого дня (включительно)"))
        self.button.setText(_translate("MainWindow", "Создать отчёт"))
        self.label_5.setText(_translate("MainWindow", "Выберите способы реабилитации"))
        self.label_6.setText(_translate("MainWindow", "Выберите врачей, которых отобразить в отчёте"))
