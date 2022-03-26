from PyQt5 import QtWidgets, QtCore
from layouts import ra_cal_ui  # compiled PyQt dialogue ui


class RADialog(QtWidgets.QDialog):
    """New observation dialogue window"""

    def __init__(self, parent_window, superclock, cancelable: bool):
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

        if not cancelable:
            self.ui.cancel_button.hide()

    def accept(self):
        # pattern = "%H:%M:%S"

        ut = self.ui.sidereal_value.text()  # user time
        self.clock.set_starting_sidereal_time(
            3600 * int(ut[:2]) + 60 * int(ut[3:5]) + int(ut[6:])
        )
        self.clock.reset_starting_time()

        try:
            self.parent_window.clear_stripchart()
        except AttributeError:
            pass  # when the stripchart hasn't been initialized yet

        self.close()
