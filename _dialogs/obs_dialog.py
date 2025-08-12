"""Dialogue box for keying in a new observation"""
import time
from typing import Optional

from PyQt5.QtWidgets import QDialog, QWidget
from PyQt5.QtCore import Qt, QTime
from layouts import obs_ui
from tools import Alert, SuperClock, ObsType, Observation, ObsRecord


class ObsDialog(QDialog):
    """New observation dialogue window"""

    def __init__(
        self,
        parent_window,
        obs: Observation,
        clock: SuperClock,
        info=False,
    ):
        QWidget.__init__(self)
        self.ui = obs_ui.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint) # type: ignore

        self.obs = obs
        self.clock: SuperClock = clock

        # Dictionary of fields and their get/set functions
        self.fields = {
            "start_time": (
                self.ui.start_time,
                self.ui.start_time.time,
                self.ui.start_time.setTime,
            ),
            "end_time": (
                self.ui.end_time,
                self.ui.end_time.time,
                self.ui.end_time.setTime,
            ),
            "min_dec": (self.ui.min_dec, self.ui.min_dec.text, self.ui.min_dec.setText),
            "max_dec": (self.ui.max_dec, self.ui.max_dec.text, self.ui.max_dec.setText),
            "data_acquisition_rate_value": (
                self.ui.data_acquisition_rate_value,
                self.ui.data_acquisition_rate_value.value,
                self.ui.data_acquisition_rate_value.setValue,
            ),
            "file_name_value": (
                self.ui.file_name_value,
                self.get_filename,
                self.ui.file_name_value.setText,
            ),
        }

        # Just checking data
        self.info = info
        self.records: Optional[ObsRecord] = None
        if self.info:
            assert obs.input_record is not None
            self.unwrap(obs.input_record)
            self.ui.accept_button.setText("Close")
            self.ui.cancel_button.hide()
            # TODO: Show info about the observation
        else:
            # Set default ra
            for i in [self.ui.start_time, self.ui.end_time]:
                i.setTime(QTime(*self.clock.get_sidereal_tuple()))

        self.confirmed = False

        # Make default filename
        self.default_filename = self.clock.get_time_slug()
        self.ui.file_name_value.setPlaceholderText(str(self.default_filename))

        # Hide error and warning labels to start
        self.clear_messages()

        # If a scan or spectrum, only one dec needed
        if self.obs.obs_type in [ObsType.SCAN, ObsType.SPECTRUM]:
            for i in [self.ui.max_dec, self.ui.end_dec_label]:
                i.hide()
            self.ui.max_dec.setText("65535")  # Arbitrary large number
            self.ui.start_dec_label.setText("Declination")
        if self.obs.obs_type in [ObsType.SPECTRUM, ObsType.SURVEY]:
            for i in [
                self.ui.data_acquisition_rate_label,
                self.ui.data_acquisition_rate_value,
            ]:
                i.hide()
            # All spectra and surveys have data acquisition rates of 6
            self.ui.data_acquisition_rate_value.setValue(6)
        if self.obs.obs_type is ObsType.SPECTRUM:
            for i in [self.ui.end_label, self.ui.end_time]:
                i.hide()
            # All spectra have a duration of 120 seconds
            self.ui.end_time.setTime(QTime(23, 59, 59))  # TODO: failure at 23:59:59?
        self.adjustSize()

        # Store parent window
        self.parent_window = parent_window

    def accept(self):
        if self.info:
            self.close()
        try:
            self.clear_messages()
            if not self.confirmed:
                self.set_observation()
                # Confirm
                self.wrap()
                self.ui.accept_button.setText("Start Observation")
                self.ui.error_label.hide()
                self.adjustSize()
                self.confirmed = True
            else:  # Already confirmed -> set observation and close
                self.close()

                assert self.obs.min_dec is not None
                target_dec = self.obs.min_dec - (
                    2 if (self.obs.obs_type is ObsType.SURVEY) else 0
                )

                def callback():
                    self.parent_window.obs = self.obs

                alerts = [
                    Alert(f"Move the telescope to {target_dec}° declination", "Okay"),
                    Alert(f"Is the telescope at {target_dec}° declination?", "Yes"),
                    Alert("Set frequency to 1319.5MHz", "Okay"),
                    Alert("Is the frequency set to 1319.5MHz?", "Yes"),
                ]
                self.parent_window.alert(
                    *alerts[: (4 if self.obs.obs_type is ObsType.SPECTRUM else 2)],
                    callback=callback,
                )

        except ValueError as err:
            self.show_error(str(err))

    def show_error(self, message: str):
        self.ui.error_label.setText(message)
        self.ui.error_label.show()

    def show_warning(self, message: str):
        self.ui.warning_label.setText(message)
        self.ui.warning_label.show()

    def clear_messages(self):
        self.ui.error_label.hide()
        self.ui.warning_label.hide()

    def get_filename(self):
        if self.ui.file_name_value.text() == "":
            return self.default_filename
        return self.ui.file_name_value.text()

    def unwrap(self, record: ObsRecord):
        """Unwrap the record into the fields"""
        for name, (widget, getter, setter) in self.fields.items():
            setter(getattr(record, name))
        self.wrap()

    def wrap(self):
        """Wrap the fields into record"""
        self.set_read_only()
        self.records = ObsRecord(
            **{name: getter() for name, (widget, getter, setter) in self.fields.items()}
        )
        self.obs.input_record = self.records

    def set_read_only(self):
        for i in self.fields.values():
            i[0].setDisabled(True)

    def set_observation(self):
        """Attempt to add all necessary info to the encapsulated observation"""

        # Parse times; pattern = "HH:MM:SS"
        starting_ra = SuperClock.deformat_time_string(self.ui.start_time.text())
        ending_ra = SuperClock.deformat_time_string(self.ui.end_time.text())
        if ending_ra < starting_ra:
            ending_ra += 3600 * 24
            self.show_warning("Assuming ending RA is the next day")

        # Calculate start and end times
        solar = self.clock.get_starting_epoch_time()  # Solar time of last calibration
        sidereal = self.clock.get_starting_sidereal_time()  # Sidereal seconds since midnight before last calibration
        start_time = solar + SuperClock.sidereal_to_solar(starting_ra - sidereal)
        print(f"{solar=}, {sidereal=}, {starting_ra=}, {start_time=}, current time={time.time()}")
        end_time = (
            (solar + self.clock.sidereal_to_solar(ending_ra - sidereal))
            if self.obs.obs_type is not ObsType.SPECTRUM
            else start_time + 180
        )
        print(f"{ending_ra=}, {end_time=}, current time={time.time()}")

        # If no filename, use default
        filename = self.ui.file_name_value.text()
        if filename == "":
            filename = self.default_filename
        self.obs.set_name(filename)

        # Attempt to set observation data
        self.obs.set_start_and_end_times(start_time, end_time)
        try:
            new_min_dec = int(self.ui.min_dec.text())
            new_max_dec = int(self.ui.max_dec.text())
        except ValueError:
            raise ValueError("Dec vals must be integers")
        self.obs.set_dec(new_min_dec, new_max_dec)

        self.obs.set_data_freq(int(self.ui.data_acquisition_rate_value.text()))
