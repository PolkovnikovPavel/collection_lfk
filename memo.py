import os, sqlite3, openpyxl
from openpyxl.styles import Font, Alignment
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QInputDialog
from history import create_history

from data.design.form_memo import Ui_MainWindow as Ui_memo

bold_big_style = Font(size="14", bold=True)
bold_style = Font(size="11", bold=True)
style = Font(size="11")


class MemoMenu(QMainWindow, Ui_memo):
    def __init__(self, main_menu, ac_name, db_name, id_patient, mod=0):
        super().__init__()
        self.mod = mod
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()
        self.main_menu = main_menu
        self.ac_name = ac_name
        self.id_patient = id_patient
        self.setupUi(self)
        self.exit_button.clicked.connect(self.open_main_menu)
        inquiry = f"""SELECT DISTINCT full_name, memo FROM patients 
                            WHERE id = {id_patient}"""
        patient = self.cur.execute(inquiry).fetchone()
        self.name.setText(patient[0])
        self.text.setText(str(patient[1]))

    def closeEvent(self, event):
        if self.mod == 1:
            return
        new_text = self.text.toPlainText()
        inquiry = f"""SELECT DISTINCT memo FROM patients 
                                    WHERE id = {self.id_patient}"""
        old_text = str(self.cur.execute(inquiry).fetchone()[0])
        if ''.join(old_text.split()) != ''.join(new_text.split()):
            description = f'memo_s;{old_text};{new_text};{self.id_patient}'
            create_history(self, description)

        inquiry = f"""UPDATE patients SET memo = '{new_text}'
                                    WHERE id = {self.id_patient}"""
        self.cur.execute(inquiry)
        self.con.commit()

    def open_main_menu(self):
        self.close()  # закрывает это окно
