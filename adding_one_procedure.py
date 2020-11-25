import os, sqlite3
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QInputDialog
from PyQt5 import QtCore, QtGui, QtWidgets

from data.design.form_adding_procedures_one import Ui_MainWindow as Ui_FormAddingProcedureOne


class MyComboBox(QtWidgets.QComboBox):
    def set_args(self, args):
        self.args = args


class AddingProcedureOne(QMainWindow, Ui_FormAddingProcedureOne):
    def __init__(self, main_menu, ac_name, db_name, day_id):
        super().__init__()
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()
        self.day_id = day_id
        self.main_menu = main_menu
        self.ac_name = ac_name
        self.setupUi(self)
        self.exit_button.clicked.connect(self.open_main_menu)
        self.add_new_procedure_button.clicked.connect(self.create_new_procedure)
        self.create_table()

    def create_table(self):
        inquiry = f"""SELECT DISTINCT id_lessons FROM records
                                        WHERE id = {self.day_id}"""
        all_procedures_id = self.cur.execute(inquiry).fetchone()
        if len(str(all_procedures_id[0])) != 0:
            all_procedures_id = list(map(int, str(all_procedures_id[0]).split(';')))
        else:
            return

        self.main_table.setRowCount(len(all_procedures_id))
        self.main_table.setColumnCount(3)
        self.main_table.setColumnWidth(0, 100)
        self.main_table.setColumnWidth(1, 200)
        self.main_table.setColumnWidth(2, 200)
        i = -1
        for lesson_id in all_procedures_id:
            i += 1
            inquiry = f"""SELECT DISTINCT id_plase, id_doctor FROM lessons
                                                    WHERE id = {lesson_id}"""
            id_plase_doctor = self.cur.execute(inquiry).fetchone()

            places = MyComboBox(self.centralwidget)
            places.activated.connect(self.seve_chenging_place)
            places.set_args(lesson_id)

            if id_plase_doctor[0] != 0:
                inquiry = f"""SELECT DISTINCT name FROM places
                                                    WHERE id = {id_plase_doctor[0]}"""
                rez = self.cur.execute(inquiry).fetchone()
                places.addItems([rez[0]])
            else:
                places.addItems(['------'])
            inquiry = f"""SELECT DISTINCT name FROM places"""
            rez = self.cur.execute(inquiry).fetchall()
            rez = list(map(lambda x: x[0], rez))
            places.addItems(rez)
            #________________________________________________________________

            doctors = MyComboBox(self.centralwidget)
            doctors.activated.connect(self.seve_chenging_doctor)
            doctors.set_args(lesson_id)
            if id_plase_doctor[1] != 0:
                inquiry = f"""SELECT DISTINCT name FROM accounts
                                                    WHERE id = {id_plase_doctor[1]}"""
                rez = self.cur.execute(inquiry).fetchone()
                doctors.addItems([rez[0]])
            else:
                doctors.addItems(['------'])
            inquiry = f"""SELECT DISTINCT name FROM accounts"""
            rez = self.cur.execute(inquiry).fetchall()
            rez = list(map(lambda x: x[0], rez))
            doctors.addItems(rez)


            self.main_table.setCellWidget(i, 1, places)
            self.main_table.setCellWidget(i, 2, doctors)


    def create_new_procedure(self):
        inquiry = f"""INSERT INTO lessons (id_plase, id_doctor) 
                                VALUES (0, 0)"""
        self.cur.execute(inquiry).fetchall()
        self.con.commit()

        inquiry = f"""SELECT DISTINCT id_lessons FROM records
                                    WHERE id = {self.day_id}"""
        new_data = self.cur.execute(inquiry).fetchone()[0]
        new_data = str(new_data)

        inquiry = f"""SELECT DISTINCT id FROM lessons"""
        max_id = max(list(map(lambda x: x[0], self.cur.execute(inquiry).fetchall())))

        if len(str(new_data)) == 0:
            new_data = str(max_id)
        else:
            new_data += f';{str(max_id)}'

        inquiry = f"""UPDATE records
                            SET id_lessons = '{new_data}'
                                WHERE id = {self.day_id}"""
        self.cur.execute(inquiry)
        self.con.commit()
        self.create_table()


    def seve_chenging_place(self):
        procedure_id = self.sender().args
        place = self.sender().currentText()
        inquiry = f"""SELECT DISTINCT id FROM places
                                WHERE name = '{place}'"""
        place_id = self.cur.execute(inquiry).fetchone()[0]

        inquiry = f"""UPDATE lessons
                            SET id_plase = {place_id}
                                WHERE id = {procedure_id}"""

        self.cur.execute(inquiry)
        self.con.commit()
        self.create_table()


    def seve_chenging_doctor(self):
        procedure_id = self.sender().args
        doctor = self.sender().currentText()
        inquiry = f"""SELECT DISTINCT id FROM accounts
                                WHERE name = '{doctor}'"""
        doctor_id = self.cur.execute(inquiry).fetchone()[0]

        inquiry = f"""UPDATE lessons
                            SET id_doctor = {doctor_id}
                                WHERE id = {procedure_id}"""

        self.cur.execute(inquiry)
        self.con.commit()
        self.create_table()

    def open_main_menu(self):
        self.close()  # закрывает это окно
        self.main_menu.show()
