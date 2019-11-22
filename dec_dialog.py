from PyQt5 import QtCore, QtWidgets, QtGui, QtChart
from dec_ui import Ui_Dialog     # compiled PyQt dialogue ui
import time
from precious import MyPrecious

class DecDialog(QtWidgets.QDialog):
    """New observation dialogue window"""
    
    start_dec  = 0
    end_dec    = 90
    
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Calibrate declination")
        
        self.data = []
        self.current_dec = self.start_dec

        # connect buttons
        self.ui.discard_cal_button.clicked.connect(self.handle_discard)
        self.ui.next_cal_button.clicked.connect(self.handle_next)

    def handle_next(self):
        
        if current_dec > end_dec:
            open("dec_cal.txt", "w").close()
            f = open("dec_cal.txt", "a")
            for line in self.data:
                f.write(line + '\m')
        else:
            self.ui.set_dec_value.text(str(current_dec))
            
        
    def handle_discard(self):
        self.close()