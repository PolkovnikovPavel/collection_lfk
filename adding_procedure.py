import os, sqlite3
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QHBoxLayout
from PyQt5 import QtCore, QtGui, QtWidgets
#from PyQt5 import AlignHCenter

from data.design.form_adding_procedures import Ui_MainWindow as Ui_FormAddingProcedures
from memo import MemoMenu


class MyPushButton(QtWidgets.QPushButton):
    def set_args(self, args):
        self.args = args


class MyComboBox(QtWidgets.QComboBox):
    def set_args(self, args):
        self.args = args


def create_places_combobox(lesson_id, cur, all_places, seve_chenging_place):
    places = MyComboBox()
    places.activated.connect(seve_chenging_place)
    places.set_args(lesson_id)

    inquiry = f"""SELECT DISTINCT id_plase FROM lessons
                                            WHERE id = {lesson_id}"""
    id_plase = cur.execute(inquiry).fetchone()


    if id_plase[0] != 0:
        inquiry = f"""SELECT DISTINCT name FROM places
                                WHERE id = {id_plase[0]}"""
        rez = cur.execute(inquiry).fetchone()
        places.addItems([str(rez[0])])
    else:
        places.addItems(['------'])
    places.addItems(all_places)
    return places


def create_doctors_combobox(lesson_id, cur, all_doctors, seve_chenging_doctor):
    doctors = MyComboBox()
    doctors.activated.connect(seve_chenging_doctor)
    doctors.set_args(lesson_id)

    inquiry = f"""SELECT DISTINCT id_doctor FROM lessons
                                            WHERE id = {lesson_id}"""
    id_doctor = cur.execute(inquiry).fetchone()


    if id_doctor[0] != 0:
        inquiry = f"""SELECT DISTINCT short_name FROM accounts
                                WHERE id = {id_doctor[0]}"""
        rez = cur.execute(inquiry).fetchone()
        doctors.addItems([str(rez[0])])
    else:
        doctors.addItems(['------'])
    doctors.addItems(all_doctors)
    return doctors


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


class AddingProcedures(QMainWindow, Ui_FormAddingProcedures):
    def __init__(self, main_menu, ac_name, db_name):
        super().__init__()
        self.ac_name = ac_name
        self.db_name = db_name
        self.choice_record_id = 0
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()
        self.main_menu = main_menu
        self.ac_name = ac_name
        self.setupUi(self)
        self.search.textChanged.connect(self.valueChanged)
        self.radio_1_1.toggled.connect(self.evaluation_selection)
        self.radio_1_2.toggled.connect(self.evaluation_selection)
        self.radio_1_3.toggled.connect(self.evaluation_selection)
        self.radio_1_4.toggled.connect(self.evaluation_selection)
        self.radio_1_5.toggled.connect(self.evaluation_selection)
        self.radio_2_1.toggled.connect(self.evaluation_selection)
        self.radio_2_2.toggled.connect(self.evaluation_selection)
        self.radio_2_3.toggled.connect(self.evaluation_selection)
        self.radio_2_4.toggled.connect(self.evaluation_selection)
        self.radio_2_5.toggled.connect(self.evaluation_selection)
        self.radio_3_1.toggled.connect(self.evaluation_selection)
        self.radio_3_2.toggled.connect(self.evaluation_selection)
        self.radio_3_3.toggled.connect(self.evaluation_selection)
        self.radio_3_4.toggled.connect(self.evaluation_selection)
        self.radio_3_5.toggled.connect(self.evaluation_selection)
        self.evaluation_1 = 5
        self.evaluation_2 = 5
        self.evaluation_3 = 5
        self.search.setFocus()
        self.exit_button.clicked.connect(self.open_main_menu)
        self.description.clicked.connect(self.open_memo)
        self.add_new_day_button.clicked.connect(self.add_new_day)
        self.name_patient.activated.connect(self.create_tabl)
        self.main_table.cellPressed[int, int].connect(self.clicked_on_table)
        self.main_table.setColumnCount(11)
        self.main_table.setHorizontalHeaderLabels([' ', ' ', 'дата', 'оценка',
                            'кол.\nупр.', 'место\n№1', 'врач\n№1',
                            'место\n№2', 'врач\n№2', 'место\n№3', 'врач\n№3'])



        inquiry = f"""SELECT DISTINCT full_name, date_of_birth, story_number, id, my_story_number
                                            FROM patients
                                    WHERE is_discharge = 0 and is_deleted = 0"""
        all_patients = self.cur.execute(inquiry).fetchall()
        all_patients.sort(key=lambda x: str(x[0]))
        self.all_patients = []
        for patient in all_patients:
            text = f'{patient[0]} -{patient[4]}- ({patient[2]}) {patient[1]}'
            self.name_patient.addItem(text)
            self.all_patients.append((text, patient[3]))

        self.create_tabl()


    def add_new_day(self):
        patient_id = -1
        for text, id in self.all_patients:
            if text == self.name_patient.currentText():
                patient_id = id
        if patient_id == -1:
            return
        date = get_date_calendar(self.choice_date)


        inquiry = f"""INSERT INTO lessons (id_plase, id_doctor, is_deleted) 
                        VALUES (0, 0, 0)"""
        self.cur.execute(inquiry).fetchall()
        self.con.commit()
        inquiry = f"""INSERT INTO lessons (id_plase, id_doctor, is_deleted) 
                                VALUES (0, 0, 0)"""
        self.cur.execute(inquiry).fetchall()
        self.con.commit()
        inquiry = f"""INSERT INTO lessons (id_plase, id_doctor, is_deleted) 
                                VALUES (0, 0, 0)"""
        self.cur.execute(inquiry).fetchall()
        self.con.commit()


        inquiry = f"""SELECT DISTINCT id FROM lessons"""
        all_lessons = self.cur.execute(inquiry).fetchall()[-3:]
        all_lessons = list(map(lambda x: x[0], all_lessons))


        inquiry = f"""INSERT INTO records (patient_id, date, 
                grade_1, grade_2, grade_3, number_of_exercises, lesson_id_1, lesson_id_2, lesson_id_3) 
VALUES ({patient_id}, '{date}', {self.evaluation_1}, {self.evaluation_2}, {self.evaluation_3}, 
        {self.number_of_exercises.value()}, {all_lessons[0]}, {all_lessons[1]}, {all_lessons[2]})"""
        self.cur.execute(inquiry).fetchall()
        self.con.commit()

        self.create_tabl()

    def create_tabl(self):
        font = QtGui.QFont()
        font.setPointSize(15)
        _translate = QtCore.QCoreApplication.translate

        patient_id = -1
        for text, id in self.all_patients:
            if text == self.name_patient.currentText():
                patient_id = id
        if patient_id == -1:
            self.main_table.setRowCount(0)
            return
        inquiry = f"""SELECT DISTINCT id, date, number_of_exercises, grade_1, 
                    grade_2, grade_3, is_deleted, lesson_id_1, lesson_id_2, lesson_id_3
                                                            FROM records
                                                    WHERE patient_id = {patient_id}"""
        all_records = self.cur.execute(inquiry).fetchall()
        all_records = all_records[::-1]

        self.main_table.setRowCount(len(all_records))
        self.main_table.setColumnWidth(0, 10)
        self.main_table.setColumnWidth(1, 70)
        self.main_table.setColumnWidth(2, 140)
        self.main_table.setColumnWidth(3, 100)
        self.main_table.setColumnWidth(4, 50)

        self.main_table.setColumnWidth(5, 85)
        self.main_table.setColumnWidth(6, 85)
        self.main_table.setColumnWidth(7, 85)
        self.main_table.setColumnWidth(8, 85)
        self.main_table.setColumnWidth(9, 85)
        self.main_table.setColumnWidth(10, 85)

        inquiry = f"""SELECT DISTINCT name FROM places WHERE is_deleted = 0"""
        all_places = self.cur.execute(inquiry).fetchall()
        all_places = list(map(lambda x: str(x[0]), all_places))
        all_places.append('------')

        inquiry = f"""SELECT DISTINCT short_name FROM accounts WHERE is_deleted = 0"""
        all_doctors = self.cur.execute(inquiry).fetchall()
        all_doctors = list(map(lambda x: str(x[0]), all_doctors))
        all_doctors.append('------')

        i = -1
        for record in all_records:
            i += 1
            button_1 = MyPushButton(self.centralwidget)
            button_1.setFont(font)
            button_1.set_args(record[0])
            if record[6]:
                button_1.setText(_translate("MainWindow", "Вост"))
                button_1.clicked.connect(self.restore_record)
                button_1.setStyleSheet("background-color: #FEC2A0")
            else:
                button_1.setText(_translate("MainWindow", "Удл"))
                button_1.clicked.connect(self.del_record)
                button_1.setStyleSheet("background-color: #FE9895")

            button_2 = MyPushButton(self.centralwidget)
            button_2.setFont(font)
            button_2.set_args(record[0])
            button_2.setText(_translate("MainWindow", "Измен"))
            button_2.clicked.connect(self.save_record)
            button_2.setStyleSheet("background-color: #FFFAA0")



            date = QtWidgets.QLabel(record[1])
            date.setFont(font)
            eval_1 = self.get_evaluation(record[3])
            eval_2 = self.get_evaluation(record[4])
            eval_3 = self.get_evaluation(record[5])
            font_t = QtGui.QFont()
            font_t.setPointSize(1)
            eval_tabl = QtWidgets.QTableWidget()
            eval_tabl.setFont(font_t)
            eval_tabl.setRowCount(1)
            eval_tabl.setColumnCount(3)
            eval_tabl.setColumnWidth(0, 27)
            eval_tabl.setColumnWidth(1, 27)
            eval_tabl.setColumnWidth(2, 27)
            eval_tabl.setHorizontalHeaderLabels(['', '', ''])
            eval_tabl.setCellWidget(0, 0, eval_1)
            eval_tabl.setCellWidget(0, 1, eval_2)
            eval_tabl.setCellWidget(0, 2, eval_3)

            number_of_exercises = QtWidgets.QLabel(str(record[2]))
            number_of_exercises.setFont(font)


            places_1 = create_places_combobox(record[7],
                                self.cur, all_places, self.seve_chenging_place)
            places_2 = create_places_combobox(record[8],
                                self.cur, all_places, self.seve_chenging_place)
            places_3 = create_places_combobox(record[9],
                                self.cur, all_places, self.seve_chenging_place)

            doctor_1 = create_doctors_combobox(record[7],
                                self.cur, all_doctors, self.seve_chenging_doctor)
            doctor_2 = create_doctors_combobox(record[8],
                                self.cur, all_doctors, self.seve_chenging_doctor)
            doctor_3 = create_doctors_combobox(record[9],
                                self.cur, all_doctors, self.seve_chenging_doctor)


            self.main_table.setCellWidget(i, 0, button_1)
            self.main_table.setCellWidget(i, 1, button_2)
            self.main_table.setCellWidget(i, 2, date)
            self.main_table.setCellWidget(i, 3, eval_tabl)
            self.main_table.setCellWidget(i, 4, number_of_exercises)

            self.main_table.setCellWidget(i, 5, places_1)
            self.main_table.setCellWidget(i, 7, places_2)
            self.main_table.setCellWidget(i, 9, places_3)
            self.main_table.setCellWidget(i, 6, doctor_1)
            self.main_table.setCellWidget(i, 8, doctor_2)
            self.main_table.setCellWidget(i, 10, doctor_3)

        inquiry = f"""SELECT DISTINCT memo FROM patients WHERE id = {patient_id}"""
        memo_of_patient = self.cur.execute(inquiry).fetchone()
        description = memo_of_patient[0].split()
        rez_description = ''
        for word in description:
            if len(rez_description + word) > 42:
                if len(word) > 3:
                    rez_description += word[:3] + '...'
                else:
                    rez_description += word + '...'
                break
            else:
                rez_description += word + ' '
        rez_description += '\n(нажмите, чтоб посмотреть полностью)'

        self.description.setText(rez_description)



    def evaluation_selection(self):
        grin_radio = [(self.radio_1_1, 1),
                      (self.radio_2_1, 2),
                      (self.radio_3_1, 3)]
        yellow_radio = [(self.radio_1_2, 1),
                      (self.radio_2_2, 2),
                      (self.radio_3_2, 3)]
        red_radio = [(self.radio_1_3, 1),
                      (self.radio_2_3, 2),
                      (self.radio_3_3, 3)]
        blue_radio = [(self.radio_1_4, 1),
                      (self.radio_2_4, 2),
                      (self.radio_3_4, 3)]
        white_radio = [(self.radio_1_5, 1),
                      (self.radio_2_5, 2),
                      (self.radio_3_5, 3)]

        for radio, evaluation in grin_radio:
            if radio.isChecked():
                self.set_evaluation(evaluation, 1)
                radio.setStyleSheet('background: #0CDC00')
            else:
                radio.setStyleSheet('background: #B5DCAE')
        for radio, evaluation in yellow_radio:
            if radio.isChecked():
                self.set_evaluation(evaluation, 2)
                radio.setStyleSheet('background: #FFD400')
            else:
                radio.setStyleSheet('background: #E9E8BA')
        for radio, evaluation in red_radio:
            if radio.isChecked():
                self.set_evaluation(evaluation, 3)
                radio.setStyleSheet('background: #F55534')
            else:
                radio.setStyleSheet('background: #F5B6A7')
        for radio, evaluation in blue_radio:
            if radio.isChecked():
                self.set_evaluation(evaluation, 4)
                radio.setStyleSheet('background: #3C1ED7; color: white')
            else:
                radio.setStyleSheet('background: #C2C1D7; color: black')
        for radio, evaluation in white_radio:
            if radio.isChecked():
                self.set_evaluation(evaluation, 5)
                radio.setStyleSheet('background: #616161; color: white')
            else:
                radio.setStyleSheet('')

    def set_evaluation(self, evaluation, num):
        if evaluation == 1:
            self.evaluation_1 = num
        if evaluation == 2:
            self.evaluation_2 = num
        if evaluation == 3:
            self.evaluation_3 = num

    def set_choice_evaluation(self, evaluation, num):
        if evaluation == 1:
            self.evaluation_1 = num
            if num == 1:
                self.radio_1_1.setChecked(True)
            elif num == 2:
                self.radio_1_2.setChecked(True)
            elif num == 3:
                self.radio_1_3.setChecked(True)
            elif num == 4:
                self.radio_1_4.setChecked(True)
            else:
                self.radio_1_5.setChecked(True)
        if evaluation == 2:
            self.evaluation_2 = num
            if num == 1:
                self.radio_2_1.setChecked(True)
            elif num == 2:
                self.radio_2_2.setChecked(True)
            elif num == 3:
                self.radio_2_3.setChecked(True)
            elif num == 4:
                self.radio_2_4.setChecked(True)
            else:
                self.radio_2_5.setChecked(True)
        if evaluation == 3:
            self.evaluation_3 = num
            if num == 1:
                self.radio_3_1.setChecked(True)
            elif num == 2:
                self.radio_3_2.setChecked(True)
            elif num == 3:
                self.radio_3_3.setChecked(True)
            elif num == 4:
                self.radio_3_4.setChecked(True)
            else:
                self.radio_3_5.setChecked(True)

    def get_evaluation(self, evaluation):
        eval = QtWidgets.QLabel('')
        if evaluation == 1:
            eval.setStyleSheet("background-color: #0CDC00")
        elif evaluation == 2:
            eval.setStyleSheet("background-color: #FFD400")
        elif evaluation == 3:
            eval.setStyleSheet("background-color: #F55534")
        elif evaluation == 4:
            eval.setStyleSheet("background-color: #3C1ED7")
        else:
            eval.setStyleSheet("background-color: #616161")
        return eval

    def seve_chenging_place(self):
        procedure_id = self.sender().args
        place = self.sender().currentText()
        if place == '------':
            place_id = 0
        else:
            inquiry = f"""SELECT DISTINCT id FROM places
                                            WHERE name = '{place}'"""
            place_id = self.cur.execute(inquiry).fetchone()[0]

        inquiry = f"""UPDATE lessons
                                    SET id_plase = {place_id}
                                        WHERE id = {procedure_id}"""

        self.cur.execute(inquiry)
        self.con.commit()
        self.create_tabl()

    def seve_chenging_doctor(self):
        procedure_id = self.sender().args
        doctor = self.sender().currentText()
        if doctor == '------':
            doctor_id = 0
        else:
            inquiry = f"""SELECT DISTINCT id FROM accounts
                                        WHERE short_name = '{doctor}'"""
            doctor_id = self.cur.execute(inquiry).fetchone()[0]

        inquiry = f"""UPDATE lessons
                            SET id_doctor = {doctor_id}
                                    WHERE id = {procedure_id}"""

        self.cur.execute(inquiry)
        self.con.commit()
        self.create_tabl()

    def del_record(self):
        record_id = self.sender().args
        inquiry = f"""UPDATE records
                        SET is_deleted = 1
                                    WHERE id = {record_id}"""

        self.cur.execute(inquiry)
        self.con.commit()

        self.sender().setText("Вост")
        self.sender().clicked.disconnect()
        self.sender().clicked.connect(self.restore_record)
        self.sender().setStyleSheet("background-color: #FEC2A0")

    def restore_record(self):
        record_id = self.sender().args
        inquiry = f"""UPDATE records
                        SET is_deleted = 0
                                    WHERE id = {record_id}"""

        self.cur.execute(inquiry)
        self.con.commit()
        self.sender().setText("Удл")
        self.sender().clicked.disconnect()
        self.sender().clicked.connect(self.del_record)
        self.sender().setStyleSheet("background-color: #FE9895")

    def save_record(self):
        record_id = self.sender().args

        if self.choice_record_id != record_id:
            result = QtWidgets.QMessageBox.question(self, "Вопрос",
                        "Точно изменить?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                    QtWidgets.QMessageBox.No)
            if result != QtWidgets.QMessageBox.Yes:
                return


        date = get_date_calendar(self.choice_date)
        inquiry = f"""UPDATE records
                        SET number_of_exercises = {self.number_of_exercises.value()}, 
                    grade_1 = {self.evaluation_1}, grade_2 = {self.evaluation_2}, 
                    grade_3 = {self.evaluation_3}, date = '{date}'
                                WHERE id = {record_id}"""

        self.cur.execute(inquiry)
        self.con.commit()
        self.create_tabl()

    def clicked_on_table(self, r, c):
        call = self.main_table.cellWidget(r, 1)
        record_id = call.args
        self.choice_record_id = record_id
        inquiry = f"""SELECT DISTINCT grade_1, grade_2, grade_3, date, number_of_exercises FROM records 
                    WHERE id = {record_id}"""
        record = self.cur.execute(inquiry).fetchone()

        self.number_of_exercises.setValue(record[4])

        date = record[3].split('.')
        self.choice_date.setSelectedDate(QtCore.QDate(int(date[2]), int(date[1]), int(date[0])))

        self.set_choice_evaluation(1, record[0])
        self.set_choice_evaluation(2, record[1])
        self.set_choice_evaluation(3, record[2])


    def valueChanged(self):
        text = self.search.text()
        self.name_patient.clear()
        for patient in self.all_patients:
            if text.lower() in patient[0][:-10].lower():
                self.name_patient.addItem(patient[0])
        self.create_tabl()

    def open_main_menu(self):
        self.close()  # закрывает это окно
        self.main_menu.show()

    def open_memo(self):
        id_patient = -1
        for patient in self.all_patients:
            if patient[0] == self.name_patient.currentText():
                id_patient = patient[1]
        if id_patient == -1:
            return
        self.memo_window = MemoMenu(self, self.ac_name, self.db_name, id_patient)
        self.memo_window.show()
