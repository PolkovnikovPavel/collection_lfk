import os, sqlite3
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QInputDialog
from PyQt5 import QtCore, QtGui, QtWidgets

from data.design.form_admin_menu import Ui_FormMainMenu as Ui_FormAdminMenu


class MyPushButton(QtWidgets.QPushButton):
    def set_args(self, args):
        self.args = args



class AdminMenu(QMainWindow, Ui_FormAdminMenu):
    def __init__(self, main_menu, ac_name, db_name):
        super().__init__()
        self.main_menu = main_menu
        self.ac_name = ac_name
        self.setupUi(self)
        self.out_button.clicked.connect(self.open_main_menu)
        self.button_place.clicked.connect(self.create_places)
        self.categories_button.clicked.connect(self.create_categories)
        self.departments_button.clicked.connect(self.create_departments)
        self.new_doktor_button.clicked.connect(self.create_new_user)
        self.button_add.clicked.connect(self.add_new_place)
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()

        self.create_places()


    def create_new_user(self):
        self.name_category.setText('Исполнители')
        font = QtGui.QFont()
        font.setPointSize(15)
        _translate = QtCore.QCoreApplication.translate

        inquiry = f"""SELECT DISTINCT name, short_name FROM accounts"""
        names = self.cur.execute(inquiry).fetchall()
        self.all_users = []
        for name in names:
            self.all_users.append(name[0])

        for i in range(self.main_table.rowCount()):
            self.main_table.removeRow(0)

        self.main_table.setRowCount(len(names))
        self.main_table.setColumnCount(5)
        self.main_table.setColumnWidth(0, 120)
        self.main_table.setColumnWidth(1, 105)
        self.main_table.setColumnWidth(2, 240)
        self.main_table.setColumnWidth(3, 100)
        self.main_table.setColumnWidth(4, 105)
        self.main_table.setHorizontalHeaderLabels(['', '', 'полное имя', 'короткое', 'пароль'])

        for i in range(len(names)):
            button_1 = MyPushButton(self.centralwidget)
            button_1.setFont(font)
            button_1.set_args((names[i][0], i))

            inquiry = f"""SELECT DISTINCT is_deleted FROM accounts
                                            WHERE name = '{names[i][0]}'"""
            is_deleted = self.cur.execute(inquiry).fetchone()[0]

            if is_deleted:
                button_1.setText(_translate("MainWindow", "Востановить"))
                button_1.clicked.connect(self.restore_user)
                button_1.setStyleSheet("background-color: #FEC2A0")
            else:
                button_1.setText(_translate("MainWindow", "Удалить"))
                button_1.clicked.connect(self.del_user)
                button_1.setStyleSheet("background-color: #FE9895")

            inquiry = f"""SELECT DISTINCT is_admin FROM accounts
                                    WHERE name = '{names[i][0]}'"""
            rez = self.cur.execute(inquiry).fetchone()
            if rez[0]:
                button_1.setDisabled(True)

            button_2 = MyPushButton(self.centralwidget)
            button_2.setFont(font)
            button_2.set_args((names[i][0], i))
            button_2.setText(_translate("MainWindow", "Сохранить"))
            button_2.clicked.connect(self.save_user)
            button_2.setStyleSheet("background-color: #FFFAA0")


            name = QtWidgets.QLineEdit(str(names[i][0]))
            name.setFont(font)

            short_name = QtWidgets.QLineEdit(str(names[i][1]))
            short_name.setFont(font)

            inquiry = f"""SELECT DISTINCT password FROM accounts
                                        WHERE name = '{names[i][0]}'"""
            password = self.cur.execute(inquiry).fetchone()[0]
            password = QtWidgets.QLineEdit(str(password))
            password.setFont(font)

            self.main_table.setCellWidget(i, 0, button_1)
            self.main_table.setCellWidget(i, 1, button_2)
            self.main_table.setCellWidget(i, 2, name)
            self.main_table.setCellWidget(i, 3, short_name)
            self.main_table.setCellWidget(i, 4, password)

        self.button_add.clicked.disconnect()
        self.button_add.clicked.connect(self.add_new_user)
        self.new_name.setText('')

    def create_places(self):
        self.name_category.setText('Способ реабилитации')
        font = QtGui.QFont()
        font.setPointSize(15)
        _translate = QtCore.QCoreApplication.translate

        inquiry = f"""SELECT DISTINCT name, price, short_name FROM places"""
        names = self.cur.execute(inquiry).fetchall()
        self.all_places = []
        for name in names:
            self.all_places.append(name[0])

        for i in range(self.main_table.rowCount()):
            self.main_table.removeRow(0)

        self.main_table.setRowCount(len(names))
        self.main_table.setColumnCount(5)
        self.main_table.setColumnWidth(0, 120)
        self.main_table.setColumnWidth(1, 105)
        self.main_table.setColumnWidth(2, 240)
        self.main_table.setColumnWidth(3, 100)
        self.main_table.setColumnWidth(4, 130)
        self.main_table.setHorizontalHeaderLabels(['', '', 'название', 'сокр. имя', 'условные ед.'])

        for i in range(len(names)):
            button_1 = MyPushButton(self.centralwidget)
            button_1.setFont(font)
            button_1.set_args((names[i][0], i))

            inquiry = f"""SELECT DISTINCT is_deleted FROM places
                                WHERE name = '{names[i][0]}'"""
            is_deleted = self.cur.execute(inquiry).fetchone()[0]

            if is_deleted:
                button_1.setText(_translate("MainWindow", "Востановить"))
                button_1.clicked.connect(self.restore_place)
                button_1.setStyleSheet("background-color: #FEC2A0")
            else:
                button_1.setText(_translate("MainWindow", "Удалить"))
                button_1.clicked.connect(self.del_place)
                button_1.setStyleSheet("background-color: #FE9895")

            button_2 = MyPushButton(self.centralwidget)
            button_2.setFont(font)
            button_2.set_args((names[i][0], i))
            button_2.setText(_translate("MainWindow", "Сохранить"))
            button_2.clicked.connect(self.save_place)
            button_2.setStyleSheet("background-color: #FFFAA0")


            name = QtWidgets.QLineEdit(str(names[i][0]))
            name.setFont(font)

            short_name = QtWidgets.QLineEdit(str(names[i][2]))
            short_name.setFont(font)

            price = QtWidgets.QLineEdit(str(names[i][1]))
            price.setFont(font)

            self.main_table.setCellWidget(i, 0, button_1)
            self.main_table.setCellWidget(i, 1, button_2)
            self.main_table.setCellWidget(i, 2, name)
            self.main_table.setCellWidget(i, 3, short_name)
            self.main_table.setCellWidget(i, 4, price)

        self.button_add.clicked.disconnect()
        self.button_add.clicked.connect(self.add_new_place)
        self.new_name.setText('')

    def create_categories(self):
        self.name_category.setText('Категории пациентов')
        font = QtGui.QFont()
        font.setPointSize(15)
        _translate = QtCore.QCoreApplication.translate

        inquiry = f"""SELECT DISTINCT name FROM categories"""
        names = self.cur.execute(inquiry).fetchall()

        self.all_categories = []
        for name in names:
            self.all_categories.append(name[0])

        for i in range(self.main_table.rowCount()):
            self.main_table.removeRow(0)

        self.main_table.setRowCount(len(names))
        self.main_table.setColumnCount(3)
        self.main_table.setColumnWidth(0, 120)
        self.main_table.setColumnWidth(1, 105)
        self.main_table.setColumnWidth(2, 240)
        self.main_table.setHorizontalHeaderLabels(['', '', 'название'])

        for i in range(len(names)):
            button_1 = MyPushButton(self.centralwidget)
            button_1.setFont(font)
            button_1.set_args((names[i][0], i))

            inquiry = f"""SELECT DISTINCT is_deleted FROM categories
                                            WHERE name = '{names[i][0]}'"""
            is_deleted = self.cur.execute(inquiry).fetchone()[0]

            if is_deleted:
                button_1.setText(_translate("MainWindow", "Востановить"))
                button_1.clicked.connect(self.restore_categori)
                button_1.setStyleSheet("background-color: #FEC2A0")
            else:
                button_1.setText(_translate("MainWindow", "Удалить"))
                button_1.clicked.connect(self.del_categori)
                button_1.setStyleSheet("background-color: #FE9895")

            button_2 = MyPushButton(self.centralwidget)
            button_2.setFont(font)
            button_2.set_args((names[i][0], i))
            button_2.setText(_translate("MainWindow", "Сохранить"))
            button_2.clicked.connect(self.save_categori)
            button_2.setStyleSheet("background-color: #FFFAA0")

            name = QtWidgets.QLineEdit(str(names[i][0]))
            name.setFont(font)

            self.main_table.setCellWidget(i, 0, button_1)
            self.main_table.setCellWidget(i, 1, button_2)
            self.main_table.setCellWidget(i, 2, name)

        self.button_add.clicked.disconnect()
        self.button_add.clicked.connect(self.add_new_categori)
        self.new_name.setText('')

    def create_departments(self):
        self.name_category.setText('Отделения стационара')
        font = QtGui.QFont()
        font.setPointSize(15)
        _translate = QtCore.QCoreApplication.translate

        inquiry = f"""SELECT DISTINCT name FROM departments"""
        names = self.cur.execute(inquiry).fetchall()

        self.all_departments = []
        for name in names:
            self.all_departments.append(name[0])

        for i in range(self.main_table.rowCount()):
            self.main_table.removeRow(0)

        self.main_table.setRowCount(len(names))
        self.main_table.setColumnCount(3)
        self.main_table.setColumnWidth(0, 120)
        self.main_table.setColumnWidth(1, 105)
        self.main_table.setColumnWidth(2, 240)
        self.main_table.setHorizontalHeaderLabels(['', '', 'название'])

        for i in range(len(names)):
            button_1 = MyPushButton(self.centralwidget)
            button_1.setFont(font)
            button_1.set_args((names[i][0], i))

            inquiry = f"""SELECT DISTINCT is_deleted FROM departments
                                WHERE name = '{names[i][0]}'"""
            is_deleted = self.cur.execute(inquiry).fetchone()[0]

            if is_deleted:
                button_1.setText(_translate("MainWindow", "Востановить"))
                button_1.clicked.connect(self.restore_department)
                button_1.setStyleSheet("background-color: #FEC2A0")
            else:
                button_1.setText(_translate("MainWindow", "Удалить"))
                button_1.clicked.connect(self.del_department)
                button_1.setStyleSheet("background-color: #FE9895")

            button_2 = MyPushButton(self.centralwidget)
            button_2.setFont(font)
            button_2.set_args((names[i][0], i))
            button_2.setText(_translate("MainWindow", "Сохранить"))
            button_2.clicked.connect(self.save_department)
            button_2.setStyleSheet("background-color: #FFFAA0")

            name = QtWidgets.QLineEdit(str(names[i][0]))
            name.setFont(font)

            self.main_table.setCellWidget(i, 0, button_1)
            self.main_table.setCellWidget(i, 1, button_2)
            self.main_table.setCellWidget(i, 2, name)

        self.button_add.clicked.disconnect()
        self.button_add.clicked.connect(self.add_new_department)
        self.new_name.setText('')

    def del_place(self):
        name = self.sender().args[0]
        inquiry = f"""UPDATE places
                    SET is_deleted = 1
                        WHERE name = '{name}'"""

        self.cur.execute(inquiry)
        self.con.commit()
        self.create_places()

    def restore_place(self):
        name = self.sender().args[0]
        inquiry = f"""UPDATE places
                            SET is_deleted = 0
                                WHERE name = '{name}'"""

        self.cur.execute(inquiry)
        self.con.commit()
        self.create_places()

    def save_place(self):
        name = self.sender().args[0]
        price = self.main_table.cellWidget(self.sender().args[1], 4).text()
        short_name = self.main_table.cellWidget(self.sender().args[1], 3).text()
        try:
            price = float('.'.join(price.split(',')))
        except Exception:
            self.create_places()
            return
        call = self.main_table.cellWidget(self.sender().args[1], 2)
        inquiry = f"""UPDATE places
                            SET name = '{call.text()}', price = {price}, short_name = '{short_name}'
                                WHERE name = '{name}'"""

        self.cur.execute(inquiry)
        self.con.commit()
        self.create_places()

    def del_categori(self):
        name = self.sender().args[0]
        inquiry = f"""UPDATE categories
                            SET is_deleted = 1
                                WHERE name = '{name}'"""
        self.cur.execute(inquiry)
        self.con.commit()
        self.create_categories()

    def restore_categori(self):
        name = self.sender().args[0]
        inquiry = f"""UPDATE categories
                            SET is_deleted = 0
                                WHERE name = '{name}'"""
        self.cur.execute(inquiry)
        self.con.commit()
        self.create_categories()

    def save_categori(self):
        name = self.sender().args[0]
        call = self.main_table.cellWidget(self.sender().args[1], 2)
        inquiry = f"""UPDATE categories
                            SET name = '{call.text()}'
                                WHERE name = '{name}'"""

        self.cur.execute(inquiry)
        self.con.commit()
        self.create_categories()

    def del_department(self):
        name = self.sender().args[0]
        inquiry = f"""UPDATE departments
                        SET is_deleted = 1
                            WHERE name = '{name}'"""
        self.cur.execute(inquiry)
        self.con.commit()
        self.create_departments()

    def restore_department(self):
        name = self.sender().args[0]
        inquiry = f"""UPDATE departments
                            SET is_deleted = 0
                                WHERE name = '{name}'"""
        self.cur.execute(inquiry)
        self.con.commit()
        self.create_departments()

    def save_department(self):
        name = self.sender().args[0]
        call = self.main_table.cellWidget(self.sender().args[1], 2)
        inquiry = f"""UPDATE departments
                        SET name = '{call.text()}'
                            WHERE name = '{name}'"""
        self.cur.execute(inquiry)
        self.con.commit()
        self.create_departments()

    def del_user(self):
        inquiry = f"""UPDATE accounts
                        SET is_deleted = 1
                            WHERE name = '{self.sender().args[0]}'"""
        self.cur.execute(inquiry)
        self.con.commit()
        self.create_new_user()

    def restore_user(self):
        inquiry = f"""UPDATE accounts
                        SET is_deleted = 0
                            WHERE name = '{self.sender().args[0]}'"""
        self.cur.execute(inquiry)
        self.con.commit()
        self.create_new_user()

    def save_user(self):
        call_name = self.main_table.cellWidget(self.sender().args[1], 2)
        call_short_name = self.main_table.cellWidget(self.sender().args[1], 3)
        call_pass = self.main_table.cellWidget(self.sender().args[1], 4)

        if call_name.text() in list(filter(lambda x: x != call_name.text(), self.all_users)):
            self.create_new_user()
            return

        inquiry = f"""UPDATE accounts
                        SET name = '{call_name.text()}', password = '{call_pass.text()}', short_name = '{call_short_name.text()}'
                            WHERE name = '{self.sender().args[0]}'"""
        self.cur.execute(inquiry)
        self.con.commit()
        self.create_new_user()

    def add_new_place(self):
        text = self.new_name.text()
        if len(self.new_name.text().split()) == 0 or text in self.all_places:
            return

        inquiry = f"""INSERT INTO places (name) 
                            VALUES ('{self.new_name.text()}')"""
        self.cur.execute(inquiry).fetchall()
        self.con.commit()

        self.create_places()

    def add_new_categori(self):
        text = self.new_name.text()
        if len(self.new_name.text().split()) == 0 or text in self.all_categories:
            return

        inquiry = f"""INSERT INTO categories (name) 
                            VALUES ('{self.new_name.text()}')"""
        self.cur.execute(inquiry).fetchall()
        self.con.commit()

        self.create_categories()

    def add_new_department(self):
        text = self.new_name.text()
        if len(self.new_name.text().split()) == 0 or text in self.all_departments:
            return

        inquiry = f"""INSERT INTO departments (name) 
                            VALUES ('{self.new_name.text()}')"""
        self.cur.execute(inquiry).fetchall()
        self.con.commit()

        self.create_departments()

    def add_new_user(self):
        text = self.new_name.text()
        if len(self.new_name.text().split()) == 0 or text in self.all_users:
            return
        password, ok = QInputDialog.getText(self, 'Ввод пароля', 'Придумайте пароль')
        if ok:
            short_name, ok = QInputDialog.getText(self, 'Ввод короткого имяни',
                                                'Введите короткое имя')
            if ok:
                inquiry = f"""INSERT INTO accounts (name, password, is_admin, short_name) 
                                            VALUES ('{text}', '{password}', 0, '{short_name}')"""
                self.cur.execute(inquiry).fetchall()
                self.con.commit()
                self.create_new_user()
        else:
            return

    def open_main_menu(self):
        self.close()  # закрывает это окно
        self.main_menu.show()

    def resizeEvent(self, event):
        self.main_table.setGeometry(QtCore.QRect(180, 140, self.width() - 200, self.height() - 170))
        self.main_table.setColumnWidth(2, self.width() - 700)

