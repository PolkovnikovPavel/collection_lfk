import os, sqlite3, openpyxl
from openpyxl.styles import Font, Alignment
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QInputDialog

from data.design.report_3 import Ui_MainWindow as Ui_Report3


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


class ReportMenu3(QMainWindow, Ui_Report3):
    def __init__(self, main_menu, ac_name, db_name):
        super().__init__()
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()
        self.main_menu = main_menu
        self.ac_name = ac_name
        self.setupUi(self)
        self.setWindowTitle('Отчёт за год')
        self.button.clicked.connect(self.create_report)
        self.name_year.activated.connect(self.select_year)

        inquiry = f"""SELECT DISTINCT date FROM records
                                            WHERE is_deleted = 0"""
        all_all_dates = self.cur.execute(inquiry).fetchall()
        self.all_years = []
        for date in all_all_dates:
            date = int(date[0].split('.')[2])
            if date not in self.all_years:
                self.all_years.append(date)

        self.all_years.sort(reverse=True)

        self.selected_year = self.all_years[0]
        for year in self.all_years:
            self.name_year.addItem(str(year))

    def select_year(self):
        for month in self.all_years:
            if self.name_year.currentText() == str(month):
                self.selected_year = month


    def create_report(self):
        file_name = QFileDialog.getSaveFileName(self, 'Путь, где сохранить отчёт', filter='*.xlsx')[0]
        if not file_name:
            return

        try:
            book = openpyxl.load_workbook(file_name)
            for sheet_name in book.sheetnames:
                if sheet_name == f"отчёт за {self.selected_year} год":
                    sheet = book.get_sheet_by_name(sheet_name)
                    book.remove_sheet(sheet)
            sheet = book.create_sheet()
        except Exception:
            book = openpyxl.Workbook()
            sheet = book.active

        sheet.title = f"отчёт за {self.selected_year} год"

        bold_big_style = Font(size="14", bold=True)
        bold_style = Font(size="11", bold=True)
        style = Font(size="11")
        pale_style = Font(size="11", color='00777777')

        # The data
        set_cell(sheet, 1, 1, 'Отчет за год работы кабинета реабилитации', bold_big_style)
        set_cell(sheet, 1, 8, str(self.selected_year) + 'г.', bold_big_style)


        inquiry = f"""SELECT DISTINCT name FROM categories WHERE is_deleted = 0"""
        all_categories = self.cur.execute(inquiry).fetchall()

        inquiry = f"""SELECT DISTINCT name FROM departments WHERE is_deleted = 0"""
        all_departments = self.cur.execute(inquiry).fetchall()

        inquiry = f"""SELECT DISTINCT name, price FROM places WHERE is_deleted = 0"""
        all_places = self.cur.execute(inquiry).fetchall()

        # ---------------------------------------катигории людей и их отделения
        inquiry = f"""SELECT records.id, patients.id FROM records, patients
                        WHERE records.is_deleted = 0 and date LIKE '%{self.selected_year}'
                                        and records.patient_id = patients.id and patients.is_deleted = 0"""
        all_records = self.cur.execute(inquiry).fetchall()

        all_people_in_year = []
        right_id_people = []

        for record in all_records:
            if record[1] not in all_people_in_year:
                all_people_in_year.append(record[1])

        for id_people in all_people_in_year:
            inquiry = f"""SELECT records.id, records.date FROM records
            WHERE records.is_deleted = 0 and records.patient_id = {id_people}"""
            all_records = self.cur.execute(inquiry).fetchall()
            if all(map(lambda x:
                       int(x[1].split('.')[2]) >= self.selected_year,
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
WHERE patients.id = {id_people} and patients.category = categories.id and patients.department = departments.id and patients.is_deleted = 0"""
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

        inquiry = f"""SELECT records.id, places.name, accounts.name FROM records, lessons, places, accounts, patients
            WHERE records.date LIKE '%{self.selected_year}' and (lessons.id = records.lesson_id_1 or 
                                                                  lessons.id = records.lesson_id_2 or
                                                                  lessons.id = records.lesson_id_3) and
            lessons.id_plase = places.id and lessons.id_doctor = accounts.id and records.is_deleted = 0 and patients.is_deleted = 0 and patients.id = records.patient_id"""
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
        set_cell(sheet, num_str + 4, 1, '        Способ реабилитации', bold_style)
        set_cell(sheet, num_str + 4, 9, 'Исполнители', bold_style)
        set_cell(sheet, num_str + 4, 5, '      еденицы', bold_style)
        set_cell(sheet, num_str + 2, 3, 'всего:', style, alignment=3)
        set_cell(sheet, num_str + 2, 4, len(all_records), style)

        num_str += 4
        sum_price = 0
        if records_by_places['удал. места'] != 0:
            all_places.append(['удал. места'])
        for place in all_places:
            num_str += 1
            set_cell(sheet, num_str, 1, place[0], style)
            set_cell(sheet, num_str, 4, records_by_places[place[0]], style)
            if place[0] != 'удал. места':
                set_cell(sheet, num_str, 5, f'* {place[1]} =', style)
                set_cell(sheet, num_str, 6,
                         place[1] * records_by_places[place[0]], style)
                sum_price += place[1] * records_by_places[place[0]]
        set_cell(sheet, num_str + 1, 5, 'всего:', style)
        set_cell(sheet, num_str + 1, 6, sum_price, style)

        num_str -= len(all_places)
        for doctor in all_doctors:
            if doctors_by_places[doctor[0]] != 0:
                num_str += 1
                set_cell(sheet, num_str, 8, doctor[0], style)
                set_cell(sheet, num_str, 13, doctors_by_places[doctor[0]], style)
        for doctor in all_doctors_del:
            if doctors_by_places[doctor[0]] != 0:
                num_str += 1
                set_cell(sheet, num_str, 8, doctor[0], pale_style)
                set_cell(sheet, num_str, 13, doctors_by_places[doctor[0]], pale_style)

        sheet.column_dimensions['D'].width = 5.5
        sheet.column_dimensions['E'].width = 6

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
