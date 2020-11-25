import sys, os, sqlite3
from datetime import datetime, timedelta, date

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QLabel
from PyQt5.QtWidgets import QGridLayout, QProgressBar, QWidget, QTableWidget
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QInputDialog, QFileDialog
from PyQt5.QtCore import Qt

from login_in_system import LoggingInSystem


app = QApplication(sys.argv)   # создаёт и отображает окно входа в систему
ex = LoggingInSystem()
ex.show()
sys.exit(app.exec_())
