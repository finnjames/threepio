import time
from PyQt5 import QtWidgets, QtCore
from _tools.superclock import SuperClock
from layouts import ra_cal_ui  # compiled PyQt dialogue ui


class RADialog(QtWidgets.QDialog):
    """New observation dialogue window"""

    def __init__(self, parent_window, superclock: SuperClock):
        QtWidgets.QWidget.__init__(self)
        self.ui = ra_cal_ui.Ui_Dialog()
        self.ui.setupUi(self)

        # store parent window and superclock
        self.parent_window = parent_window
        self.clock = superclock

        # hide the close/minimize/fullscreen buttons
        self.setWindowFlags(
            QtCore.Qt.Window | QtCore.Qt.WindowTitleHint | QtCore.Qt.CustomizeWindowHint
        )

    def accept(self):

        self.clock.calibrate(self.ui.sidereal_value.text())

        try:
            self.parent_window.clear_stripchart()
        except AttributeError:
            pass  # when the stripchart hasn't been initialized yet

        self.close()
