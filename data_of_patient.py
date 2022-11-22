import os, sqlite3, datetime
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QInputDialog
from PyQt5 import QtCore
from history import create_history

from data.design.chenge_data_of_patient import Ui_MainWindow as Ui_FormDataPatient


def get_date(date):
    # возращает выбраную дату в отформатированном виде(дд.мм.гггг)
    date = f'{date.day()}.{date.month()}.{date.year()}'
    if len(date.split('.')[0]) == 1:
        # проверка на то, что день записан одним символом
        date = f'0{date}'
    if len(date.split('.')[1]) == 1:
        # проверка на то, что месяц записан одним символом
        date = f'{date.split(".")[0]}.0{".".join(date.split(".")[1:])}'
    return date


class DataPatient(QMainWindow, Ui_FormDataPatient):
    def __init__(self, main_menu, ac_name, db_name, patient_id, mod=0):
        self.mod = mod
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()

        super().__init__()
        self.main_menu = main_menu
        self.ac_name = ac_name
        self.db_name = db_name
        self.selected_patient = patient_id
        self.setupUi(self)

        self.name_patient.activated.connect(self.select_patient)
        self.search.textChanged.connect(self.valueChanged)
        self.save_button.clicked.connect(self.save_patient)
        self.exit_button.clicked.connect(self.open_main_menu)

        self.all_diagnosis = []
        inquiry = f"""SELECT DISTINCT name FROM diagnoses"""
        diagnoses = self.cur.execute(inquiry).fetchall()
        for diagnose in diagnoses[::-1]:
            self.all_diagnosis.append(str(diagnose[0]))
            self.text_diagnos.addItem(str(diagnose[0]))

        inquiry = f"""SELECT DISTINCT full_name, date_of_birth, story_number, id, my_story_number FROM patients
                                            WHERE is_discharge = {self.mod} and is_deleted = 0"""
        all_patients = self.cur.execute(inquiry).fetchall()
        all_patients.sort(key=lambda x: str(x[0]))
        self.all_patients = []
        for patient in all_patients:
            text = f'{" ".join(patient[0].split())} -{patient[4]}- ({patient[2]}) {patient[1]}'
            self.name_patient.addItem(text)
            self.all_patients.append((text, patient[3]))
            if patient[3] == self.selected_patient:
                self.name_patient.setCurrentIndex(all_patients.index(patient))
        if self.selected_patient == -1:
            self.selected_patient = all_patients[0][1]

        inquiry = f"""SELECT DISTINCT name, id FROM categories
                            WHERE is_deleted = 0"""
        categories = self.cur.execute(inquiry).fetchall()
        self.all_categories = []
        for categorie in categories:
            self.all_categories.append((categorie[0], categorie[1]))
            self.text_category.addItem(categorie[0])

        inquiry = f"""SELECT DISTINCT name, id FROM departments
                            WHERE is_deleted = 0"""
        departments = self.cur.execute(inquiry).fetchall()
        self.all_departments = []
        for department in departments:
            self.all_departments.append((department[0], department[1]))
            self.text_department.addItem(department[0])
        self.create_tabl()


    def create_tabl(self):
        if self.selected_patient == -1:
            self.text_full_name.setText('')
            self.choice_date_of_birth.setDate(QtCore.QDate(2000, 1, 1))
            return
        inquiry = f"""SELECT DISTINCT * FROM patients
                                    WHERE id = {self.selected_patient}"""
        data_of_patient = self.cur.execute(inquiry).fetchone()

        self.text_full_name.setText(data_of_patient[1])
        date = data_of_patient[2].split('.')
        self.choice_date_of_birth.setDate(QtCore.QDate(int(date[2]), int(date[1]), int(date[0])))
        self.story_number.setValue(int(data_of_patient[3]))
        self.story_number_my.setValue(int(data_of_patient[11]))
        categorie = list(filter(lambda x: x[1] == data_of_patient[4], self.all_categories))[0]
        self.text_category.setCurrentIndex(self.all_categories.index(categorie))
        department = list(filter(lambda x: x[1] == data_of_patient[7], self.all_departments))[0]
        self.text_department.setCurrentIndex(self.all_departments.index(department))
        self.text_diagnos.setCurrentText(str(data_of_patient[6]))
        self.text_memo.setText(str(data_of_patient[8]))
        date = data_of_patient[10].split('.')
        self.choice_date_of_operation.setSelectedDate(QtCore.QDate(int(date[2]), int(date[1]), int(date[0])))


    def save_patient(self):
        if self.selected_patient == -1 or self.mod != 0:
            return

        date_of_birth = get_date(self.choice_date_of_birth.date())
        date_of_operation = get_date(self.choice_date_of_operation.selectedDate())
        story_number = self.story_number.value()
        story_number_my = self.story_number_my.value()
        diagnosis = self.text_diagnos.currentText()
        memo = self.text_memo.toPlainText()

        category = self.text_category.currentText()
        inquiry = f"""SELECT DISTINCT id FROM categories WHERE name = '{category}'"""
        category = self.cur.execute(inquiry).fetchone()[0]

        department = self.text_department.currentText()
        inquiry = f"""SELECT DISTINCT id FROM departments WHERE name = '{department}'"""
        department = self.cur.execute(inquiry).fetchone()[0]

        inquiry = f"""SELECT DISTINCT * FROM patients
                                WHERE id = {self.selected_patient}"""
        old_data_patient = self.cur.execute(inquiry).fetchone()

        inquiry = f"""UPDATE patients
                SET full_name = '{" ".join(self.text_full_name.text().split())}',
            date_of_birth = '{date_of_birth}', 
            story_number = {story_number},
            category = {category},
            diagnosis = '{diagnosis}',
            department = {department},
            memo = '{memo}',
            date_of_operation = '{date_of_operation}',
            my_story_number = {story_number_my}
                    WHERE id = {self.selected_patient}"""
        self.cur.execute(inquiry).fetchall()
        self.con.commit()

        if diagnosis not in self.all_diagnosis:
            inquiry = f"""INSERT INTO diagnoses (name) VALUES ('{diagnosis}')"""
            self.cur.execute(inquiry).fetchall()
            self.con.commit()

        data = [(old_data_patient[1], self.text_full_name.text()),
                (old_data_patient[2], date_of_birth),
                (old_data_patient[3], story_number),
                (old_data_patient[4], category),
                (old_data_patient[6], diagnosis),
                (old_data_patient[7], department),
                (old_data_patient[8], memo),
                (old_data_patient[10], date_of_operation),
                (old_data_patient[11], story_number_my)]

        create_history(self, f'c_patient;{self.selected_patient};{data[0][0]};{data[0][1]};{data[1][0]};{data[1][1]};{data[2][0]};{data[2][1]};{data[3][0]};{data[3][1]};{data[4][0]};{data[4][1]};{data[5][0]};{data[5][1]};{data[6][0]};{data[6][1]};{data[7][0]};{data[7][1]};{data[8][0]};{data[8][1]};')

        self.close()

    def select_patient(self):
        for text, id in self.all_patients:
            if text == self.name_patient.currentText():
                self.selected_patient = id
                self.create_tabl()
                return


    def valueChanged(self):
        text = self.search.text()
        self.name_patient.clear()
        all_right_id_patient = []
        for patient in self.all_patients:
            if text.lower() in patient[0][:-10].lower():
                self.name_patient.addItem(patient[0])
                all_right_id_patient.append(patient[1])
        if self.selected_patient not in all_right_id_patient:
            if len(all_right_id_patient) > 0:
                self.selected_patient = all_right_id_patient[0]
            else:
                self.selected_patient = -1
        self.create_tabl()

    def open_main_menu(self):
        self.close()  # закрывает это окно
        self.main_menu.show()

