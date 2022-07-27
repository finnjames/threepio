from PyQt5.QtWidgets import QDialog, QWidget
from PyQt5.QtCore import Qt
from _tools.superclock import SuperClock
from layouts import ra_cal_ui  # compiled PyQt dialogue ui


class RADialog(QDialog):
    """New observation dialogue window"""

    def __init__(self, parent_window, superclock: SuperClock):
        QWidget.__init__(self)
        self.ui = ra_cal_ui.Ui_Dialog()
        self.ui.setupUi(self)

        # store parent window and superclojck
        self.parent_window = parent_window
        self.clock = superclock

        # hide the close/minimize/fullscreen buttons
        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)

    def accept(self):

        self.clock.calibrate(SuperClock.deformat_time(self.ui.sidereal_value.text()))

        try:
            self.parent_window.clear_stripchart()
        except AttributeError:
            pass  # when the stripchart hasn't been initialized yet

        self.close()
