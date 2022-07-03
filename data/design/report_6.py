# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'data/design/report_6.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(628, 714)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(170, 10, 451, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 110, 140, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(130, 80, 201, 111))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.radio_month = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.radio_month.setFont(font)
        self.radio_month.setObjectName("radio_month")
        self.verticalLayout.addWidget(self.radio_month)
        self.radio_quarter = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.radio_quarter.setFont(font)
        self.radio_quarter.setChecked(True)
        self.radio_quarter.setObjectName("radio_quarter")
        self.verticalLayout.addWidget(self.radio_quarter)
        self.radio_year = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.radio_year.setFont(font)
        self.radio_year.setObjectName("radio_year")
        self.verticalLayout.addWidget(self.radio_year)
        self.selected_period = QtWidgets.QComboBox(self.centralwidget)
        self.selected_period.setGeometry(QtCore.QRect(350, 120, 261, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.selected_period.setFont(font)
        self.selected_period.setObjectName("selected_period")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(10, 210, 610, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(10, 50, 610, 20))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 230, 551, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 270, 601, 110))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.layout_categories = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.layout_categories.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.layout_categories.setContentsMargins(0, 0, 0, 0)
        self.layout_categories.setSpacing(1)
        self.layout_categories.setObjectName("layout_categories")
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(10, 400, 610, 20))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 420, 611, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(10, 460, 601, 104))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.radio_all = QtWidgets.QRadioButton(self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.radio_all.setFont(font)
        self.radio_all.setObjectName("radio_all")
        self.verticalLayout_3.addWidget(self.radio_all)
        self.radio_discharged = QtWidgets.QRadioButton(self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.radio_discharged.setFont(font)
        self.radio_discharged.setChecked(True)
        self.radio_discharged.setObjectName("radio_discharged")
        self.verticalLayout_3.addWidget(self.radio_discharged)
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setGeometry(QtCore.QRect(10, 580, 610, 20))
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.button = QtWidgets.QPushButton(self.centralwidget)
        self.button.setGeometry(QtCore.QRect(210, 620, 210, 40))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.button.setFont(font)
        self.button.setObjectName("button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 628, 22))
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
        self.label.setText(_translate("MainWindow", "Отчёт по категориям"))
        self.label_2.setText(_translate("MainWindow", "период:"))
        self.radio_month.setText(_translate("MainWindow", "За месяц"))
        self.radio_quarter.setText(_translate("MainWindow", "За квартал"))
        self.radio_year.setText(_translate("MainWindow", "За год"))
        self.label_3.setText(_translate("MainWindow", "Отображаемые категории:"))
        self.label_4.setText(_translate("MainWindow", "Правила выбора пациентов для отчёта:"))
        self.radio_all.setText(_translate("MainWindow", "Выбирать всех пациентов"))
        self.radio_discharged.setText(_translate("MainWindow", "Выбирать только выписанных"))
        self.button.setText(_translate("MainWindow", "Создать отчёт"))
