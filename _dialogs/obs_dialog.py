"""dialogue box for keying in a new observation"""
from typing import Optional

from PyQt5.QtWidgets import QDialog, QWidget
from PyQt5.QtCore import Qt, QTime
from layouts import obs_ui  # compiled PyQt dialogue ui
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
        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)

        self.obs = obs
        self.clock: SuperClock = clock

        # dictionary of fields and their get/set functions
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

        # just checking data
        self.info = info
        self.records: Optional[ObsRecord] = None
        if self.info:
            self.unwrap(obs.input_record)
            self.ui.accept_button.setText("Close")
            self.ui.cancel_button.hide()
            # TODO: show info about the observation

        self.confirmed = False

        # make default filename
        self.default_filename = self.clock.get_time_slug()
        self.ui.file_name_value.setPlaceholderText(str(self.default_filename))

        # set default ra
        for i in [self.ui.start_time, self.ui.end_time]:
            i.setTime(QTime(*self.clock.get_sidereal_tuple()))

        # hide error and warning labels to start
        self.clear_messages()

        # If a scan or spectrum, only one dec needed
        if self.obs.obs_type in [ObsType.SCAN, ObsType.SPECTRUM]:
            for i in [self.ui.max_dec, self.ui.end_dec_label]:
                i.hide()
            self.ui.max_dec.setText("65535")  # TODO: change this?
            self.ui.start_dec_label.setText("Declination")
        if self.obs.obs_type in [ObsType.SPECTRUM, ObsType.SURVEY]:
            for i in [
                self.ui.data_acquisition_rate_label,
                self.ui.data_acquisition_rate_value,
            ]:
                i.hide()
            # all spectra and surveys have data acquisition rates of 6
            self.ui.data_acquisition_rate_value.setValue(6)
        if self.obs.obs_type is ObsType.SPECTRUM:
            for i in [self.ui.end_label, self.ui.end_time]:
                i.hide()
            # all spectra have a duration of 120 seconds
            self.ui.end_time.setTime(QTime(23, 59, 59))  # TODO: failure at 23:59:59?
        self.adjustSize()

        # store parent window
        self.parent_window = parent_window

    def accept(self):
        if self.info:
            self.close()
        try:
            self.clear_messages()
            if not self.confirmed:
                self.set_observation()
                # confirm
                self.wrap()
                self.ui.accept_button.setText("Start Observation")
                self.ui.error_label.hide()
                self.adjustSize()
                self.confirmed = True
            else:  # already confirmed -> set observation and close
                self.close()

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
        for i in [self.ui.error_label, self.ui.warning_label]:
            i.hide()

    def get_filename(self):
        if self.ui.file_name_value.text() == "":
            return self.default_filename
        return self.ui.file_name_value.text()

    def unwrap(self, record: ObsRecord):
        """unwrap the record into the fields"""
        for name, (widget, getter, setter) in self.fields.items():
            setter(getattr(record, name))
        self.wrap()

    def wrap(self):
        """wrap the fields into record"""
        self.set_read_only()
        self.records = ObsRecord(
            **{name: getter() for name, (widget, getter, setter) in self.fields.items()}
        )
        self.obs.input_record = self.records

    def set_read_only(self):
        for i in self.fields.values():
            i[0].setDisabled(True)

    def set_observation(self):
        """attempt to add all necessary info to the encapsulated observation"""

        # parse times; pattern = "HH:MM:SS"
        starting_ra = SuperClock.deformat_time(self.ui.start_time.text())
        ending_ra = SuperClock.deformat_time(self.ui.end_time.text())
        if ending_ra < starting_ra:
            ending_ra += 3600 * 24
            self.show_warning("Assuming ending RA is the next day")

        # calculate start and end times
        solar = self.clock.get_time()  # current solar time
        sidereal = self.clock.get_sidereal_seconds()  # current sidereal seconds
        start_time = solar + self.clock.sidereal_to_solar(starting_ra - sidereal)
        end_time = (
            (solar + self.clock.sidereal_to_solar(ending_ra - sidereal))
            if self.obs.obs_type is not ObsType.SPECTRUM
            else start_time + 180
        )

        # if no filename, use default
        filename = self.ui.file_name_value.text()
        if filename == "":
            filename = self.default_filename
        self.obs.set_name(filename)

        # attempt to set data of observation
        self.obs.set_ra(start_time, end_time)
        try:
            new_min_dec = int(self.ui.min_dec.text())
            new_max_dec = int(self.ui.max_dec.text())
        except ValueError:
            raise ValueError("Dec vals must be integers")
        self.obs.set_dec(new_min_dec, new_max_dec)

        self.obs.set_data_freq(int(self.ui.data_acquisition_rate_value.text()))
