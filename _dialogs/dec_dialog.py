from enum import Enum
from functools import reduce
from PyQt5.QtWidgets import QDialog, QWidget
from PyQt5.QtCore import Qt
from layouts import dec_cal_ui  # compiled PyQt dialogue ui
from tools import DecCalc as dc

class NorthSouth(Enum):
    NORTH = 0
    SOUTH = 1

class DecDialog(QDialog):
    """New observation dialogue window"""

    CAL_FILENAME = "dec-cal.txt"
    CAL_BACKUP_FILENAME = "dec-cal-backup.txt"

    def __init__(self, minitars, threepio):
        QWidget.__init__(self)
        self.ui = dec_cal_ui.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Calibrate declination")

        self.starting_dec = dc.SOUTH_DEC
        self.ending_dec = dc.NORTH_DEC
        self.direction = NorthSouth.NORTH
        self.step = dc.STEP
        self.current_dec = dc.SOUTH_DEC
        self.data = self.get_empty_data()
        self.confirmation_requested = False
        self.ui.warning_label.hide()
        self.update_labels()

        self.minitars = minitars
        self.parent = threepio

        # connect buttons
        self.ui.record_button.clicked.connect(self.handle_record)
        self.ui.next_button.clicked.connect(self.handle_next)
        self.ui.previous_button.clicked.connect(self.handle_previous)
        self.ui.save_button.clicked.connect(self.handle_save)
        self.ui.north_south_combo_box.currentIndexChanged.connect(
            self.set_direction
        )

    def set_direction(self):
        if self.ui.north_south_combo_box.currentIndex() == 0:
            self.starting_dec = dc.SOUTH_DEC
            self.current_dec = dc.SOUTH_DEC
            self.ending_dec = dc.NORTH_DEC
            self.step = dc.STEP
        else:
            self.starting_dec = dc.NORTH_DEC
            self.current_dec = dc.NORTH_DEC
            self.ending_dec = dc.SOUTH_DEC
            self.step = -dc.STEP
        self.data = self.get_empty_data()
        self.update_labels()
    
    def get_dec_range(self):
        return range(self.starting_dec, self.ending_dec + self.step, self.step)
    
    def get_empty_data(self):
        return {key: None for key in self.get_dec_range()}
    
    def handle_record(self):
        self.parent.beep()

        # read just the declination value
        new_dec = None
        while new_dec is None:
            new_dec = self.minitars.read_latest()

        self.data[self.current_dec] = new_dec

        nonmonotonic = False
        try:
            self.validate_data()
        except TypeError as e:
            nonmonotonic = True
        if nonmonotonic:
            self.ui.warning_label.setText("Warning: data is not monotonic")
            self.ui.warning_label.show()
        else:
            self.ui.warning_label.hide()

        self.move(self.step)

        self.update_labels()
    
    def handle_save(self):
        try:
            self.complete_calibration()
        except Exception as e:
            self.parent.log(f"Dec cal failed: {e.__str__()}")
        finally:
            self.close()

    def complete_calibration(self):
        self.validate_data(allow_incomplete=False)

        # copy over the current file to the backup file
        try:
            with open(self.CAL_FILENAME) as f, open(
                self.CAL_BACKUP_FILENAME, "w+"
            ) as b:
                for line in f:
                    b.write(line)
        except FileNotFoundError:
            pass

        with open(self.CAL_FILENAME, "w+") as f:
            write_str = ""
            for dec in range(dc.SOUTH_DEC, dc.NORTH_DEC + dc.STEP, dc.STEP):
                write_str += (f"{self.data[dec]}\n")
            f.write(write_str)

        self.move(-self.step)

    def validate_data(self, allow_incomplete = True):
        decs_to_test = self.get_dec_range()
        if allow_incomplete:
            decs_to_test = list(filter(lambda a: self.data[a] is not None, decs_to_test))
            assert sorted(decs_to_test) or sorted(decs_to_test, reverse=True)
        for i, _ in enumerate(decs_to_test):
            try:
                if i < 2:
                    continue
                this_dec = self.data[decs_to_test[i]]
                prior_dec = self.data[decs_to_test[i - 1]]
                twice_prior_dec = self.data[decs_to_test[i - 2]]
                assert this_dec is not None
                assert prior_dec is not None
                assert twice_prior_dec is not None
                if (this_dec - prior_dec) * (prior_dec - twice_prior_dec) <= 0:
                    raise TypeError("non-monotonic data")
            except AssertionError:
                if not allow_incomplete:
                    raise AssertionError("not all declinations recorded")
            except KeyError:
                pass
            except IndexError:
                pass

    def handle_next(self):
        self.move(self.step)

    def move(self, step: int):
        new_dec = self.current_dec + step

        if dc.SOUTH_DEC <= new_dec <= dc.NORTH_DEC:
            self.current_dec = new_dec
            self.update_labels()
        elif new_dec == self.starting_dec:
            # re-enable N/S choice if first
            self.ui.north_south_combo_box.setDisabled(False)
    
    def allow_save(self):
        self.ui.save_button.setEnabled(True)
        self.confirmation_requested = True

    def update_labels(self):
        self.ui.set_dec_value.setText(str(self.current_dec) + "°")

        self.ui.north_south_combo_box.setEnabled(
            self.current_dec == self.starting_dec
        )

        # if all values are filled, enable the save button
        self.ui.save_button.setEnabled(all([val is not None for val in self.data.values()]))

        dec_range = self.get_dec_range()
        degree_values_string = ""
        for dec in dec_range:
            degree_values_string += (("-> " if dec == self.current_dec else "") + str(dec) + "\n")
        self.ui.degree_values_label.setText(degree_values_string)
        data_string = ""
        for dec in dec_range:
            data_string += (
                f"{self.data[dec]:.2f}"
                if self.data[dec] is not None
                else ""
            ) + '\n'
        self.ui.input_data_label.setText(data_string)
