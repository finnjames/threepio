"""dialogue box for keying in a new observation"""

from PyQt5 import QtWidgets, QtCore
from layouts import obs_ui  # compiled PyQt dialogue ui
import time


class ObsDialog(QtWidgets.QDialog):
    """New observation dialogue window"""

    def __init__(self, parent_window, observation, clock):
        QtWidgets.QWidget.__init__(self)
        self.ui = obs_ui.Ui_Dialog()
        self.ui.setupUi(self)
        self.setModal(True)  # keep focus until dealt with
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowTitleHint | QtCore.Qt.CustomizeWindowHint)

        self.observation = observation
        self.clock = clock

        # make default filename
        self.default_filename = self.clock.get_time_slug()
        self.ui.file_name_value.setPlaceholderText(str(self.default_filename))

        # If a scan or spectrum, only one Dec needed
        if self.observation.obs_type == "Scan" or self.observation.obs_type == "Spectrum":
            self.ui.starting_dec.hide()
            self.ui.start_dec_label.hide()
            self.ui.starting_dec.setText("0")
            self.ui.end_dec_label.setText("Declination")

        # store parent window
        self.parent_window = parent_window

    def accept(self):
        exit_code = self.set_observation()
        if exit_code == 0:  # set_observation() executed successfully
            self.parent_window.observation = None
            self.parent_window.observation = self.observation
            self.close()
        else:
            print("error creating observation")

    def set_observation(self):
        """add all necessary info to the encapsulated observation; 1: error"""

        # pattern = "%H:%M:%S"
        u_start_time = self.ui.start_time.text()
        starting_sidereal_time = 3600 * int(u_start_time[:2]) + 60 * int(u_start_time[3:5]) + int(u_start_time[6:])
        u_end_time = self.ui.end_time.text()
        ending_sidereal_time = 3600 * int(u_end_time[:2]) + 60 * int(u_end_time[3:5]) + int(u_end_time[6:])

        start_time = starting_sidereal_time - self.clock.get_sidereal_seconds() + time.time()
        end_time = ending_sidereal_time - self.clock.get_sidereal_seconds() + time.time()

        # set all of the relevant data to the observation
        # if no filename, use timestamp
        filename = self.ui.file_name_value.text()
        if filename == "":
            filename = self.default_filename
        self.observation.set_name(filename)

        # catch when the user doesn't bother to put in a declination or data frequency
        try:
            self.observation.set_ra(start_time, end_time)
            self.observation.set_dec(int(self.ui.ending_dec.text()), int(self.ui.starting_dec.text()))
            self.observation.set_data_freq(int(self.ui.data_acquisition_rate_value.text()))
        except ValueError:
            return 1

        return 0
