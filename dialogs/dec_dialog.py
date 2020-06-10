import math
import random

from PyQt5 import QtWidgets, QtCore

from layouts import dec_cal_ui  # compiled PyQt dialogue ui


class DecDialog(QtWidgets.QDialog):
    """New observation dialogue window"""

    start_dec = -25
    end_dec = 95
    step = 10

    def __init__(self, tars):
        QtWidgets.QWidget.__init__(self)
        self.ui = dec_cal_ui.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Calibrate declination")

        # hide the close/minimize/fullscreen buttons
        self.setWindowFlags(
            QtCore.Qt.Window | QtCore.Qt.WindowTitleHint | QtCore.Qt.CustomizeWindowHint)

        self.data = []
        self.current_dec = self.start_dec
        self.ui.set_dec_value.setText(str(self.current_dec))

        self.tars = tars

        # connect buttons
        self.ui.discard_cal_button.clicked.connect(self.handle_discard)
        self.ui.next_cal_button.clicked.connect(self.handle_next)

        self.handle_next()

    def handle_next(self):
        if self.current_dec > self.end_dec:  # base case, calibration complete

            # copy over the current file to the backup file
            with open("dec_cal.txt") as f:
                with open("dec_cal_backup.txt", 'w') as b:
                    for line in f:
                        b.write(line)

            open("dec_cal.txt", 'w').close()  # overwrite file
            f = open("dec_cal.txt", 'a')

            # reverse it if it's N -> S
            if self.ui.north_or_south_combo_box.currentIndex() == 1:
                self.data.reverse()

            for line in self.data:  # replace with new calibration data
                if line == self.data[len(self.data) - 1]:
                    f.write(str(line))
                else:
                    f.write(str(line) + '\n')
            self.close()
        else:
            # TODO: make this a little less hard-coded
            self.data.append(self.tars.read_latest()[2][1])  # read just the declination value

            self.ui.set_dec_value.setText(str(self.current_dec))
            if self.current_dec == self.end_dec:
                # specify action if it will save and not just progress
                self.ui.next_cal_button.setText("Save")
            elif self.current_dec > self.start_dec:
                # disable N/S choice if not first
                self.ui.north_or_south_combo_box.setDisabled(True)

            self.current_dec += self.step

    def handle_discard(self):
        self.close()
