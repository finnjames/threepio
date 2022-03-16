"""dialogue box for keying in a new observation"""

from PyQt5 import QtWidgets, QtCore
from layouts import obs_ui  # compiled PyQt dialogue ui
import time
from tools.alert import Alert

from tools.observation import Observation
from tools.inputrecord import InputRecord


class ObsDialog(QtWidgets.QDialog):
    """New observation dialogue window"""

    def __init__(self, parent_window, observation: Observation, clock, info=False):
        QtWidgets.QWidget.__init__(self)
        self.ui = obs_ui.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowFlags(
            QtCore.Qt.Window | QtCore.Qt.WindowTitleHint | QtCore.Qt.CustomizeWindowHint
        )

        self.observation = observation
        self.clock = clock

        # just checking data
        self.info = info
        self.records: InputRecord = None
        if self.info:
            self.unwrap(observation.input_record)
            self.ui.accept_button.setText("Close")
            self.ui.cancel_button.hide()
            # TODO: show info about the observation

        self.confirmed = False

        # make default filename
        self.default_filename = self.clock.get_time_slug()
        self.ui.file_name_value.setPlaceholderText(str(self.default_filename))

        # hide error label to start
        self.ui.error_label.hide()

        # If a scan or spectrum, only one Dec needed
        if self.observation.obs_type in ["Scan", "Spectrum"]:
            for i in [self.ui.max_dec, self.ui.end_dec_label]:
                i.hide()
            self.ui.max_dec.setText("65535")
            self.ui.start_dec_label.setText("Declination")
        if self.observation.obs_type in ["Spectrum", "Survey"]:
            for i in [
                self.ui.data_acquisition_rate_label,
                self.ui.data_acquisition_rate_value,
            ]:
                i.hide()
            # all spectra and surveys have data acquisition rates of 6
            self.ui.data_acquisition_rate_value.setValue(6)
        if self.observation.obs_type == "Spectrum":
            for i in [self.ui.end_label, self.ui.end_time]:
                i.hide()
        self.adjustSize()

        # store parent window
        self.parent_window = parent_window

    def accept(self):
        if self.info:
            self.close()
        try:
            self.set_observation()
            if self.confirmed:  # set observation and close
                self.parent_window.observation = self.observation
                self.close()

                target_dec = self.observation.min_dec - (
                    2 if (self.observation.obs_type == "Survey") else 0
                )
                self.parent_window.alert(
                    Alert(f"Move the telescope to {target_dec}° declination", "Okay"),
                    Alert(f"Is the telescope at {target_dec}° declination?", "Yes"),
                )
                if self.observation.obs_type == "Spectrum":
                    self.parent_window.alert(
                        Alert("Set frequency to 1319.5MHz", "Okay"),
                        Alert("Is the frequency set to 1319.5MHz?", "Yes"),
                    )
            else:  # set_observation() executed successfully
                self.wrap()
                self.ui.accept_button.setText("Start Observation")
                self.ui.error_label.hide()
                self.adjustSize()
                self.confirmed = True
        except ValueError as err:
            self.ui.error_label.setText(str(err))
            self.ui.error_label.show()

    def get_filename(self):
        if self.ui.file_name_value.text() == "":
            return self.default_filename
        return self.ui.file_name_value.text()

    def unwrap(self, record: InputRecord):
        self.ui.start_time.setTime(record.start_time)
        self.ui.end_time.setTime(record.end_time)
        self.ui.min_dec.setText(record.min_dec)
        self.ui.max_dec.setText(record.max_dec)
        self.ui.data_acquisition_rate_value.setValue(record.data_acquisition_rate_value)
        self.ui.file_name_value.setText(record.file_name_value)
        self.wrap()

    def wrap(self):
        self.set_read_only()
        self.records = InputRecord(
            self.ui.start_time.time(),
            self.ui.end_time.time(),
            self.ui.min_dec.text(),
            self.ui.max_dec.text(),
            self.ui.data_acquisition_rate_value.value(),
            self.get_filename(),
        )
        self.observation.input_record = self.records

    def set_read_only(self):
        for i in [
            self.ui.start_time,
            self.ui.end_time,
            self.ui.min_dec,
            self.ui.max_dec,
            self.ui.file_name_value,
            self.ui.data_acquisition_rate_value,
        ]:
            i.setEnabled(False)

    def set_observation(self):
        """add all necessary info to the encapsulated observation; 1: error"""

        # pattern = "%H:%M:%S"
        u_start_time = self.ui.start_time.text()
        starting_sidereal_time = (
            3600 * int(u_start_time[:2])
            + 60 * int(u_start_time[3:5])
            + int(u_start_time[6:])
        )
        u_end_time = self.ui.end_time.text()
        ending_sidereal_time = (
            3600 * int(u_end_time[:2]) + 60 * int(u_end_time[3:5]) + int(u_end_time[6:])
        )
        if ending_sidereal_time < starting_sidereal_time:
            ending_sidereal_time += 3600 * 24

        start_time = (
            starting_sidereal_time - self.clock.get_sidereal_seconds() + time.time()
        )
        end_time = (
            (ending_sidereal_time - self.clock.get_sidereal_seconds() + time.time())
            if self.observation.obs_type != "Spectrum"
            else start_time + 180
        )

        # final check and write to observation

        # if no filename, use default (timestamp)
        filename = self.ui.file_name_value.text()
        if filename == "":
            filename = self.default_filename
        self.observation.set_name(filename)

        # attempt to set data of observation
        self.observation.set_ra(start_time, end_time)
        try:
            new_min_dec = int(self.ui.min_dec.text())
            new_max_dec = int(self.ui.max_dec.text())
        except ValueError:
            raise ValueError("Declination must be an integer")
        self.observation.set_dec(new_min_dec, new_max_dec)

        self.observation.set_data_freq(int(self.ui.data_acquisition_rate_value.text()))

        return 0
