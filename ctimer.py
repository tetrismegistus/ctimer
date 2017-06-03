
from PyQt5.QtWidgets import (QMainWindow, QLCDNumber, QWidget, QApplication, QVBoxLayout, QHBoxLayout,
                             QDateEdit, QPushButton, QDialog, QDialogButtonBox)
from PyQt5.QtCore import QTimer, QDateTime
from PyQt5.QtGui import QIcon
from dateutil.relativedelta import relativedelta
import datetime as pydt
import os
import sys
import pickle


class ClockPanel(QLCDNumber):
    def __init__(self):
        super(ClockPanel, self).__init__()
        self.setDigitCount(19)
        # '00 y 000 d 00:00:00' three digit years seemed a bit optimistic
        style = 'QLCDNumber { background-color: gray; color: black; }'
        self.setStyleSheet(style)
        self.setSegmentStyle(QLCDNumber.Flat)
        self.setFixedSize(460, 57)

    def update_display(self, time_string='00 y 000 d 00:00:00'):
        self.display(time_string)


class InitTimeDialog(QDialog):
    def __init__(self):
        super(InitTimeDialog, self).__init__()
        layout = QVBoxLayout(self)
        self.datetime = QDateEdit(self)
        self.datetime.setCalendarPopup(True)
        self.datetime.setDateTime(QDateTime.currentDateTime())
        button = QDialogButtonBox(QDialogButtonBox.Ok, self)
        button.accepted.connect(self.accept)
        layout.addWidget(self.datetime)
        layout.addWidget(button)
        self.setWindowTitle('Start Date')
        self.setWindowIcon(QIcon('icon.png'))

    def get_datetime(self):
        return self.datetime.dateTime()

    @staticmethod
    def display_dialog():
        dialog = InitTimeDialog()
        dialog.exec_()
        date = dialog.get_datetime()
        return date.date()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        reset_button = QPushButton('Reset')
        reset_button.clicked.connect(self.reset_timestamp)

        self.panel = ClockPanel()
        self.time_dialog = InitTimeDialog()
        self.setWindowTitle('CTimer')
        self.timestamp = self.load_time()
        self.update_time()

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(reset_button)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.panel)
        main_layout.addLayout(button_layout)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)

        self.setCentralWidget(main_widget)
        # help pyinstaller find icon file

        self.setWindowIcon(QIcon('icon.png'))
        self.setFixedSize(self.sizeHint())

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.show()

    def time_elapsed(self):
        current_time = pydt.datetime.now()
        elapsed = relativedelta(current_time, self.timestamp)
        years, days, hours, minutes, seconds = elapsed.years, elapsed.days, elapsed.hours, elapsed.minutes, \
                                               elapsed.seconds
        time_string = ''
        if years > 0:
            time_string = '{} y '.format(years) + time_string
        if days > 0:
            time_string = time_string + '{} d '.format(days)
        time_string += '{0:02d}'.format(hours)
        time_string += ':{0:02d}'.format(minutes)
        time_string += ':{0:02d}'.format(seconds)

        return time_string

    def update_time(self):
        self.panel.update_display(self.time_elapsed())

    def reset_timestamp(self):
        self.timer.stop()
        os.remove('timestam.p')
        self.timestamp = QDateTime(InitTimeDialog.display_dialog()).toPyDateTime()
        pickle.dump(self.timestamp, open('timestam.p', 'wb'))
        self.timer.start(1000)

    @staticmethod
    def load_time():
        try:
            return pickle.load(open('timestam.p', 'rb'))
        except FileNotFoundError:
            date = QDateTime(InitTimeDialog.display_dialog()).toPyDateTime()
            pickle.dump(date, open('timestam.p', 'wb'))
            return date


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
