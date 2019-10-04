from PyQt5 import QtCore, QtWidgets, QtGui, QtChart
from main_ui import Ui_MainWindow  # pre compiled PyQt main ui
from dialog_ui import Ui_Dialog    # pre compiled PyQt dialogue ui
import time, math, random

class Dialog(QtWidgets.QDialog): # new observation dialog
    def __init__(self, parent_window):
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Threepio Dialogue")

        # get the window that spawned it
        self.parent_window = parent_window

        # what to do when press "ok"
        self.ui.dialog_button_box.clicked.connect(self.handleOk)

    def handleOk(self):
        self.parent_window.setRA(self.ui.start_value.text(), self.ui.end_value.text())

class Threepio(QtWidgets.QMainWindow): # whole app class
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        # use main_ui for window setup
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Threepio")

        # make the line chart in the widget
        series = QtChart.QLineSeries()
        for i in range(100):
            series.append((random.random()-0.5)**3, i)

        chart = QtChart.QChart()
        chart.addSeries(series)
        chart.createDefaultAxes()
        chart.legend().hide()

        self.ui.stripchart.setChart(chart)

        # self.ui.stripchart.show()

        # chart clear button runs handleHello
        self.ui.chart_clear_button.clicked.connect(self.handleScan)

        # start/end RA default to 0
        self.start_RA = 0
        self.end_RA = 0

        # timer for... everything
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.handleHello)
        self.timer.start(1000)

    def setRA(self, start_RA, end_RA):
        self.start_RA = start_RA
        self.end_RA = end_RA
        print(start_RA, end_RA)

    def handleHello(self): # TODO: make this go to 1/100ths of a second
        current_time = time.localtime(time.clock_gettime(time.CLOCK_REALTIME))
        self.ui.ra_value.setText(str(current_time[3]) + " : " + str(current_time[4]) + " : " + str(current_time[5]))
        self.ui.progressBar.setValue(current_time[5] / 60 * 100)

    def newObservation(self, observation_type):
        if (observation_type):
            print(observation_type)
        else:
            print("no type")

    def handleScan(self):
        dialog = Dialog(self)
        dialog.show()
        dialog.exec_()


if __name__ == '__main__':

    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    window = Threepio()
    window.show()
    sys.exit(app.exec_())