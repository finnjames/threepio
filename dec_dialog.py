from PyQt5 import QtCore, QtWidgets, QtGui, QtChart
from dec_ui import Ui_Dialog     # compiled PyQt dialogue ui
import random

class DecDialog(QtWidgets.QDialog):
    """New observation dialogue window"""
    
    start_dec  = 0
    end_dec    = 90
    step       = 5
    
    def __init__(self, tars):
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Calibrate declination")
        
        self.data = []
        self.current_dec = self.start_dec
        self.ui.set_dec_value.setText(str(self.current_dec))
        
        self.tars = tars

        # connect buttons
        self.ui.discard_cal_button.clicked.connect(self.handle_discard)
        self.ui.next_cal_button.clicked.connect(self.handle_next)
        
        self.handle_next()

    def handle_next(self):
        if self.current_dec > self.end_dec: # base case, calibration complete
            open("dec_cal.txt", "w").close() # overwrite file
            f = open("dec_cal.txt", "a")
            for line in self.data: # replace with new calibration data
                f.write(str(line) + '\n')
            self.close()
        else:
            self.data.append(self.current_dec + random.randint(-2, 2)) # TODO: read data from declinometer
            self.ui.set_dec_value.setText(str(self.current_dec))
            self.current_dec += self.step
        
    def handle_discard(self):
        self.close()