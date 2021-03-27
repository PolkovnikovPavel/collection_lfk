import os, sqlite3
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QInputDialog
from PyQt5 import QtCore, QtGui, QtWidgets
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta

from data.design.form_history import Ui_MainWindow as Ui_FormHistory


class MyPushButton(QtWidgets.QPushButton):
    def set_args(self, args):
        self.args = args


periods = {'1 день': 1, '7 дней': 7, '14 дней': 14, '1 месяц': 30, '2 месяца': 61, '3 месяц': 92, '6 месяцов': 183, '1 год': 365}
types = {'все': '',
         'Запись пациента': 'add_patient',
         'Выписка пациента': 'discharge',
         'Изменение данных о пациенте': 'c_patient',
         'Изменение дополнительной информации': 'memo_s',
         'Добавление нового дня процедур': 'add_record',
         'Изменение места проведения процедуры': 's_cheng_p',
         'Изменение исполнителя процедуры': 's_cheng_d',
         'Удаление дня процедур': 'del_record',
         'Востановление дня процедур': 'restore_record'}


def create_history(self, description):
    inquiry = f"""SELECT DISTINCT id FROM accounts WHERE name = '{self.ac_name}'"""
    user_id = self.cur.execute(inquiry).fetchall()[0]

    now = datetime.datetime.now()
    time = now.strftime('%d-%m-%Y  %H:%M')

    inquiry = f"""INSERT INTO logs (user_id, description, date) 
                            VALUES ({user_id[0]}, '{description}', '{time}')"""
    self.cur.execute(inquiry).fetchall()
    self.con.commit()


def get_datetime_from_text(text):
    text = text.split('-')
    datetime_date = date(day=int(text[0]), month=int(text[1]), year=int(text[2]))
    return datetime_date


def get_datetime_date_from_calendar(calendar):
    calendar_date = calendar.date()
    datetime_date = date(day=calendar_date.day(), month=calendar_date.month(),
                         year=calendar_date.year())
    return datetime_date


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
        self.type_of_log.activated.connect(self.create_tabl)
        self.number_days.activated.connect(self.create_tabl)

        self.main_table.setColumnCount(4)
        self.main_table.setHorizontalHeaderLabels([' ', 'врач', 'дата', 'описание'])
        self.main_table.setColumnWidth(0, 200)
        self.main_table.setColumnWidth(1, 100)
        self.main_table.setColumnWidth(2, 250)

        inquiry = f"""SELECT DISTINCT id, name FROM accounts"""
        self.all_doctors = self.cur.execute(inquiry).fetchall()
        self.all_doctors.sort(key=lambda x: str(x[1]))
        self.who_to_show.addItem('всех')
        for doctor in self.all_doctors:
            self.who_to_show.addItem(str(doctor[1]))

        for period in periods:
            self.number_days.addItem(period)
        self.number_days.setCurrentIndex(2)
        for type in types:
            self.type_of_log.addItem(type)
        self.type_of_log.setCurrentIndex(1)

        now = datetime.datetime.now()
        self.date_start.setDate(QtCore.QDate(now.year, now.month, now.day))

        self.create_tabl()

    def create_tabl(self):
        font = QtGui.QFont()
        font.setPointSize(15)
        _translate = QtCore.QCoreApplication.translate

        inquiry = f"""SELECT DISTINCT id, is_admin FROM accounts WHERE name = '{self.ac_name}'"""
        user_id = self.cur.execute(inquiry).fetchone()

        if self.who_to_show.currentText() == 'всех' and self.type_of_log.currentText() == 'все':
            inquiry = f"""SELECT DISTINCT * FROM logs"""
        else:
            users_sort = ''
            types_sort = ''
            for id, name in self.all_doctors:
                if str(name) == self.who_to_show.currentText():
                    users_sort = f'user_id = {id}'
                    break
            types_sort = f'description LIKE "{types[self.type_of_log.currentText()]}%"'

            if self.type_of_log.currentText() == 'все':
                inquiry = f"""SELECT DISTINCT * FROM logs WHERE {users_sort}"""
            elif self.who_to_show.currentText() == 'всех':
                inquiry = f"""SELECT DISTINCT * FROM logs WHERE {types_sort}"""
            else:
                inquiry = f"""SELECT DISTINCT * FROM logs WHERE {types_sort} and {users_sort}"""

        all_logs = self.cur.execute(inquiry).fetchall()
        self.main_table.setRowCount(len(all_logs))

        count_days = periods[self.number_days.currentText()]
        start_date = get_datetime_date_from_calendar(self.date_start)
        count_logs = -1

        for i in range(len(all_logs)):
            log = all_logs[::-1][i]

            date = get_datetime_from_text(log[4].split(' ')[0])

            if (start_date - date).days < count_days and (start_date - date).days >= 0:
                button = MyPushButton(self.centralwidget)
                button.setFont(font)
                button.set_args(log[0])

                count_logs += 1
                if log[3]:
                    button.setText(_translate("MainWindow", "Востановить"))
                    button.clicked.connect(self.restore_log)
                    if log[1] != user_id[0] and user_id[1] == 0:
                        button.setDisabled(True)
                    else:
                        button.setStyleSheet("background-color: #FEC2A0")
                else:
                    button.setText(_translate("MainWindow", "Отменить"))
                    button.clicked.connect(self.cancel_log)
                    if log[1] != user_id[0] and user_id[1] == 0:
                        button.setDisabled(True)
                    else:
                        button.setStyleSheet("background-color: #FE9895")

                date = QtWidgets.QLineEdit(str(log[4]))
                date.setFont(font)

                inquiry = f"""SELECT DISTINCT short_name FROM accounts WHERE id = {log[1]}"""
                doctor_name = self.cur.execute(inquiry).fetchone()[0]
                doctor_name = QtWidgets.QLineEdit(str(doctor_name))
                doctor_name.setFont(font)

                text = ''
                description = log[2]
                if 'discharge' in description:
                    patient_id = description.split(';')[1]
                    inquiry = f"""SELECT DISTINCT full_name, story_number FROM patients WHERE id = {patient_id}"""
                    data = self.cur.execute(inquiry).fetchone()
                    text = f'Выписан пациент, № истории: {data[1]}, ФИО: {data[0]}'
                elif 'add_patient' in description:
                    patient_id = description.split(';')[1]
                    inquiry = f"""SELECT DISTINCT full_name, story_number FROM patients WHERE id = {patient_id}"""
                    data = self.cur.execute(inquiry).fetchone()
                    text = f'Записан новый пациент, № истории: {data[1]}, ФИО: {data[0]}'
                elif 'add_record' in description:
                    record_id = description.split(';')[1]
                    inquiry = f"""SELECT DISTINCT full_name, story_number, date FROM records, patients
                            WHERE records.id = {record_id} and patients.id = records.patient_id"""
                    record = self.cur.execute(inquiry).fetchone()
                    text = f'Добавлен новый день процедур за {record[2]} у "{record[0]}" ({record[1]})'
                elif 'del_record' in description:
                    record_id = description.split(';')[1]
                    inquiry = f"""SELECT DISTINCT full_name, story_number, date FROM records, patients
                            WHERE records.id = {record_id} and patients.id = records.patient_id"""
                    record = self.cur.execute(inquiry).fetchone()
                    text = f'Удалён день процедур за {record[2]} у "{record[0]}" ({record[1]})'
                elif 'restore_record' in description:
                    record_id = description.split(';')[1]
                    inquiry = f"""SELECT DISTINCT full_name, story_number, date FROM records, patients
                            WHERE records.id = {record_id} and patients.id = records.patient_id"""
                    record = self.cur.execute(inquiry).fetchone()
                    text = f'Востановлен день процедур за {record[2]} у {record[0]} ({record[1]})'
                elif 's_cheng_p' in description:
                    lesson_id = description.split(';')[3]
                    old_place_id = description.split(';')[1]
                    place_id = description.split(';')[2]
                    if int(old_place_id) != 0:
                        inquiry = f"""SELECT DISTINCT name FROM places WHERE id = {old_place_id}"""
                        old_place_name = self.cur.execute(inquiry).fetchone()[0]
                    else:
                        old_place_name = '------'
                    if int(place_id) != 0:
                        inquiry = f"""SELECT DISTINCT name FROM places WHERE id = {place_id}"""
                        new_place_name = self.cur.execute(inquiry).fetchone()[0]
                    else:
                        new_place_name = '------'
                    inquiry = f"""SELECT DISTINCT records.id FROM records
                            WHERE {lesson_id} = lesson_id_1 or {lesson_id} = lesson_id_2 or {lesson_id} = lesson_id_3"""
                    record_id = self.cur.execute(inquiry).fetchone()[0]

                    inquiry = f"""SELECT DISTINCT full_name, story_number, date FROM records, patients
                                            WHERE records.id = {record_id} and patients.id = records.patient_id"""
                    record = self.cur.execute(inquiry).fetchone()
                    text = f'Изменено место проведения процедуры с "{old_place_name}" на "{new_place_name}" {record[2]} у "{record[0]}" ({record[1]})'
                elif 's_cheng_d' in description:
                    lesson_id = description.split(';')[3]
                    old_doctor_id = description.split(';')[1]
                    doctor_id = description.split(';')[2]
                    if int(old_doctor_id) != 0:
                        inquiry = f"""SELECT DISTINCT short_name FROM accounts WHERE id = {old_doctor_id}"""
                        old_doctor_name = self.cur.execute(inquiry).fetchone()[0]
                    else:
                        old_doctor_name = '------'
                    if int(doctor_id) != 0:
                        inquiry = f"""SELECT DISTINCT short_name FROM accounts WHERE id = {doctor_id}"""
                        new_doctor_name = self.cur.execute(inquiry).fetchone()[0]
                    else:
                        new_doctor_name = '------'
                    inquiry = f"""SELECT DISTINCT records.id FROM records
                            WHERE {lesson_id} = lesson_id_1 or {lesson_id} = lesson_id_2 or {lesson_id} = lesson_id_3"""
                    record_id = self.cur.execute(inquiry).fetchone()[0]
                    inquiry = f"""SELECT DISTINCT full_name, story_number, date FROM records, patients
                                        WHERE records.id = {record_id} and patients.id = records.patient_id"""
                    record = self.cur.execute(inquiry).fetchone()
                    text = f'Изменён исполнитель процедуры с "{old_doctor_name}" на "{new_doctor_name}" {record[2]} у "{record[0]}" ({record[1]})'
                elif 'memo_s' in description:
                    old_text = description.split(';')[1]
                    new_text = description.split(';')[2]
                    id_patient = description.split(';')[3]
                    inquiry = f"""SELECT DISTINCT full_name, story_number FROM patients
                                            WHERE patients.id = {id_patient}"""
                    patient = self.cur.execute(inquiry).fetchone()
                    text = f'Изменена доп. информация у "{patient[0]}" ({patient[1]}) с "{old_text}" на "{new_text}"'
                elif 'c_patient' in description:
                    id_patient = description.split(';')[1]
                    old_full_name = description.split(';')[2]
                    new_full_name = description.split(';')[3]
                    old_date_of_birth = description.split(';')[4]
                    new_date_of_birth = description.split(';')[5]
                    old_story_number = description.split(';')[6]
                    new_story_number = description.split(';')[7]
                    old_category = description.split(';')[8]
                    new_category = description.split(';')[9]
                    old_diagnosis = description.split(';')[10]
                    new_diagnosis = description.split(';')[11]
                    old_department = description.split(';')[12]
                    new_department = description.split(';')[13]
                    old_memo = description.split(';')[14]
                    new_memo = description.split(';')[15]
                    old_date_of_operation = description.split(';')[16]
                    new_date_of_operation = description.split(';')[17]
                    old_story_number_my = description.split(';')[18]
                    new_story_number_my = description.split(';')[19]

                    inquiry = f"""SELECT DISTINCT full_name, story_number FROM patients WHERE patients.id = {id_patient}"""
                    patient = self.cur.execute(inquiry).fetchone()
                    text = f'Изменён пациент "{patient[0]}" ({patient[1]}): '
                    if old_full_name != new_full_name:
                        text += f'ФИО (было "{old_full_name}", стало "{new_full_name}"), '
                    if old_date_of_birth != new_date_of_birth:
                        text += f'Дата рождения (было {old_date_of_birth}, стало {new_date_of_birth}), '
                    if old_story_number != new_story_number:
                        text += f'Номер истории (было {old_story_number}, стало {new_story_number}), '
                    if old_category != new_category:
                        inquiry = f"""SELECT DISTINCT name FROM categories WHERE id = {old_category}"""
                        old_category = self.cur.execute(inquiry).fetchone()
                        inquiry = f"""SELECT DISTINCT name FROM categories WHERE id = {new_category}"""
                        new_category = self.cur.execute(inquiry).fetchone()
                        text += f'Категория (было "{old_category[0]}", стало "{new_category[0]}"), '
                    if old_diagnosis != new_diagnosis:
                        text += f'диагноз (было "{old_diagnosis}", стало "{new_diagnosis}"), '
                    if old_department != new_department:
                        inquiry = f"""SELECT DISTINCT name FROM departments WHERE id = {old_department}"""
                        old_department = self.cur.execute(inquiry).fetchone()
                        inquiry = f"""SELECT DISTINCT name FROM departments WHERE id = {new_department}"""
                        new_department = self.cur.execute(inquiry).fetchone()
                        text += f'Отделение (было "{old_department[0]}", стало "{new_department[0]}"), '
                    if old_memo.split() != new_memo.split():
                        text += f'Описание (было "{old_memo}", стало "{new_memo}"), '
                    if old_date_of_operation != new_date_of_operation:
                        text += f'Дата опирации (было {old_date_of_operation}, стало {new_date_of_operation}), '
                    if old_story_number_my != new_story_number_my:
                        text += f'Порядковый номер (было {old_story_number_my}, стало {new_story_number_my}), '

                description = QtWidgets.QLineEdit(text)
                description.setFont(font)

                self.main_table.setCellWidget(count_logs, 0, button)
                self.main_table.setCellWidget(count_logs, 1, doctor_name)
                self.main_table.setCellWidget(count_logs, 2, date)
                self.main_table.setCellWidget(count_logs, 3, description)
        self.main_table.setRowCount(count_logs + 1)

    def resizeEvent(self, event):
        self.main_table.setGeometry(QtCore.QRect(10, 120, self.width() - 20, self.height() - 150))
        self.main_table.setColumnWidth(3, self.width() - 660)
        w = (self.width() - 1050) // 3 + 150
        self.type_of_log.setGeometry(QtCore.QRect(890, 80, w, 30))


    def cancel_log(self):
        memo_id = self.sender().args
        inquiry = f"""SELECT DISTINCT * FROM logs WHERE id = {memo_id}"""
        log = self.cur.execute(inquiry).fetchone()
        description = log[2]

        if 'discharge' in description:
            patient_id = description.split(';')[1]
            inquiry = f"""UPDATE patients
                            SET is_discharge = 0
                            WHERE id = {patient_id}"""

            self.cur.execute(inquiry)
            self.con.commit()

            inquiry = f"""UPDATE logs SET is_canceled = 1 WHERE id = {memo_id}"""
            self.cur.execute(inquiry)
            self.con.commit()
        elif 'add_patient' in description:
            patient_id = description.split(';')[1]
            inquiry = f"""UPDATE patients
                            SET is_deleted = 1
                            WHERE id = {patient_id}"""
            self.cur.execute(inquiry)
            self.con.commit()

            inquiry = f"""UPDATE records
                            SET is_deleted = 1
                            WHERE patient_id = {patient_id}"""
            self.cur.execute(inquiry)
            self.con.commit()
            inquiry = f"""UPDATE logs SET is_canceled = 1 WHERE id = {memo_id}"""
            self.cur.execute(inquiry)
            self.con.commit()
        elif 'add_record' in description:
            record_id = description.split(';')[1]
            inquiry = f"""UPDATE records
                            SET is_deleted = 1
                            WHERE id = {record_id}"""
            self.cur.execute(inquiry)
            self.con.commit()

            inquiry = f"""UPDATE logs SET is_canceled = 1 WHERE id = {memo_id}"""
            self.cur.execute(inquiry)
            self.con.commit()
        elif 'del_record' in description:
            record_id = description.split(';')[1]
            inquiry = f"""UPDATE records
                            SET is_deleted = 0
                            WHERE id = {record_id}"""
            self.cur.execute(inquiry)
            self.con.commit()

            inquiry = f"""UPDATE logs SET is_canceled = 1 WHERE id = {memo_id}"""
            self.cur.execute(inquiry)
            self.con.commit()
        elif 'restore_record' in description:
            record_id = description.split(';')[1]
            inquiry = f"""UPDATE records
                            SET is_deleted = 1
                            WHERE id = {record_id}"""
            self.cur.execute(inquiry)
            self.con.commit()

            inquiry = f"""UPDATE logs SET is_canceled = 1 WHERE id = {memo_id}"""
            self.cur.execute(inquiry)
            self.con.commit()
        elif 's_cheng_p' in description:
            lesson_id = description.split(';')[3]
            old_place_id = description.split(';')[1]
            inquiry = f"""UPDATE lessons
                            SET id_plase = {old_place_id}
                            WHERE id = {lesson_id}"""
            self.cur.execute(inquiry)
            self.con.commit()

            inquiry = f"""UPDATE logs SET is_canceled = 1 WHERE id = {memo_id}"""
            self.cur.execute(inquiry)
            self.con.commit()
        elif 's_cheng_d' in description:
            lesson_id = description.split(';')[3]
            old_doctor_id = description.split(';')[1]
            inquiry = f"""UPDATE lessons
                            SET id_doctor = {old_doctor_id}
                            WHERE id = {lesson_id}"""
            self.cur.execute(inquiry)
            self.con.commit()

            inquiry = f"""UPDATE logs SET is_canceled = 1 WHERE id = {memo_id}"""
            self.cur.execute(inquiry)
            self.con.commit()
        elif 'memo_s' in description:
            old_text = description.split(';')[1]
            id_patient = description.split(';')[3]
            inquiry = f"""UPDATE patients
                            SET memo = '{old_text}'
                            WHERE id = {id_patient}"""
            self.cur.execute(inquiry)
            self.con.commit()

            inquiry = f"""UPDATE logs SET is_canceled = 1 WHERE id = {memo_id}"""
            self.cur.execute(inquiry)
            self.con.commit()
        elif 'c_patient' in description:
            id_patient = description.split(';')[1]
            old_full_name = description.split(';')[2]
            old_date_of_birth = description.split(';')[4]
            old_story_number = description.split(';')[6]
            old_category = description.split(';')[8]
            old_diagnosis = description.split(';')[10]
            old_department = description.split(';')[12]
            old_memo = description.split(';')[14]
            old_date_of_operation = description.split(';')[16]
            old_story_number_my = description.split(';')[18]

            inquiry = f"""UPDATE patients
                            SET full_name = '{old_full_name}',
                        date_of_birth = '{old_date_of_birth}', 
                        story_number = {old_story_number},
                        category = {old_category},
                        diagnosis = '{old_diagnosis}',
                        department = {old_department},
                        memo = '{old_memo}',
                        date_of_operation = '{old_date_of_operation}',
                        my_story_number = {old_story_number_my}
                                WHERE id = {id_patient}"""
            self.cur.execute(inquiry).fetchall()
            self.con.commit()
            inquiry = f"""UPDATE logs SET is_canceled = 1 WHERE id = {memo_id}"""
            self.cur.execute(inquiry)
            self.con.commit()

        _translate = QtCore.QCoreApplication.translate
        self.sender().clicked.disconnect()
        self.sender().clicked.connect(self.restore_log)
        self.sender().setText(_translate("MainWindow", "Востановить"))
        self.sender().setStyleSheet("background-color: #FEC2A0")


    def restore_log(self):
        memo_id = self.sender().args
        inquiry = f"""SELECT DISTINCT * FROM logs WHERE id = {memo_id}"""
        log = self.cur.execute(inquiry).fetchone()
        description = log[2]
        if 'discharge' in description:
            patient_id = description.split(';')[1]
            inquiry = f"""UPDATE patients
                            SET is_discharge = 1
                            WHERE id = {patient_id}"""

            self.cur.execute(inquiry)
            self.con.commit()

            inquiry = f"""UPDATE logs SET is_canceled = 0 WHERE id = {memo_id}"""
            self.cur.execute(inquiry)
            self.con.commit()
        elif 'add_patient' in description:
            patient_id = description.split(';')[1]
            inquiry = f"""UPDATE patients
                            SET is_deleted = 0
                            WHERE id = {patient_id}"""
            self.cur.execute(inquiry)
            self.con.commit()
            inquiry = f"""UPDATE records
                            SET is_deleted = 0
                            WHERE patient_id = {patient_id}"""
            self.cur.execute(inquiry)
            self.con.commit()
            inquiry = f"""UPDATE logs SET is_canceled = 0 WHERE id = {memo_id}"""
            self.cur.execute(inquiry)
            self.con.commit()
        elif 'add_record' in description:
            record_id = description.split(';')[1]
            inquiry = f"""UPDATE records
                            SET is_deleted = 0
                            WHERE id = {record_id}"""
            self.cur.execute(inquiry)
            self.con.commit()

            inquiry = f"""UPDATE logs SET is_canceled = 0 WHERE id = {memo_id}"""
            self.cur.execute(inquiry)
            self.con.commit()
        elif 'del_record' in description:
            record_id = description.split(';')[1]
            inquiry = f"""UPDATE records
                            SET is_deleted = 1
                            WHERE id = {record_id}"""
            self.cur.execute(inquiry)
            self.con.commit()

            inquiry = f"""UPDATE logs SET is_canceled = 0 WHERE id = {memo_id}"""
            self.cur.execute(inquiry)
            self.con.commit()
        elif 'restore_record' in description:
            record_id = description.split(';')[1]
            inquiry = f"""UPDATE records
                            SET is_deleted = 0
                            WHERE id = {record_id}"""
            self.cur.execute(inquiry)
            self.con.commit()

            inquiry = f"""UPDATE logs SET is_canceled = 0 WHERE id = {memo_id}"""
            self.cur.execute(inquiry)
            self.con.commit()
        elif 's_cheng_p' in description:
            lesson_id = description.split(';')[3]
            place_id = description.split(';')[2]
            inquiry = f"""UPDATE lessons
                            SET id_plase = {place_id}
                            WHERE id = {lesson_id}"""
            self.cur.execute(inquiry)
            self.con.commit()

            inquiry = f"""UPDATE logs SET is_canceled = 0 WHERE id = {memo_id}"""
            self.cur.execute(inquiry)
            self.con.commit()
        elif 's_cheng_d' in description:
            lesson_id = description.split(';')[3]
            doctor_id = description.split(';')[2]
            inquiry = f"""UPDATE lessons
                            SET id_doctor = {doctor_id}
                            WHERE id = {lesson_id}"""
            self.cur.execute(inquiry)
            self.con.commit()

            inquiry = f"""UPDATE logs SET is_canceled = 0 WHERE id = {memo_id}"""
            self.cur.execute(inquiry)
            self.con.commit()
        elif 'memo_s' in description:
            new_text = description.split(';')[2]
            id_patient = description.split(';')[3]
            inquiry = f"""UPDATE patients
                            SET memo = '{new_text}'
                            WHERE id = {id_patient}"""
            self.cur.execute(inquiry)
            self.con.commit()

            inquiry = f"""UPDATE logs SET is_canceled = 0 WHERE id = {memo_id}"""
            self.cur.execute(inquiry)
            self.con.commit()
        elif 'c_patient' in description:
            id_patient = description.split(';')[1]
            new_full_name = description.split(';')[3]
            new_date_of_birth = description.split(';')[5]
            new_story_number = description.split(';')[7]
            new_category = description.split(';')[9]
            new_diagnosis = description.split(';')[11]
            new_department = description.split(';')[13]
            new_memo = description.split(';')[15]
            new_date_of_operation = description.split(';')[17]
            new_story_number_my = description.split(';')[19]

            inquiry = f"""UPDATE patients
                            SET full_name = '{new_full_name}',
                        date_of_birth = '{new_date_of_birth}', 
                        story_number = {new_story_number},
                        category = {new_category},
                        diagnosis = '{new_diagnosis}',
                        department = {new_department},
                        memo = '{new_memo}',
                        date_of_operation = '{new_date_of_operation}',
                        my_story_number = {new_story_number_my}
                                WHERE id = {id_patient}"""
            self.cur.execute(inquiry).fetchall()
            self.con.commit()
            inquiry = f"""UPDATE logs SET is_canceled = 0 WHERE id = {memo_id}"""
            self.cur.execute(inquiry)
            self.con.commit()



        _translate = QtCore.QCoreApplication.translate
        self.sender().clicked.disconnect()
        self.sender().clicked.connect(self.cancel_log)
        self.sender().setText(_translate("MainWindow", "Отмениить"))
        self.sender().setStyleSheet("background-color: #FE9895")



    def open_main_menu(self):
        self.close()  # закрывает это окно
        self.main_menu.show()
