from PyQt5 import QtCore, QtWidgets, QtGui
from main_ui import Ui_MainWindow  # pre compiled PyQt main ui
from dialog_ui import Ui_Dialog    # pre compiled PyQt dialogue ui
import time

class Dialog(QtWidgets.QDialog): # new observation dialog
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

class Threepio(QtWidgets.QMainWindow): # whole app class
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.chart_clear_button.clicked.connect(self.handleHello)

        # timer for clock
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.handleHello)
        self.timer.start(1000)

    def handleHello(self):
        current_time = time.localtime(time.clock_gettime(time.CLOCK_REALTIME))
        self.ui.ra_value.setText(str(current_time[3]) + " : " + str(current_time[4]) + " : " + str(current_time[5]))


if __name__ == '__main__':

    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Threepio()
    window.show()
    sys.exit(app.exec_())