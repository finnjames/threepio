from PyQt5 import QtCore, QtWidgets, QtGui, QtChart
from layouts import ra_cal_ui     # compiled PyQt dialogue ui
import time
from precious import MyPrecious

class RADialog(QtWidgets.QDialog):
    """New observation dialogue window"""
    
    def __init__(self, superclock):
        QtWidgets.QWidget.__init__(self)
        self.ui = ra_cal_ui.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Set time")

        # store parent window's superclock
        self.superclock = superclock

        # connect okay button
        self.ui.dialog_button_box.accepted.connect(self.handle_ok)

    def handle_ok(self):
        # pattern = "%H:%M:%S"
                
        u_time = self.ui.sidereal_value.text()
        self.superclock.starting_sidereal_time = 3600*int(u_time[:2]) + 60*int(u_time[3:5]) + int(u_time[6:])
        
        self.superclock.starting_time = time.time()