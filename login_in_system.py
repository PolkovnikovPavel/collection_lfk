import os, sqlite3, subprocess
from PyQt5.QtWidgets import QMainWindow, QFileDialog

from backup_copies import get_appdata_folder
from data.design.form_account_login import Ui_FormAccountLogin
from main_menu import *


class LoggingInSystem(QMainWindow, Ui_FormAccountLogin):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.is_db = False
        self.is_backup = False
        self.check()
        # if self.is_db:
        #     self.check_correct()

        self.button_db.clicked.connect(self.open_db)
        self.button_enter_accaunt.clicked.connect(self.enter_to_accaunt)
        self.button_oben_backups.clicked.connect(self.open_folder_backups)
        self.password.setFocus()

    def enter_to_accaunt(self):  # вызывается при нажатии на кнопку "Войти"
        if self.is_db:
            name = self.list_names.currentText()
            pas = self.password.text()

            inquiry = f"""SELECT DISTINCT password FROM accounts
                                WHERE name = '{name}'"""
            cur = self.con.cursor()
            right_pas = cur.execute(inquiry).fetchone()
            if str(right_pas[0]) == pas:
                self.open_main_menu(name)
            else:
                self.text_error.setText('Не верный пароль')

    def check(self):
        if os.path.isfile('options.txt'):
            try:
                with open('options.txt') as file:
                    db_name = file.read().split('\n')[0]
                    if not os.path.isfile(db_name):
                        if db_name != '':
                            db_name = 'nr'
            except Exception:
                with open('options.txt', 'w') as file:
                    file.write('')
                db_name = ''
        else:
            with open('options.txt', 'w') as file:
                file.write('')
            db_name = ''

        if db_name != 'nr':
            self.con = sqlite3.connect(db_name)

        if db_name != '' and db_name != 'nr':
            try:
                inquiry = f"""SELECT DISTINCT name FROM accounts
                                    WHERE is_deleted = 0"""
                cur = self.con.cursor()  # этот запрос получает всех пользователей
                all_names = cur.execute(inquiry).fetchall()
                self.is_db = True
                self.db_name = db_name
                for name in all_names:  # добавление вариантов выбора
                    self.list_names.addItem(str(name[0]))
            except Exception:
                db_name == 'nf'

        if db_name == '':
            self.text_error.setText('Файл базы данных не указан!')
        elif db_name == 'nr':
            self.text_error.setText('Выбранного файла не существует!')
        elif db_name.split('.')[-1] != 'db':
            self.text_error.setText('База данных выбрана не правильно!')
        else:
            self.text_error.setText('')

    def open_db(self):
        fname = QFileDialog.getOpenFileName(self, 'Укажите путь к базе данных')[0]
        if fname:
            with open('options.txt', 'w') as file:
                file.write(fname)
            self.open_self()

    def open_folder_backups(self):
        subprocess.run(['explorer', get_appdata_folder()], shell=True)

    def open_main_menu(self, name):
        self.password.setText('')
        self.main_menu_window = MainMenu(self, name, self.db_name)
        self.close()  # закрывает это окно
        self.main_menu_window.show()  # отображает окно главного меню

    def open_self(self):
        self.login_window = LoggingInSystem()
        self.close()  # закрывает это окно
        self.login_window.show()  # отображает это же окно
