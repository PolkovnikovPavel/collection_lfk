import os, sqlite3, datetime
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QInputDialog
from PyQt5 import QtCore, QtGui, QtWidgets

from data.design.form_discharge_of_patients import Ui_MainWindow as Ui_FormDischarge


def get_date_calendar(calendar):
    # возращает выбраную дату в отформатированном виде(дд.мм.гггг)
    date = calendar.selectedDate()
    date = f'{date.day()}.{date.month()}.{date.year()}'
    if len(date.split('.')[0]) == 1:
        # проверка на то, что день записан одним символом
        date = f'0{date}'
    if len(date.split('.')[1]) == 1:
        # проверка на то, что месяц записан одним символом
        date = f'{date.split(".")[0]}.0{".".join(date.split(".")[1:])}'
    return date


class DischargeMenu(QMainWindow, Ui_FormDischarge):
    def __init__(self, main_menu, ac_name, db_name):
        super().__init__()
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()
        self.main_menu = main_menu
        self.ac_name = ac_name
        self.setupUi(self)
        self.button_discharge.clicked.connect(self.discharge_patient)
        self.cancel_button.clicked.connect(self.open_main_menu)
        self.search.textChanged.connect(self.valueChanged)
        self.search.setFocus()

        self.all_patients = []
        inquiry = f"""SELECT DISTINCT full_name, date_of_birth, story_number, id, my_story_number
                                                    FROM patients
                                            WHERE is_discharge = 0"""
        all_patients = self.cur.execute(inquiry).fetchall()
        self.all_patients = []
        for patient in all_patients:
            text = f'{patient[0]} -{patient[4]}- ({patient[2]}) {patient[1]}'
            self.name_patient.addItem(text)
            self.all_patients.append((text, patient[3]))

    def discharge_patient(self):
        self.patient = self.name_patient.currentText()
        date_of_discharge = get_date_calendar(self.choice_date)
        if self.patient not in map(lambda x: x[0], self.all_patients):
            print('no')
            return

        patient = list(filter(lambda x: x[0] == self.patient, self.all_patients))[0]

        inquiry = f"""UPDATE patients SET is_discharge = 1, date_of_discharge = '{date_of_discharge}'
                            WHERE id = {patient[1]}"""
        self.cur.execute(inquiry)
        self.con.commit()

        inquiry = f"""SELECT DISTINCT id FROM accounts
                               WHERE name = '{self.ac_name}'"""
        user_id = self.cur.execute(inquiry).fetchall()[0]

        now = datetime.datetime.now()
        time = f"{now.day}.{now.month}.{now.year}  {now.hour}:{now.minute}"

        inquiry = f"""INSERT INTO logs (user_id, description, is_cancel_button, date) 
        VALUES ({user_id[0]}, 'discharge;{patient[1]}', 1, '{time}')"""
        self.cur.execute(inquiry).fetchall()
        self.con.commit()


        self.close()


    def valueChanged(self):
        text = self.search.text()
        self.name_patient.clear()
        for patient in self.all_patients:
            if text.lower() in patient[0][:-10].lower():
                self.name_patient.addItem(patient[0])

    def open_main_menu(self):
        self.close()  # закрывает это окно
        self.main_menu.show()
