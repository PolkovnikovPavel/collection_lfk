# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'data/design/description_menu.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(690, 675)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.exit_button = QtWidgets.QPushButton(self.centralwidget)
        self.exit_button.setGeometry(QtCore.QRect(10, 10, 130, 30))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.exit_button.setFont(font)
        self.exit_button.setObjectName("exit_button")
        self.text = QtWidgets.QTextBrowser(self.centralwidget)
        self.text.setGeometry(QtCore.QRect(10, 50, 670, 580))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.text.setFont(font)
        self.text.setDocumentTitle("")
        self.text.setPlaceholderText("")
        self.text.setObjectName("text")
        self.copy_link_button = QtWidgets.QPushButton(self.centralwidget)
        self.copy_link_button.setGeometry(QtCore.QRect(470, 10, 210, 30))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.copy_link_button.setFont(font)
        self.copy_link_button.setObjectName("copy_link_button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 690, 18))
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
        self.exit_button.setText(_translate("MainWindow", "Выйти"))
        self.copy_link_button.setText(_translate("MainWindow", "Отправить письмо"))
