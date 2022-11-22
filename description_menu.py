import os, sqlite3, webbrowser
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QInputDialog
from PyQt5 import QtCore, QtGui, QtWidgets
import datetime

from data.design.description_menu import Ui_MainWindow as Ui_Description_menu


text = '''                           Журнал ЛФК (v - 1.10.1)

Данная программа предназначена для:
* Упрощения передачи информации о приверженности пациента.
* Упрощения и автоматизации формирования учетно - отчетной информации сотрудниками выполняющими реабилитационные мероприятия.
* Формирование специализированной базы данных. 

Для обеспечения безопасности, корректности, сохранности базы данных программой могут пользоваться сотрудники имеющие индивидуальный логин и пароль, который присваивается администратором.

Имеются разделы:
* Добавить пациента - сотрудники организации самостоятельно добавляют в базу данных (ФИО, датус диагнозом).
* Добавить процедуры - сотрудники организации самостоятельно добавляют выполнение мероприятий по реабилитации.
* Выписать пациента - сотрудники организации самостоятельно отмечают дату выписки пациента.
* Отчет на один день - сотрудники организации самостоятельно выбирают дату формирования отчета о выполненной работе на один день, который сохраняется в программе excel в указанном месте хранения.
* Отчет на период - сотрудники организации самостоятельно выбирают период, за который программа формирует отчет о выполненной работе, который сохраняется в программе excel в указанном месте хранения.
* Отчет за месяц - сотрудники организации самостоятельно выбирают год и месяц для формирования программой стандартного отчета о выполненной работе, который сохраняется в программе excel в указанном месте хранения.
* Отчет за год - сотрудники организации самостоятельно выбирают год для формирования программой стандартного отчета о выполненной работе, который сохраняется в программе excel в указанном месте хранения.
* Сборный отчет - сотрудники организации самостоятельно выбирают период формирования нестандартного отчета о приверженности, который сохраняется в программе excel в указанном месте хранения.
* История - для возможности внесения исправлений сотрудники организации самостоятельно могут просмотреть и изменить свою историю действий в программе.

Если вы нашли какую-то ошибку или недостаток, то можно писать свои предложения автору на почту pavelpolkovnikov334@gmail.com
'''


class MyPushButton(QtWidgets.QPushButton):
    def set_args(self, args):
        self.args = args


def create_history(self, description):
    inquiry = f"""SELECT DISTINCT id FROM accounts WHERE name = '{self.ac_name}'"""
    user_id = self.cur.execute(inquiry).fetchall()[0]

    now = datetime.datetime.now()
    time = now.strftime('%d-%m-%Y  %H:%M')

    inquiry = f"""INSERT INTO logs (user_id, description, date) 
                            VALUES ({user_id[0]}, '{description}', '{time}')"""
    self.cur.execute(inquiry).fetchall()
    self.con.commit()


class DescriptionMenu(QMainWindow, Ui_Description_menu):
    def __init__(self, main_menu, ac_name, db_name):
        super().__init__()
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()
        self.main_menu = main_menu
        self.ac_name = ac_name
        self.setupUi(self)
        self.exit_button.clicked.connect(self.open_main_menu)
        self.copy_link_button.clicked.connect(self.copy_link)
        self.text.setText(text)
        self.setWindowTitle('О проекте')


    def copy_link(self):
        webbrowser.open('mailto:pavelpolkovnikov334@gmail.com', new=2)   # Написать сообщение на почту

    def resizeEvent(self, event):
        self.text.setGeometry(QtCore.QRect(10, 50, self.width() - 20, self.height() - 95))
        self.copy_link_button.setGeometry(QtCore.QRect(self.width() - 220, 10, 210, 30))

    def open_main_menu(self):
        self.close()  # закрывает это окно
        self.main_menu.show()
