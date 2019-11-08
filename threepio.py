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
from main_ui import Ui_MainWindow   # compiled PyQt main ui
from dialog_ui import Ui_Dialog     # compiled PyQt dialogue ui
from astropy.time import Time
# from playsound import playsound # TODO: test on Windows 
import numpy as np
import time, math, random

import tars
from precious import MyPrecious
from dialog import Dialog
from superclock import SuperClock
from observation import Observation, Survey, Scan, Spectrum, DataPoint
        
class Threepio(QtWidgets.QMainWindow):
    """Main class for the app"""

    # basic time
    timer_rate = 10 # ms
    stripchart_display_ticks = 2048 # how many data points to draw to stripchart
    stripchart_offset = 0

    # test data
    ticker = 0
    other_ticker = 0

    # stripchart
    stripchart_low = -1
    stripchart_high = 1

    # palette
    BLUE = 0x2196f3
    RED = 0xff5252

    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        # use main_ui for window setup
        self.ui = Ui_MainWindow()
        self.setStyleSheet(open('stylesheet.qss').read())
        self.ui.setupUi(self)
        self.setWindowTitle("Threepio")

        # connect buttons
        self.ui.speed_faster_radio.clicked.connect(self.update_speed)
        self.ui.speed_slower_radio.clicked.connect(self.update_speed)
        self.ui.speed_default_radio.clicked.connect(self.update_speed)

        self.ui.actionScan.triggered.connect(self.handle_scan)
        self.ui.actionSurvey.triggered.connect(self.handle_survey)
        self.ui.actionSpectrum.triggered.connect(self.handle_spectrum)

        self.ui.chart_clear_button.clicked.connect(self.handle_clear)
        # self.ui.chart_refresh_button.clicked.connect(self.handle_refresh)
        # this is for testing, the above line is the correct one
        self.ui.chart_refresh_button.clicked.connect(self.handle_scan)

        # TODO: maybe just choose one of these?
        self.ui.actionLegacy.triggered.connect(self.legacy_mode)
        self.ui.chart_legacy_button.clicked.connect(self.legacy_mode)

        # initialize stripchart
        self.stripchart_series_a = QtChart.QLineSeries()
        self.stripchart_series_b = QtChart.QLineSeries()
        self.ui.stripchart.setRenderHint(QtGui.QPainter.Antialiasing)

        # make the charts m a t e r i a l (blue and red)
        pen = QtGui.QPen(QtGui.QColor(self.BLUE))
        pen.setWidth(3)
        self.stripchart_series_a.setPen(pen)
        pen.setColor(QtGui.QColor(self.RED))
        self.stripchart_series_b.setPen(pen)

        # # DATAQ stuff
        # self.tars = tars.Tars(tars.discovery())
        # self.tars.init()
        # self.tars.start()
        
        #  clock
        self.clock = SuperClock()
        
        # blank obs
        self.observation = Observation()
        
        # refresh timer
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.tick) # do everything
        self.timer.start(self.timer_rate) # set refresh rate

    def tick(self): # primary controller for each clock tick

        self.update_gui() # update gui

        self.ticker += random.random()*random.randint(-1,1)       # \ for the test data
        self.other_ticker += random.random()*random.randint(-1,1) # /
        self.observation.add_data(DataPoint(self.clock.get_time(), self.ticker, self.other_ticker, 1)) # random meander

        # self.observation.add_data(self.tars.read_one(1)) # get data from DAQ
        
        self.update_strip_chart() # make the stripchart scroll
        
    def legacy_mode(self):
        f = open("stylesheet.qss", "w")
        f.write("background-color:#00ff00; color: #ff0000")
        self.setStyleSheet("background-color:#00ff00; color: #ff0000")
        self.setAutoFillBackground( True )

    def update_speed(self):
        if (self.ui.speed_faster_radio.isChecked()):
            self.stripchart_display_ticks = 512
        elif (self.ui.speed_slower_radio.isChecked()):
            self.stripchart_display_ticks = 3072
        else:
            self.stripchart_display_ticks = 2048
        self.handle_clear()

    def update_gui(self):
        self.ui.ra_value.setText(self.clock.get_sidereal_time() + "UTC")
        
        # TODO: get data from declinometer
        self.ui.dec_value.setText(str(self.observation.start_dec) + "deg")
        
        if len(self.observation.data) > 0:
            self.ui.channelA_value.setText("%.2f" % (self.observation.data[len(self.observation.data) - 1].a))
            self.ui.channelB_value.setText("%.2f" % (self.observation.data[len(self.observation.data) - 1].b))
        
        # this mess makes the progress bar display "T+/- XX.XX" when
        # assigned, and progress the bar when taking data
        if not self.observation.end_RA - self.observation.start_RA <= 1:
            if self.clock.get_time_until(self.observation.start_RA) > 0 and self.clock.get_time_until(self.observation.end_RA) < 0:
                self.ui.progressBar.setValue(int((self.clock.get_time_until(self.observation.end_RA) / (self.observation.end_RA - self.observation.start_RA)) * 100 % 100))
            else:
                self.ui.progressBar.setValue(0)
            self.ui.progressBar.setFormat("T%+.1fs" % (self.clock.get_time_until(self.observation.start_RA)))
        else:
            self.ui.progressBar.setFormat("n/a")
            self.ui.progressBar.setValue(0)
    
    def update_strip_chart(self):
        new_a = self.observation.data[len(self.observation.data) - 1].a
        new_b = self.observation.data[len(self.observation.data) - 1].b
        self.stripchart_series_a.append(new_a, len(self.observation.data))
        self.stripchart_series_b.append(new_b, len(self.observation.data))

        while (len(self.observation.data) - self.stripchart_offset > self.stripchart_display_ticks):
            self.stripchart_series_a.remove(0)
            self.stripchart_series_b.remove(0)
            self.stripchart_offset += 1

        # TODO: make the stripchart fill in old data when slowed down

        chart = QtChart.QChart()
        chart.addSeries(self.stripchart_series_a)
        chart.addSeries(self.stripchart_series_b)
        
        
        axisX = QtChart.QValueAxis()

        if (new_a < new_b):
            if (new_a < self.stripchart_low):
                self.stripchart_low = new_a
            if (new_b > self.stripchart_high):
                self.stripchart_high = new_b
        else:
            if (new_b < self.stripchart_low):
                self.stripchart_low = new_b
            if (new_a > self.stripchart_high):
                self.stripchart_high = new_a
                
        axisX.setRange(self.stripchart_low, self.stripchart_high)
        
        # axisX.setLabelFormat("%g")
        chart.setAxisX(axisX)

        self.stripchart_series_a.attachAxis(axisX)
        self.stripchart_series_b.attachAxis(axisX)
        
        # chart.createDefaultAxes()
        chart.legend().hide()

        self.ui.stripchart.setChart(chart)
        
    def handle_clear(self):
        self.stripchart_offset += self.stripchart_series_a.count()
        self.stripchart_series_a.clear()
        self.stripchart_series_b.clear()
    
    def handle_refresh(self):
        self.stripchart_low = 32767
        self.stripchart_high = -32768

    def handle_survey(self):
        obs = Survey()
        self.new_observation(obs)

    def handle_scan(self):
        obs = Scan()
        self.new_observation(obs)

    def handle_spectrum(self):
        obs = Spectrum()
        self.new_observation(obs)

    def new_observation(self, obs):
        dialog = Dialog(self, self.clock.get_time(), obs)
        dialog.setWindowTitle("New " + obs.obs_type)
        dialog.show()
        dialog.exec_()


def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    window = Threepio()
    window.setMinimumSize(800,600)
    window.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()