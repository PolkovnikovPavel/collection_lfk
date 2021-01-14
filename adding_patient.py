import os, sqlite3, datetime
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QInputDialog
from history import create_history

from data.design.form_adding_patient import Ui_MainWindow as Ui_FormAddingPatient


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


class AddingMenu(QMainWindow, Ui_FormAddingPatient):
    def __init__(self, main_menu, ac_name, db_name):
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()

        super().__init__()
        self.main_menu = main_menu
        self.ac_name = ac_name
        self.db_name = db_name
        self.setupUi(self)

        self.save_button.clicked.connect(self.save_patient)
        self.exit_button.clicked.connect(self.open_main_menu)

        self.all_diagnosis = []
        inquiry = f"""SELECT DISTINCT name FROM diagnoses"""
        diagnoses = self.cur.execute(inquiry).fetchall()
        for diagnose in diagnoses[::-1]:
            self.all_diagnosis.append(diagnose[0])
            self.text_diagnos.addItem(diagnose[0])

        inquiry = f"""SELECT DISTINCT name FROM categories
                            WHERE is_deleted = 0"""
        categories = self.cur.execute(inquiry).fetchall()
        for categorie in categories:
            self.text_category.addItem(categorie[0])

        inquiry = f"""SELECT DISTINCT name FROM departments
                            WHERE is_deleted = 0"""
        departments = self.cur.execute(inquiry).fetchall()
        for department in departments:
            self.text_department.addItem(department[0])

        inquiry = f"""SELECT DISTINCT my_story_number, date_of_operation FROM patients"""
        old_nums = self.cur.execute(inquiry).fetchall()
        old_nums = filter(lambda x: x[1].split('.')[2] == str(datetime.datetime.now().year), old_nums)
        old_nums = list(map(lambda x: x[0], old_nums))
        if len(old_nums) != 0:
            new_num = max(old_nums) + 1
        else:
            new_num = 1
        self.story_number_my.setValue(new_num)

        inquiry = f"""SELECT DISTINCT story_number, date_of_operation FROM patients"""
        old_nums = self.cur.execute(inquiry).fetchall()
        old_nums = filter(lambda x: x[1].split('.')[2] == str(datetime.datetime.now().year), old_nums)
        old_nums = list(map(lambda x: x[0], old_nums))
        if len(old_nums) != 0:
            new_num = max(old_nums) + 1
        else:
            new_num = 1
        self.story_number.setValue(new_num)



    def save_patient(self):
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


        inquiry = f"""INSERT INTO patients (full_name, date_of_birth, 
story_number, category, is_discharge, diagnosis, department, memo, date_of_operation, my_story_number) 
                                    VALUES ('{self.text_full_name.text()}', 
                                    '{date_of_birth}', {story_number}, 
                                    {category}, 0, '{diagnosis}', {department}, 
                                    '{memo}', '{date_of_operation}', {story_number_my})"""
        self.cur.execute(inquiry).fetchall()
        self.con.commit()

        if diagnosis not in self.all_diagnosis:
            inquiry = f"""INSERT INTO diagnoses (name) VALUES ('{diagnosis}')"""
            self.cur.execute(inquiry).fetchall()
            self.con.commit()


        inquiry = f"""SELECT DISTINCT id FROM patients"""
        patient_id = self.cur.execute(inquiry).fetchall()[-1][0]
        create_history(self, f'add_patient;{patient_id}')

        self.close()

    def open_main_menu(self):
        self.close()  # закрывает это окно
        self.main_menu.show()

