import os, sqlite3, openpyxl
import xlwt
from openpyxl.styles import Font, Alignment
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QInputDialog
from PyQt5 import QtCore, QtGui, QtWidgets

from data.design.report_2 import Ui_MainWindow as Ui_Report2


def set_cell(sheet, x, y, value, style, alignment=1):
    cell = sheet._get_cell(x, y)
    cell.value = value
    cell.font = style
    if alignment == 1:
        cell.alignment = Alignment(horizontal='left')
    elif alignment == 2:
        cell.alignment = Alignment(horizontal='center')
    elif alignment == 3:
        cell.alignment = Alignment(horizontal='right')


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


def get_num_from_date(date):
    d, m, y = date.split('.')
    return int(m) * 32 + int(y) * 385 + int(d)

all_month = {'01': 'Январь', '02': 'Февраль', '03': 'Март', '04': 'Апрель',
             '05': 'Май', '06': 'Июнь', '07': 'Июль', '08': 'Август',
             '09': 'Сентябрь', '10': 'Октябрь', '11': 'Ноябрь', '12': 'Декабрь'}


class ReportMenu2(QMainWindow, Ui_Report2):
    def __init__(self, main_menu, ac_name, db_name):
        super().__init__()
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()
        self.main_menu = main_menu
        self.ac_name = ac_name
        self.setupUi(self)
        self.button.clicked.connect(self.create_report)
        self.name_month.activated.connect(self.select_month)

        inquiry = f"""SELECT DISTINCT date FROM records
                                            WHERE is_deleted = 0"""
        all_all_dates = self.cur.execute(inquiry).fetchall()
        self.all_dates = []
        for date in all_all_dates:
            date = '.'.join(date[0].split('.')[1::])
            num_date = date.split('.')
            date = all_month[date.split('.')[0]] + '(' + date.split('.')[0] + ') ' + date.split('.')[1]
            if (date, num_date) not in self.all_dates:
                self.all_dates.append((date, num_date))

        self.all_dates.sort(key=lambda x: x[1][0] + x[1][1] * 13, reverse=True)

        self.selected_month = self.all_dates[0][1]
        for month in self.all_dates:
            self.name_month.addItem(month[0])


    def select_month(self):
        for month in self.all_dates:
            if self.name_month.currentText() == month[0]:
                self.selected_month = month[1]


    def create_report(self):
        file_name = QFileDialog.getSaveFileName(self, 'Путь, где сохранить отчёт', filter='*.xlsx')[0]
        if not file_name:
            return

        try:
            book = openpyxl.load_workbook(file_name)
            for sheet_name in book.sheetnames:
                if sheet_name == f"отчёт за {self.name_month.currentText()}":
                    sheet = book.get_sheet_by_name(sheet_name)
                    book.remove_sheet(sheet)
            sheet = book.create_sheet()
        except Exception:
            book = openpyxl.Workbook()
            sheet = book.active

        sheet.title = f"отчёт за {self.name_month.currentText()}"

        bold_big_style = Font(size="14", bold=True)
        bold_style = Font(size="11", bold=True)
        style = Font(size="11")
        pale_style = Font(size="11", color='00777777')

        # The data
        set_cell(sheet, 1, 1, 'Отчет за месяц работы кабинета реабилитации', bold_big_style)
        set_cell(sheet, 1, 8, all_month[self.selected_month[0]] + ' ' + self.selected_month[1] + 'г.', bold_big_style)


        inquiry = f"""SELECT DISTINCT name FROM categories WHERE is_deleted = 0"""
        all_categories = self.cur.execute(inquiry).fetchall()

        inquiry = f"""SELECT DISTINCT name FROM departments WHERE is_deleted = 0"""
        all_departments = self.cur.execute(inquiry).fetchall()

        inquiry = f"""SELECT DISTINCT name FROM places WHERE is_deleted = 0"""
        all_places = self.cur.execute(inquiry).fetchall()

        # ---------------------------------------катигории людей и их отделения
        inquiry = f"""SELECT records.id, patients.id FROM records, patients
                        WHERE records.is_deleted = 0 and date LIKE '___{self.selected_month[0]}_____'
                                        and records.patient_id = patients.id"""
        all_records = self.cur.execute(inquiry).fetchall()

        all_people_in_month = []
        right_id_people = []

        for record in all_records:
            if record[1] not in all_people_in_month:
                all_people_in_month.append(record[1])

        for id_people in all_people_in_month:
            inquiry = f"""SELECT records.id, records.date FROM records
            WHERE records.is_deleted = 0 and records.patient_id = {id_people}"""
            all_records = self.cur.execute(inquiry).fetchall()
            if all(map(lambda x:
                       get_num_from_date(x[1]) > get_num_from_date(f'01.{self.selected_month[0]}.{self.selected_month[1]}'),
                       all_records)):
                right_id_people.append(id_people)

        department_by_people = {}
        for department in all_departments:
            department_by_people[department[0]] = 0
        department_by_people['удал. отделения'] = 0

        category_by_people = {}
        for categorie in all_categories:
            category_by_people[categorie[0]] = 0
        category_by_people['удал. категории'] = 0

        for id_people in right_id_people:
            inquiry = f"""SELECT patients.id, departments.name, categories.name FROM patients, departments, categories
WHERE patients.id = {id_people} and patients.category = categories.id and patients.department = departments.id"""
            department_categori = self.cur.execute(inquiry).fetchone()
            if department_categori[1] not in department_by_people:
                department_by_people['удал. отделения'] += 1
            else:
                department_by_people[department_categori[1]] += 1
            if department_categori[2] not in category_by_people:
                category_by_people['удал. категории'] += 1
            else:
                category_by_people[department_categori[2]] += 1

        set_cell(sheet, 3, 1, 'Всего человек', bold_style)
        set_cell(sheet, 3, 4, len(right_id_people), bold_style)
        if category_by_people['удал. категории'] != 0:
            all_categories.append(['удал. категории'])
        num_str = 3
        for categorie in all_categories:
            num_str += 1
            set_cell(sheet, num_str, 1, categorie[0], style)
            set_cell(sheet, num_str, 4, category_by_people[categorie[0]], style)

        set_cell(sheet, num_str + 2, 1, 'По отделениям', bold_style)
        if department_by_people['удал. отделения'] != 0:
            all_departments.append(['удал. отделения'])
        num_str += 3
        for department in all_departments:
            num_str += 1
            set_cell(sheet, num_str, 1, department[0], style)
            set_cell(sheet, num_str, 4, department_by_people[department[0]], style)
        # ---------------------------------------------------------------------

        # ------------------------------------------------------- По процедурам

        inquiry = f"""SELECT records.id, places.name, accounts.name FROM records, lessons, places, accounts
            WHERE records.date LIKE '___{self.selected_month[0]}_____' and (lessons.id = records.lesson_id_1 or 
                                                                            lessons.id = records.lesson_id_2 or
                                                                            lessons.id = records.lesson_id_3) and
            lessons.id_plase = places.id and lessons.id_doctor = accounts.id and records.is_deleted = 0"""
        all_records = self.cur.execute(inquiry).fetchall()

        records_by_places = {}
        doctors_by_places = {}

        for place in all_places:
            records_by_places[place[0]] = 0
        records_by_places['удал. места'] = 0

        inquiry = f"""SELECT DISTINCT name FROM accounts WHERE is_deleted = 0"""
        all_doctors = self.cur.execute(inquiry).fetchall()
        for doctor in all_doctors:
            doctors_by_places[doctor[0]] = 0
        inquiry = f"""SELECT DISTINCT name FROM accounts WHERE is_deleted = 1"""
        all_doctors_del = self.cur.execute(inquiry).fetchall()
        for doctor in all_doctors_del:
            doctors_by_places[doctor[0]] = 0


        for record in all_records:
            if record[1] not in records_by_places:
                records_by_places['удал. места'] += 1
            else:
                records_by_places[record[1]] += 1
            doctors_by_places[record[2]] += 1





        set_cell(sheet, num_str + 2, 1, 'По процедурам', bold_style)
        set_cell(sheet, num_str + 4, 2, 'Места', bold_style)
        set_cell(sheet, num_str + 5, 1, 'Всего', style)
        set_cell(sheet, num_str + 5, 4, len(all_records), style)
        set_cell(sheet, num_str + 5, 6, 'Всего', style)
        set_cell(sheet, num_str + 5, 11, len(all_records), style)

        set_cell(sheet, num_str + 4, 7, 'Исполнители', bold_style)

        num_str += 5
        if records_by_places['удал. места'] != 0:
            all_places.append(['удал. места'])
        for place in all_places:
            num_str += 1
            set_cell(sheet, num_str, 1, place[0], style)
            set_cell(sheet, num_str, 4, records_by_places[place[0]], style)

        num_str -= len(all_places)
        for doctor in all_doctors:
            num_str += 1
            if doctors_by_places[doctor[0]] != 0:
                set_cell(sheet, num_str, 6, doctor[0], style)
                set_cell(sheet, num_str, 11, doctors_by_places[doctor[0]], style)
        for doctor in all_doctors_del:
            num_str += 1
            if doctors_by_places[doctor[0]] != 0:
                set_cell(sheet, num_str, 6, doctor[0], pale_style)
                set_cell(sheet, num_str, 11, doctors_by_places[doctor[0]], pale_style)



        sheet.sheet_properties.pageSetUpPr.fitToPage = True
        sheet.orientation = 'landscape'
        sheet.set_printer_settings(9, 'landscape')

        try:
            book.save(file_name)
        except PermissionError:
            pass
        self.close()

    def open_main_menu(self):
        self.close()  # закрывает это окно
        self.main_menu.show()
