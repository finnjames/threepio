from PyQt5.QtWidgets import QDialog, QWidget
from PyQt5.QtCore import Qt
from layouts import dec_cal_ui  # compiled PyQt dialogue ui
from tools import DecCalc as dc


class DecDialog(QDialog):
    """New observation dialogue window"""

    CAL_FILENAME = "dec-cal.txt"
    CAL_BACKUP_FILENAME = "dec-cal-backup.txt"

    def __init__(self, minitars, parent):
        QWidget.__init__(self)
        self.ui = dec_cal_ui.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Calibrate declination")

        # hide the close/minimize/fullscreen buttons and make window always on top
        self.setWindowFlags(
            Qt.Window
            | Qt.WindowTitleHint
            | Qt.CustomizeWindowHint
            | Qt.WindowStaysOnTopHint
        )

        self.data = []
        self.current_dec = dc.SOUTH_DEC
        self.step = dc.STEP
        self.update_label()

        self.minitars = minitars
        self.parent = parent

        # connect buttons
        self.ui.discard_cal_button.clicked.connect(self.handle_discard)
        self.ui.next_cal_button.clicked.connect(self.handle_next)
        self.ui.north_or_south_combo_box.currentIndexChanged.connect(
            self.switch_direction
        )

        self.confirmed = False

    def switch_direction(self):
        if self.ui.north_or_south_combo_box.currentIndex() == 0:
            self.current_dec = dc.SOUTH_DEC
            self.step = 10
        else:
            self.current_dec = dc.NORTH_DEC
            self.step = -10
        self.update_label()

    def handle_next(self):

        self.parent.beep()

        if not self.confirmed:
            self.set_confirmed_true()
        else:
            # read just the declination value
            new_dec = None
            while new_dec is None:
                new_dec = self.minitars.read_latest()
            if (
                len(self.data) >= 2
                and (new_dec - self.data[-1]) * (self.data[-1] - self.data[-2]) <= 0
            ):
                self.parent.log("Dec cal failed, non-monotonic data")
                self.handle_discard()

            self.data.append(new_dec)

            self.current_dec += self.step
            self.ui.next_cal_button.setText("Next")
            self.ui.discard_cal_button.setText("Discard")
            self.ui.set_dec_label.setText("Set declination to")

            if self.current_dec not in [dc.SOUTH_DEC, dc.NORTH_DEC]:
                # disable N/S choice if not first
                self.ui.north_or_south_combo_box.setDisabled(True)
            elif self.current_dec <= dc.SOUTH_DEC or self.current_dec >= dc.NORTH_DEC:
                self.ui.next_cal_button.setText("Save")

            self.update_label()
            self.confirmed = False

            # is calibration complete?
            if self.current_dec > dc.NORTH_DEC or self.current_dec < dc.SOUTH_DEC:
                # copy over the current file to the backup file
                with open(self.CAL_FILENAME) as f, open(
                    self.CAL_BACKUP_FILENAME, "w"
                ) as b:
                    for line in f:
                        b.write(line)

                open(self.CAL_FILENAME, "w").close()  # overwrite file
                with open(self.CAL_FILENAME, "a") as f:
                    self.step < 0 and self.data.reverse()  # reverse if N -> S

                    f.write("\n".join(str(line) for line in self.data))

                self.close()

    def handle_discard(self):
        if self.confirmed:
            self.set_confirmed_false()
        else:
            self.close()

    def update_label(self):
        self.ui.set_dec_value.setText(str(self.current_dec) + "°")

    def set_confirmed_true(self):
        self.confirmed = True
        self.ui.set_dec_label.setText("Are you sure?")
        self.ui.discard_cal_button.setText("No")
        self.ui.next_cal_button.setText("Yes")

    def set_confirmed_false(self):
        self.confirmed = False
        self.ui.next_cal_button.setText("Next")
        self.ui.discard_cal_button.setText("Discard")
        self.ui.set_dec_label.setText("Set declination to")
