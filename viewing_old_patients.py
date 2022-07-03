import os, sqlite3, datetime
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QHBoxLayout
from PyQt5 import QtCore, QtGui, QtWidgets

from data.design.form_adding_procedures import Ui_MainWindow as Ui_FormAddingProcedures
from memo import MemoMenu
from data_of_patient import DataPatient


font = QtGui.QFont()
font.setPointSize(15)


class MyPushButton(QtWidgets.QPushButton):
    def set_args(self, args):
        self.args = args


class MyComboBox(QtWidgets.QComboBox):
    def set_args(self, args):
        self.args = args


def create_places_combobox(lesson_id, cur):
    text = '------'
    inquiry = f"""SELECT DISTINCT id_plase FROM lessons
                                    WHERE id = {lesson_id}"""
    id_plase = cur.execute(inquiry).fetchone()
    if id_plase[0] != 0:
        inquiry = f"""SELECT DISTINCT short_name FROM places
                            WHERE id = {id_plase[0]}"""
        plase = cur.execute(inquiry).fetchone()
        text = str(plase[0])

    place = QtWidgets.QTextBrowser()
    place.setText(text)
    place.setFont(font)

    return place


def create_doctors_combobox(lesson_id, cur):
    text = '------'
    inquiry = f"""SELECT DISTINCT id_doctor FROM lessons
                                            WHERE id = {lesson_id}"""
    id_doctor = cur.execute(inquiry).fetchone()
    if id_doctor[0] != 0:
        inquiry = f"""SELECT DISTINCT short_name FROM accounts
                            WHERE id = {id_doctor[0]}"""
        doctor = cur.execute(inquiry).fetchone()
        text = str(doctor[0])

    doctor = QtWidgets.QTextBrowser()
    doctor.setText(text)
    doctor.setFont(font)
    return doctor


def get_num_from_date(date):
    day, month, year = map(int, date.split('.'))
    return year * 365 + month * 30 + day

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


class ViewingProcedures(QMainWindow, Ui_FormAddingProcedures):
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
        self.old_choice_date = None
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
        self.add_new_day_button.hide()
        self.chenge_data_of_patient.clicked.connect(self.open_menu_data_of_patient)
        self.name_patient.activated.connect(self.create_tabl)
        self.choice_date.clicked['QDate'].connect(self.choiced_date)
        self.main_table.setColumnCount(9)
        self.main_table.setHorizontalHeaderLabels(['дата', 'оценка',
                            'кол.\nупр.', 'процед.\n№1', 'врач\n№1',
                            'процед.\n№2', 'врач\n№2', 'процед.\n№3', 'врач\n№3'])
        self.chenge_data_of_patient.setText('Просмотреть данные')


        inquiry = f"""SELECT DISTINCT full_name, date_of_birth, story_number, id, my_story_number, date_of_discharge
                                            FROM patients
                                    WHERE is_discharge = 1 and is_deleted = 0"""
        all_patients = self.cur.execute(inquiry).fetchall()
        all_patients.sort(key=lambda x: get_num_from_date(x[5]), reverse=True)
        self.all_patients = []
        for patient in all_patients:
            text = f'{patient[0]} -{patient[4]}- ({patient[2]}) {patient[1]}'
            self.name_patient.addItem(text)
            self.all_patients.append((text, patient[3]))
        self.choiced_date()
        self.create_tabl()
        self.label_12.setText(f'Всего человек: {len(self.all_patients)}')


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
                                                    WHERE patient_id = {patient_id} AND is_deleted = 0"""
        all_records = self.cur.execute(inquiry).fetchall()
        all_records = all_records[::-1]

        self.main_table.setRowCount(len(all_records))
        self.main_table.setColumnWidth(0, 140)
        self.main_table.setColumnWidth(1, 100)
        self.main_table.setColumnWidth(2, 50)
        self.main_table.setColumnWidth(3, 85)
        self.main_table.setColumnWidth(4, 85)

        self.main_table.setColumnWidth(5, 85)
        self.main_table.setColumnWidth(6, 85)
        self.main_table.setColumnWidth(7, 85)
        self.main_table.setColumnWidth(8, 85)

        inquiry = f"""SELECT DISTINCT short_name FROM places WHERE is_deleted = 0"""
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


            places_1 = create_places_combobox(record[7], self.cur)
            places_2 = create_places_combobox(record[8], self.cur)
            places_3 = create_places_combobox(record[9], self.cur)

            doctor_1 = create_doctors_combobox(record[7], self.cur)
            doctor_2 = create_doctors_combobox(record[8], self.cur)
            doctor_3 = create_doctors_combobox(record[9], self.cur)


            self.main_table.setCellWidget(i, 0, date)
            self.main_table.setCellWidget(i, 1, eval_tabl)
            self.main_table.setCellWidget(i, 2, number_of_exercises)

            self.main_table.setCellWidget(i, 3, places_1)
            self.main_table.setCellWidget(i, 5, places_2)
            self.main_table.setCellWidget(i, 7, places_3)
            self.main_table.setCellWidget(i, 4, doctor_1)
            self.main_table.setCellWidget(i, 6, doctor_2)
            self.main_table.setCellWidget(i, 8, doctor_3)

        inquiry = f"""SELECT DISTINCT memo, diagnosis, date_of_operation, date_of_discharge FROM patients WHERE id = {patient_id}"""
        memo_of_patient = self.cur.execute(inquiry).fetchone()
        description = memo_of_patient[0]
        rez_description = ' '.join(description.split())[:39]
        if len(' '.join(description.split())) > 39:
            rez_description += '...'
        rez_description += '\n(нажмите, чтоб посмотреть полностью)'
        self.description.setText(rez_description)

        diagnos = memo_of_patient[1]
        date_of_operation = memo_of_patient[2]
        date_of_discharge = memo_of_patient[3]
        self.diagnosis.setText(f'Дата оп. {date_of_operation}, Дата выписки: {date_of_discharge}\n {diagnos}')

        self.resizeEvent(0)

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
        self.memo_window = MemoMenu(self, self.ac_name, self.db_name, id_patient, mod=1)
        self.memo_window.show()

    def open_menu_data_of_patient(self):
        patient_id = -1
        for text, id in self.all_patients:
            if text == self.name_patient.currentText():
                patient_id = id

        self.data_of_patient_window = DataPatient(self, self.ac_name, self.db_name, patient_id, mod=1)
        self.data_of_patient_window.show()

    def choiced_date(self):
        pass

    def resizeEvent(self, event):
        self.main_table.setGeometry(QtCore.QRect(10, 440, self.width() - 20, self.height() - 480))
        if self.width() > 1100:
            width = (self.width() - 580) // 6
            if width > 170:
                width = 170
            self.main_table.setColumnWidth(3, width)
            self.main_table.setColumnWidth(4, width)
            self.main_table.setColumnWidth(5, width)
            self.main_table.setColumnWidth(6, width)
            self.main_table.setColumnWidth(7, width)
            self.main_table.setColumnWidth(8, width)
        else:
            self.main_table.setColumnWidth(3, 85)
            self.main_table.setColumnWidth(4, 85)
            self.main_table.setColumnWidth(5, 85)
            self.main_table.setColumnWidth(6, 85)
            self.main_table.setColumnWidth(7, 85)
            self.main_table.setColumnWidth(8, 85)

        self.diagnosis.setGeometry(QtCore.QRect(10, 370, self.width() - 180, 61))
        self.chenge_data_of_patient.setGeometry(QtCore.QRect(self.width() - 180, 370, 170, 40))
        self.search.setGeometry(QtCore.QRect(330, 10, self.width() - 340, 30))
        self.name_patient.setGeometry(QtCore.QRect(330, 40, self.width() - 340, 30))
        self.label_6.setGeometry(QtCore.QRect(self.width() - 340, 70, 240, 31))
        self.label_8.setGeometry(QtCore.QRect(self.width() - 460, 100, 40, 31))
        self.label_9.setGeometry(QtCore.QRect(self.width() - 460, 130, 40, 31))
        self.label_10.setGeometry(QtCore.QRect(self.width() - 460, 160, 40, 31))
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(self.width() - 420, 100, 410, 30))
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(self.width() - 420, 130, 410, 30))
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(self.width() - 420, 160, 410, 30))
        self.label_7.setGeometry(QtCore.QRect(self.width() - 450, 200, 321, 60))
        self.number_of_exercises.setGeometry(QtCore.QRect(self.width() - 120, 220, 110, 30))
        self.description.setGeometry(QtCore.QRect(self.width() - 450, 260, 440, 50))
        self.add_new_day_button.setGeometry(QtCore.QRect(self.width() - 450, 320, 440, 40))

