from PyQt5 import QtCore, QtWidgets, QtGui, QtChart
from credits_ui import Ui_Dialog     # compiled PyQt dialogue ui

class CreditsDialog(QtWidgets.QDialog):
    """Credits dialogue window"""
    
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Credits")

        # connect okay button
        # self.ui.clo.accepted.connect(self.handle_close)

    def handle_ok(self):
        pass