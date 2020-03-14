"""dialogue box for keying in a new observation"""

from PyQt5 import QtCore, QtWidgets, QtGui, QtChart
from layouts import obs_ui     # compiled PyQt dialogue ui
import time
from precious import MyPrecious

class ObsDialog(QtWidgets.QDialog):
    """New observation dialogue window"""
    def __init__(self, parent_window, current_time, observation, clock):
        QtWidgets.QWidget.__init__(self)
        self.ui = obs_ui.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Threepio Dialogue")
        self.observation = observation
        self.clock = clock
        
        # If a scan or spectrum, only one Dec needed
        if self.observation.obs_type == "Scan" or self.observation.obs_type == "Spectrum":
            self.ui.ending_dec.hide()
            self.ui.end_dec_label.hide()
            self.ui.ending_dec.setText("0")
            self.ui.start_dec_label.setText("Declination")
        
        # store parent window
        self.parent_window = parent_window

        # connect okay button
        self.ui.dialog_button_box.accepted.connect(self.handle_ok)

    def handle_ok(self):
        self.set_observation()
        self.parent_window.observation = None
        self.parent_window.observation = self.observation
        
        # this should fix the stripchart, #nojudgement #TODO: is this still necessary?
        self.parent_window.data = []
        self.parent_window.stripchart_offset = 0
        self.parent_window.stripchart_series_a.clear()
        self.parent_window.stripchart_series_b.clear()
        
    def set_observation(self):
        # pattern = "%H:%M:%S"
        
        u_start_time = self.ui.start_time.text()
        starting_sidereal_time = 3600*int(u_start_time[:2]) + 60*int(u_start_time[3:5]) + int(u_start_time[6:])
        u_end_time = self.ui.end_time.text()
        ending_sidereal_time = 3600*int(u_end_time[:2]) + 60*int(u_end_time[3:5]) + int(u_end_time[6:])
        
        start_time = starting_sidereal_time - self.clock.get_sidereal_seconds() + time.time()
        end_time = ending_sidereal_time - self.clock.get_sidereal_seconds() + time.time()
        
        self.observation.set_RA(start_time, end_time)
        self.observation.set_dec(int(self.ui.starting_dec.text()), int(self.ui.ending_dec.text()))
        self.observation.set_name(self.ui.file_name_value.text())
        self.observation.set_data_freq(int(self.ui.data_acquisition_rate_value.text()))