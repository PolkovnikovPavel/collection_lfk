import os, sqlite3, openpyxl
from openpyxl.styles import Font, Alignment
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QInputDialog
from PyQt5 import QtCore, QtGui, QtWidgets

from data.design.report_1 import Ui_MainWindow as Ui_Report1

bold_big_style = Font(size="14", bold=True)
bold_style = Font(size="11", bold=True)
style = Font(size="11")


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




def create_report():

    file_name = QFileDialog.getSaveFileName(self, 'Путь, где сохранить отчёт', filter='*.xlsx')[0]
    if not file_name:
        return

    try:
        book = openpyxl.load_workbook(file_name)
        for sheet_name in book.sheetnames:
            if sheet_name == "отчёт за день":
                sheet = book.get_sheet_by_name(sheet_name)
                book.remove_sheet(sheet)
        sheet = book.create_sheet()
    except Exception:
        book = openpyxl.Workbook()
        sheet = book.active

    sheet.title = "отчёт за день"

    set_cell(sheet, 1, 1, 'Сборный отчёт динамики лечения', bold_big_style)


    set_cell(sheet, 2, 1, 'ФИО, год рождения, диагноз', bold_style)
    set_cell(sheet, 2, 2, '№ карты', bold_style)


    sheet.column_dimensions['B'].width = 55
    sheet.column_dimensions['A'].width = 5
    sheet.column_dimensions['C'].width = 12
    sheet.column_dimensions['D'].width = 17
    sheet.column_dimensions['F'].width = 7
    sheet.column_dimensions['H'].width = 7
    sheet.column_dimensions['J'].width = 7
    sheet.column_dimensions['G'].width = 10
    sheet.column_dimensions['I'].width = 10
    sheet.column_dimensions['K'].width = 10
    sheet.column_dimensions['E'].width = 24

    sheet.sheet_properties.pageSetUpPr.fitToPage = True
    sheet.page_setup.fitToHeight = False
    sheet.orientation = 'landscape'
    sheet.set_printer_settings(9, 'landscape')

    try:
        book.save(file_name)
    except PermissionError:
        pass

