"""
  __  __                    _                 
 / /_/ /  _______ ___ ___  (_)__    ___  __ __
/ __/ _ \/ __/ -_) -_) _ \/ / _ \_ / _ \/ // /
\__/_//_/_/  \__/\__/ .__/_/\___(_) .__/\_, / 
                   /_/           /_/   /___/  

The helpful companion to the 40' telescope
Written with frustration by Shengjie, Isabel, and Finn

"""


from PyQt5 import QtCore, QtWidgets, QtGui, QtChart
from main_ui import Ui_MainWindow  # compiled PyQt main ui
from dialog_ui import Ui_Dialog    # compiled PyQt dialogue ui
import time, math, random

import tars

class Dialog(QtWidgets.QDialog):
    """New observation dialogue window"""
    def __init__(self, parent_window):
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Threepio Dialogue")

        # get the window that spawned it
        self.parent_window = parent_window

        # what to do when press "ok"
        self.ui.dialog_button_box.clicked.connect(self.handle_ok)

    def handle_ok(self):
        # TODO: convert input to epoch time properly (not just assume everything is Jan 1 1970)
        pattern = "%H:%M:%S"
        start = int(time.mktime(time.strptime(self.ui.start_value.text(), pattern)))
        end = int(time.mktime(time.strptime(self.ui.end_value.text(), pattern)))

        self.parent_window.setRA(start, end)

class SuperClock():
    """Clock object for encapsulation; keeps track of the time"""
    def __init__(self, starting_time = time.time()):
        self.starting_time = starting_time
    
    def get_time(self):
        return time.time()

    def get_elapsed_time(self):
        return time.time() - self.starting_time

class Threepio(QtWidgets.QMainWindow):
    """Main class for the app"""

    # basic time values; generally, default to milliseconds
    start_RA = 0 # ms
    end_RA = 0 # ms
    elapsed_time = 0 # ms
    timer_rate = 20 # ms
    stripchart_display_ticks = 300 # how many data points to draw to stripchart


    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        # use main_ui for window setup
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Threepio")

        # connect buttons
        self.ui.chart_clear_button.clicked.connect(self.handle_scan)
        self.ui.speed_faster_radio.clicked.connect(self.update_speed)
        self.ui.speed_slower_radio.clicked.connect(self.update_speed)
        self.ui.speed_default_radio.clicked.connect(self.update_speed)

        # time
        self.clock = SuperClock()

        # store data in... an array
        # TODO: make this less terrible (at least delegate or something)
        self.data = []

        # initialize stripchart
        self.stripchart_series = QtChart.QLineSeries()
        for i in range(self.stripchart_display_ticks): # make line of zeros at start
            self.data.append(0)
        chart = QtChart.QChart()
        chart.addSeries(self.stripchart_series)
        chart.legend().hide()
        self.ui.stripchart.setChart(chart)
        self.ui.stripchart.setRenderHint(QtGui.QPainter.Antialiasing)

        # DATAQ stuff
        self.tars = tars.Tars(tars.discovery())
        self.tars.init()
        self.tars.start()


        # timer for... everything
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.tick) # do everything
        self.timer.start(self.timer_rate)

    def tick(self): # primary controller for each clock tick
        self.elapsed_time += self.timer_rate # 
        self.update_gui()
        # self.data.append(int(((math.sin((self.elapsed_time / (200 * math.pi)))*300)**2))) # pretty sine wave

        self.data.append(self.tars.read_one(1))

        # make the stripchart scroll

        self.update_strip_chart()

    def add_data(self, data):
        self.data.append(data)

    # def get_elapsed_time(self):
    #     return self.clock.get_time()

    def update_speed(self):
        if (self.ui.speed_faster_radio.isChecked()):
            self.stripchart_display_ticks = 200
        elif (self.ui.speed_slower_radio.isChecked()):
            self.stripchart_display_ticks = 600
        else:
            self.stripchart_display_ticks = 400

    def set_ra(self, start_RA, end_RA):
        self.start_RA = start_RA
        self.end_RA = end_RA
        print(start_RA, end_RA)

    def update_gui(self): # TODO: make this display in human time
        current_time = str(round(self.start_RA + self.clock.get_elapsed_time(), 2))
        self.ui.ra_value.setText("T+" + current_time + "ms")
        # TODO: get data from declinometer

    def new_observation(self, observation_type):
        if (observation_type):
            print(observation_type)
        else:
            print("no type")

    def handle_scan(self):
        dialog = Dialog(self)
        dialog.show()
        dialog.exec_()
    
    def update_strip_chart(self):

        self.stripchart_series.clear()

        if (len(self.data) >= self.stripchart_display_ticks): # ticks
            for i in range(self.stripchart_display_ticks):
                self.stripchart_series.append(self.data[len(self.data) - self.stripchart_display_ticks + i], i)
        else:
            for i in range(len(self.data)):
                self.stripchart_series.append(self.data[i], i)

        chart = QtChart.QChart()
        chart.addSeries(self.stripchart_series)
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