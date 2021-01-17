# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'data/design/form_adding_patient.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(886, 613)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.text_full_name = QtWidgets.QLineEdit(self.centralwidget)
        self.text_full_name.setGeometry(QtCore.QRect(550, 10, 320, 30))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.text_full_name.setFont(font)
        self.text_full_name.setObjectName("text_full_name")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(490, 10, 60, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.story_number = QtWidgets.QSpinBox(self.centralwidget)
        self.story_number.setGeometry(QtCore.QRect(660, 140, 210, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.story_number.setFont(font)
        self.story_number.setMinimum(1)
        self.story_number.setMaximum(9999999)
        self.story_number.setObjectName("story_number")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(490, 140, 160, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(490, 250, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.text_category = QtWidgets.QComboBox(self.centralwidget)
        self.text_category.setGeometry(QtCore.QRect(610, 250, 260, 30))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.text_category.setFont(font)
        self.text_category.setEditable(False)
        self.text_category.setObjectName("text_category")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(490, 80, 160, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.choice_date_of_operation = QtWidgets.QCalendarWidget(self.centralwidget)
        self.choice_date_of_operation.setGeometry(QtCore.QRect(20, 120, 410, 270))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.choice_date_of_operation.setFont(font)
        self.choice_date_of_operation.setObjectName("choice_date_of_operation")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(20, 80, 160, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.text_department = QtWidgets.QComboBox(self.centralwidget)
        self.text_department.setGeometry(QtCore.QRect(610, 310, 260, 30))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.text_department.setFont(font)
        self.text_department.setEditable(False)
        self.text_department.setIconSize(QtCore.QSize(16, 16))
        self.text_department.setObjectName("text_department")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(490, 310, 110, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(30, 430, 90, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.text_diagnos = QtWidgets.QComboBox(self.centralwidget)
        self.text_diagnos.setGeometry(QtCore.QRect(130, 430, 740, 30))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.text_diagnos.setFont(font)
        self.text_diagnos.setEditable(True)
        self.text_diagnos.setObjectName("text_diagnos")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(30, 470, 300, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.text_memo = QtWidgets.QTextEdit(self.centralwidget)
        self.text_memo.setGeometry(QtCore.QRect(340, 470, 530, 100))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.text_memo.setFont(font)
        self.text_memo.setObjectName("text_memo")
        self.save_button = QtWidgets.QPushButton(self.centralwidget)
        self.save_button.setGeometry(QtCore.QRect(30, 520, 290, 50))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.save_button.setFont(font)
        self.save_button.setObjectName("save_button")
        self.exit_button = QtWidgets.QPushButton(self.centralwidget)
        self.exit_button.setGeometry(QtCore.QRect(20, 10, 160, 40))
        font = QtGui.QFont()
        font.setPointSize(19)
        self.exit_button.setFont(font)
        self.exit_button.setObjectName("exit_button")
        self.choice_date_of_birth = QtWidgets.QDateEdit(self.centralwidget)
        self.choice_date_of_birth.setGeometry(QtCore.QRect(660, 80, 210, 30))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.choice_date_of_birth.setFont(font)
        self.choice_date_of_birth.setObjectName("choice_date_of_birth")
        self.story_number_my = QtWidgets.QSpinBox(self.centralwidget)
        self.story_number_my.setGeometry(QtCore.QRect(690, 190, 180, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.story_number_my.setFont(font)
        self.story_number_my.setMinimum(1)
        self.story_number_my.setMaximum(9999999)
        self.story_number_my.setObjectName("story_number_my")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(490, 190, 190, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 886, 17))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.menubar.setFont(font)
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.statusbar.setFont(font)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Новый пациент"))
        self.label.setText(_translate("MainWindow", "ФИО:"))
        self.label_2.setText(_translate("MainWindow", "Номер истории:"))
        self.label_3.setText(_translate("MainWindow", "Категория:"))
        self.label_4.setText(_translate("MainWindow", "Дата рождения:"))
        self.label_5.setText(_translate("MainWindow", "Дата операции:"))
        self.label_6.setText(_translate("MainWindow", "Отделение:"))
        self.label_7.setText(_translate("MainWindow", "Диагноз:"))
        self.label_8.setText(_translate("MainWindow", "Дополнительная информация:"))
        self.save_button.setText(_translate("MainWindow", "Сохранить"))
        self.exit_button.setText(_translate("MainWindow", "Выйти"))
        self.label_9.setText(_translate("MainWindow", "Порядковый номер:"))
