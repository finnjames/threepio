from PyQt5 import QtCore, QtWidgets, QtGui
from main_ui import Ui_MainWindow # pre compiled PyQt ui
import time

class Threepio(QtWidgets.QMainWindow): # whole app class
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.chart_clear_button.clicked.connect(self.handleHello)

    def handleHello(self):
        self.ui.ra_value.setText(time.gmtime(time.clock_gettime(time.CLOCK_REALTIME)))


if __name__ == '__main__':

    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Threepio()
    window.show()
    sys.exit(app.exec_())