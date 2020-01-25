"""dialogue box for keying in a new observation"""

from PyQt5 import QtCore, QtWidgets, QtGui, QtChart
from dialog_ui import Ui_Dialog     # compiled PyQt dialogue ui
import time
from precious import MyPrecious

class Dialog(QtWidgets.QDialog):
    """New observation dialogue window"""
    def __init__(self, parent_window, date, observation):
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Threepio Dialogue")
        self.observation = observation
        
        # If a scan or spectrum, only one Dec needed
        if self.observation.obs_type == "Scan" or self.observation.obs_type == "Spectrum":
            self.ui.ending_dec.hide()
            self.ui.end_dec_label.hide()
            self.ui.start_dec_label.setText("Declination")
        
        # set today's date
        self.current_date = QtCore.QDate(time.localtime(date)[0], time.localtime(date)[1], time.localtime(date)[2])
        self.current_time = QtCore.QTime(time.localtime(date)[3], time.localtime(date)[4], 0)
        self.ui.start_time.setDate(self.current_date)
        self.ui.start_time.setTime(self.current_time)
        self.ui.end_time.setDate(self.current_date)
        self.ui.end_time.setTime(self.current_time)

        # store parent window
        self.parent_window = parent_window

        # connect okay button
        self.ui.dialog_button_box.accepted.connect(self.handle_ok)

    def handle_ok(self):
        self.set_observation()
        self.parent_window.observation = None
        self.parent_window.observation = self.observation
        
        # this should fix the stripchart, #nojudgement
        self.parent_window.stripchart_offset = 0
        self.parent_window.stripchart_series_a.clear()
        self.parent_window.stripchart_series_b.clear()
        
    def set_observation(self):
        pattern = "%Y.%m.%d %H:%M:%S"
        
        self.observation.set_RA(int(time.mktime(time.strptime(self.ui.start_time.text(), pattern))), int(time.mktime(time.strptime(self.ui.end_time.text(), pattern))))
        self.observation.set_dec(self.ui.starting_dec.text(), self.ui.ending_dec.text())
        
        self.observation.set_precious(MyPrecious(self.ui.file_name_value))