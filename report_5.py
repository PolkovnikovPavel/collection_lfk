import os, sqlite3, openpyxl
from openpyxl.styles import Font, Alignment
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QInputDialog
from PyQt5 import QtCore, QtGui, QtWidgets

from data.design.report_1 import Ui_MainWindow as Ui_Report1

bold_big_style = Font(size="14", bold=True)
bold_style = Font(size="11", bold=True)
style = Font(size="11")
abc = ['', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
       'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


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




def create_report(self):

    file_name = QFileDialog.getSaveFileName(self, 'Путь, где сохранить отчёт', filter='*.xlsx')[0]
    if not file_name:
        return

    try:
        book = openpyxl.load_workbook(file_name)
        for sheet_name in book.sheetnames:
            if sheet_name == "сборный":
                sheet = book.get_sheet_by_name(sheet_name)
                book.remove_sheet(sheet)
        sheet = book.create_sheet()
    except Exception:
        book = openpyxl.Workbook()
        sheet = book.active

    sheet.title = "сборный"

    set_cell(sheet, 1, 1, 'Сборный отчёт динамики лечения', bold_big_style)

    set_cell(sheet, 2, 1, 'ФИО, год рождения, диагноз', bold_style)
    set_cell(sheet, 2, 2, '№ карты', bold_style)
    set_cell(sheet, 2, 3, 'дата с..по..', bold_style)
    set_cell(sheet, 2, 4, 'дней лечения', bold_style)
    set_cell(sheet, 2, 5, 'дней ЛФК', bold_style)
    set_cell(sheet, 2, 6, 'всего процедур', bold_style)
    set_cell(sheet, 2, 7, 'сего ед.', bold_style)

    inquiry = f"""SELECT DISTINCT full_name, diagnosis, date_of_birth, story_number, category, department, my_story_number
                                                        FROM patients
                                                    WHERE is_discharge = 1"""
    all_patients = self.cur.execute(inquiry).fetchall()

    for symbol_1 in abc:
        for symbol_2 in abc[1::]:
            sheet.column_dimensions[symbol_1 + symbol_2].width = 1.09


    sheet.sheet_properties.pageSetUpPr.fitToPage = True
    sheet.page_setup.fitToHeight = False
    sheet.orientation = 'landscape'
    sheet.set_printer_settings(9, 'landscape')

    try:
        book.save(file_name)
    except PermissionError:
        pass

