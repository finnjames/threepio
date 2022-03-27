import time
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

        self.set_clock(self.clock, self.ui.sidereal_value.text())

        try:
            self.parent_window.clear_stripchart()
        except AttributeError:
            pass  # when the stripchart hasn't been initialized yet

        self.close()

    @staticmethod
    def set_clock(superclock, input: str, epoch=None):
        if epoch is None:
            epoch = time.time()

        # pattern = "%H:%M:%S"
        superclock.set_starting_sidereal_time(
            3600 * int(input[:2]) + 60 * int(input[3:5]) + int(input[6:])
        )
        superclock.set_starting_time(epoch)

        with open("ra-cal.txt", "w") as f:
            f.write(input + "\n" + str(epoch))
