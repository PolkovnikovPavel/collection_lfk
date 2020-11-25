import os, sqlite3
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QInputDialog
from PyQt5 import QtCore, QtGui, QtWidgets

from data.design.form_history import Ui_MainWindow as Ui_FormHistory


class HistoryMenu(QMainWindow, Ui_FormHistory):
    def __init__(self, main_menu, ac_name, db_name):
        super().__init__()
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()
        self.main_menu = main_menu
        self.ac_name = ac_name
        self.setupUi(self)
        self.exit_button.clicked.connect(self.open_main_menu)

        self.main_table.setColumnCount(3)
        self.main_table.setHorizontalHeaderLabels([' ', 'дата', 'описание'])

    def create_tabl(self):
        font = QtGui.QFont()
        font.setPointSize(15)
        _translate = QtCore.QCoreApplication.translate

        inquiry = f"""SELECT DISTINCT id FROM accounts WHERE name = '{self.ac_name}'"""
        user_id = self.cur.execute(inquiry).fetchall()[0]

        inquiry = f"""SELECT DISTINCT id, description, is_canceled, is_cancel_button, date
                                                    FROM logs
                                        WHERE user_id = {user_id[0]}"""


    def open_main_menu(self):
        self.close()  # закрывает это окно
        self.main_menu.show()
