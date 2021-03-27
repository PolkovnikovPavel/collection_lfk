import os, sqlite3
from PyQt5.QtWidgets import QMainWindow, QFileDialog

from data.design.form_main_menu import Ui_MainWindow as Ui_FormMainMenu
from admin_menu import AdminMenu
from adding_patient import AddingMenu
from discharge_of_patients import DischargeMenu
from adding_procedure import AddingProcedures
from viewing_old_patients import ViewingProcedures
from description_menu import DescriptionMenu
from history import HistoryMenu
from report_1 import ReportMenu1
from report_2 import ReportMenu2
from report_3 import ReportMenu3
from report_4 import ReportMenu4
from report_5 import ReportMenu5


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


class MainMenu(QMainWindow, Ui_FormMainMenu):
    def __init__(self, login_in_system, ac_name, db_name):
        super().__init__()
        self.login_in_system = login_in_system
        self.ac_name = ac_name
        self.db_name = db_name
        self.setupUi(self)
        self.exit_button.clicked.connect(self.open_login)
        self.admin_button.clicked.connect(self.open_admin_menu)
        self.add_patient_button.clicked.connect(self.open_adding_menu)
        self.button_viewing_procedure.clicked.connect(self.open_viewing_procedure)
        self.delete_patient.clicked.connect(self.open_discharge_menu)
        self.history_button.clicked.connect(self.open_history)
        self.description_button.clicked.connect(self.open_description)
        self.report_1.clicked.connect(self.open_report_1)
        self.report_2.clicked.connect(self.open_report_2)
        self.report_3.clicked.connect(self.open_report_3)
        self.report_4.clicked.connect(self.open_report_4)
        self.report_5.clicked.connect(self.create_report_5)
        self.button_add_procedure.clicked.connect(self.open_adding_procedure)
        self.name.setText(self.ac_name)
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()

        inquiry = f"""SELECT DISTINCT is_admin FROM accounts
                                    WHERE name = '{ac_name}'"""
        is_admin = self.cur.execute(inquiry).fetchone()[0]
        if not is_admin:
            self.admin_button.hide()

    def open_admin_menu(self):
        self.admin_window = AdminMenu(self, self.ac_name, self.db_name)
        #self.close()
        self.admin_window.show()

    def open_adding_menu(self):
        self.adding_window = AddingMenu(self, self.ac_name, self.db_name)
        #self.close()
        self.adding_window.show()

    def open_discharge_menu(self):
        self.dischar_window = DischargeMenu(self, self.ac_name, self.db_name)
        #self.close()
        self.dischar_window.show()

    def open_adding_procedure(self):
        self.procedure_window = AddingProcedures(self, self.ac_name, self.db_name)
        # self.close()
        self.procedure_window.show()

    def open_viewing_procedure(self):
        self.procedure_window = ViewingProcedures(self, self.ac_name, self.db_name)
        # self.close()
        self.procedure_window.show()

    def open_history(self):
        self.history_window = HistoryMenu(self, self.ac_name, self.db_name)
        # self.close()
        self.history_window.show()

    def open_description(self):
        self.description_window = DescriptionMenu(self, self.ac_name, self.db_name)
        # self.close()
        self.description_window.show()

    def open_report_1(self):
        self.report_window = ReportMenu1(self, self.ac_name, self.db_name)
        # self.close()
        self.report_window.show()

    def open_report_2(self):
        self.report_window = ReportMenu2(self, self.ac_name, self.db_name)
        # self.close()
        self.report_window.show()

    def open_report_3(self):
        self.report_window = ReportMenu3(self, self.ac_name, self.db_name)
        # self.close()
        self.report_window.show()

    def open_report_4(self):
        self.report_window = ReportMenu4(self, self.ac_name, self.db_name)
        # self.close()
        self.report_window.show()

    def create_report_5(self):
        self.report_window = ReportMenu5(self, self.ac_name, self.db_name)
        # self.close()
        self.report_window.show()

    def open_login(self):
        self.close()  # закрывает это окно
        self.login_in_system.show()

