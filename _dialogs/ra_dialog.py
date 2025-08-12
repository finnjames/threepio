from PyQt5.QtWidgets import QDialog, QWidget
from PyQt5.QtCore import Qt
from _tools.superclock import SuperClock
from layouts import ra_cal_ui


class RADialog(QDialog):
    """New observation dialogue window"""

    def __init__(self, parent_window, superclock: SuperClock):
        QWidget.__init__(self)
        self.ui = ra_cal_ui.Ui_Dialog()
        self.ui.setupUi(self)

        # Store parent window and superclock
        self.parent_window = parent_window
        self.clock = superclock

        # Hide the close/minimize/fullscreen buttons
        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)  # type: ignore

    def accept(self):

        sidereal_seconds = SuperClock.deformat_time_string(self.ui.sidereal_value.text())
        self.clock.calibrate_sidereal_time(sidereal_seconds)

        try:
            self.parent_window.clear_stripchart()
        except AttributeError:
            pass  # When the stripchart hasn't been initialized yet

        self.close()
