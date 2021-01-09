import os, sqlite3
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QInputDialog
from PyQt5 import QtCore, QtGui, QtWidgets

from data.design.form_history import Ui_MainWindow as Ui_FormHistory


class MyPushButton(QtWidgets.QPushButton):
    def set_args(self, args):
        self.args = args


class HistoryMenu(QMainWindow, Ui_FormHistory):
    def __init__(self, main_menu, ac_name, db_name):
        super().__init__()
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()
        self.main_menu = main_menu
        self.ac_name = ac_name
        self.setupUi(self)
        self.exit_button.clicked.connect(self.open_main_menu)
        self.who_to_show.activated.connect(self.create_tabl)

        self.main_table.setColumnCount(4)
        self.main_table.setHorizontalHeaderLabels([' ', 'врач', 'дата', 'описание'])
        self.main_table.setColumnWidth(0, 120)
        self.main_table.setColumnWidth(1, 100)
        self.main_table.setColumnWidth(2, 200)

        inquiry = f"""SELECT DISTINCT id, name FROM accounts"""
        self.all_doctors = self.cur.execute(inquiry).fetchall()
        self.all_doctors.sort(key=lambda x: str(x[1]))
        self.who_to_show.addItem('всех')
        for doctor in self.all_doctors:
            self.who_to_show.addItem(str(doctor[1]))

        self.create_tabl()


    def create_tabl(self):
        font = QtGui.QFont()
        font.setPointSize(15)
        _translate = QtCore.QCoreApplication.translate

        inquiry = f"""SELECT DISTINCT id, is_admin FROM accounts WHERE name = '{self.ac_name}'"""
        user_id = self.cur.execute(inquiry).fetchone()

        inquiry = f"""SELECT DISTINCT * FROM logs"""
        all_logs = self.cur.execute(inquiry).fetchall()
        self.main_table.setRowCount(len(all_logs))

        for i in range(len(all_logs)):
            log = all_logs[i]
            button = MyPushButton(self.centralwidget)
            button.setFont(font)
            button.set_args(log[0])

            if log[3]:
                button.setText(_translate("MainWindow", "Востановить"))
                button.clicked.connect(self.restore_log)
                if log[1] != user_id[0] and user_id[1] == 0:
                    button.setDisabled(True)
                else:
                    button.setStyleSheet("background-color: #FEC2A0")
            else:
                button.setText(_translate("MainWindow", "Удалить"))
                button.clicked.connect(self.cancel_log)
                if log[1] != user_id[0] and user_id[1] == 0:
                    button.setDisabled(True)
                else:
                    button.setStyleSheet("background-color: #FE9895")

            date = QtWidgets.QLineEdit(str(log[4]))
            date.setFont(font)

            inquiry = f"""SELECT DISTINCT short_name FROM accounts WHERE id = '{log[1]}'"""
            doctor_name = self.cur.execute(inquiry).fetchone()[0]
            doctor_name = QtWidgets.QLineEdit(str(doctor_name))
            doctor_name.setFont(font)

            text = ''
            description = log[2]
            if 'discharge' in description:
                patient_id = description.split(';')[1]
                inquiry = f"""SELECT DISTINCT full_name, story_number FROM patients WHERE id = {patient_id}"""
                data = self.cur.execute(inquiry).fetchone()
                text = f'выписан пациент, ФИО: {data[0]}\nномер истории: {data[1]}'


            description = QtWidgets.QLineEdit(text)
            description.setFont(font)

            self.main_table.setCellWidget(i, 0, button)
            self.main_table.setCellWidget(i, 1, doctor_name)
            self.main_table.setCellWidget(i, 2, date)
            self.main_table.setCellWidget(i, 3, description)

    def resizeEvent(self, event):
        self.main_table.setGeometry(QtCore.QRect(10, 120, self.width() - 20, self.height() - 150))
        self.main_table.setColumnWidth(3, self.width() - 470)

    def cancel_log(self):
        pass

    def restore_log(self):
        pass

    def open_main_menu(self):
        self.close()  # закрывает это окно
        self.main_menu.show()
