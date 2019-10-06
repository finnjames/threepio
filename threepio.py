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
        # TODO: convert input to epoch time properly (not just assume everything is Jan 1 1970)
        pattern = "%H:%M:%S"
        start = int(time.mktime(time.strptime(self.ui.start_value.text(), pattern)))
        end = int(time.mktime(time.strptime(self.ui.end_value.text(), pattern)))

        self.parent_window.setRA(start, end)

class Threepio(QtWidgets.QMainWindow): # whole app class
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        # use main_ui for window setup
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Threepio")

        # chart clear button runs handleScan
        self.ui.chart_clear_button.clicked.connect(self.handleScan)

        # basic time values
        self.start_RA = 0
        self.end_RA = 0
        self.elapsed_time = 0 # ms
        self.timer_rate = 10 # ms
        self.stripchart_display_ticks = 256 # how many data points to draw to stripchart

        # store data in... an array
        # TODO: make this less terrible
        self.data = []

        # initialize stripchart
        self.stripchart_series = QtChart.QLineSeries()
        for i in range(self.stripchart_display_ticks):
            self.data.append(0)

        chart = QtChart.QChart()
        chart.addSeries(self.stripchart_series)
        # chart.createDefaultAxes()
        chart.legend().hide()

        self.ui.stripchart.setChart(chart)
        self.ui.stripchart.setRenderHint(QtGui.QPainter.Antialiasing)

        # timer for... everything
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.tick) # do everything
        self.timer.start(self.timer_rate)

    def tick(self): # primary controller for each clock tick
        self.elapsed_time += self.timer_rate
        self.handleHello()
        self.data.append(int(((math.sin((self.elapsed_time / (100 * math.pi)))*10)**2)))

        # make the stripchart scroll
        self.stripchart_series.clear()
        if (len(self.data) >= self.stripchart_display_ticks): # ticks
            for i in range(self.stripchart_display_ticks):
                self.stripchart_series.append(self.data[len(self.data) - self.stripchart_display_ticks + i], i)
        else:
            for i in range(len(self.data)):
                self.stripchart_series.append(self.data[i], i)

        self.updateStripChart(self.stripchart_series)

    def addData(self, data):
        self.data.append(data)


    def setRA(self, start_RA, end_RA):
        self.start_RA = start_RA
        self.end_RA = end_RA
        print(start_RA, end_RA)

    def handleHello(self): # TODO: make this display in human time
        self.ui.ra_value.setText("T+" + str(round(self.start_RA + self.elapsed_time, 2)) + "ms")

    def newObservation(self, observation_type):
        if (observation_type):
            print(observation_type)
        else:
            print("no type")

    def handleScan(self):
        dialog = Dialog(self)
        dialog.show()
        dialog.exec_()
    
    def updateStripChart(self, series): # updates chart based on passed series

        chart = QtChart.QChart()
        chart.addSeries(series)
        # chart.createDefaultAxes()
        chart.legend().hide()

        self.ui.stripchart.setChart(chart)


if __name__ == '__main__':

    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    window = Threepio()
    window.setMinimumSize(800,600)
    window.show()
    sys.exit(app.exec_())