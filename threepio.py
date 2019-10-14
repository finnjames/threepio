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
import time, math, random

import tars

class Dialog(QtWidgets.QDialog):
    """New observation dialogue window"""
    def __init__(self, parent_window, date):
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Threepio Dialogue")
        
        # set today's date
        self.current_date = QtCore.QDate(time.localtime(date)[0], time.localtime(date)[1], time.localtime(date)[2])
        self.current_time = QtCore.QTime(time.localtime(date)[3], time.localtime(date)[4], 0)
        self.ui.start_time.setDate(self.current_date)
        self.ui.start_time.setTime(self.current_time)
        self.ui.end_time.setDate(self.current_date)
        self.ui.end_time.setTime(self.current_time) 

        # store the window that spawned it
        self.parent_window = parent_window

        # when "ok" pressed
        self.ui.dialog_button_box.accepted.connect(self.handle_ok)

    def handle_ok(self):
        pattern = "%Y.%m.%d %H:%M:%S"
        print(self.ui.start_time.text())
        start = int(time.mktime(time.strptime(self.ui.start_time.text(), pattern)))
        end = int(time.mktime(time.strptime(self.ui.end_time.text(), pattern)))

        self.parent_window.set_ra(start, end)

class SuperClock():
    """Clock object for encapsulation; keeps track of the time"""
    def __init__(self, starting_time = time.time()):
        self.starting_time = starting_time
    
    def get_time(self):
        return time.time()

    def get_elapsed_time(self):
        return time.time() - self.starting_time
    
    def get_time_until(self, destination_time):
        return time.time() - destination_time
    
class DataPoint():
    """each data point taken"""
    def __init__(self, timestamp, a, b):
        self.timestamp = timestamp
        self.a = a
        self.b = b
        

class Threepio(QtWidgets.QMainWindow):
    """Main class for the app"""

    # basic time
    start_RA = 0
    end_RA = 0
    timer_rate = 10 # ms
    stripchart_display_ticks = 2048 # how many data points to draw to stripchart
    stripchart_offset = 0

    # test data
    ticker = 0
    other_ticker = 0
    
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
        self.ui.chart_refresh_button.clicked.connect(self.handle_scan)

        self.ui.actionLegacy.triggered.connect(self.legacy_mode)

        # init data array
        self.data = []

        # initialize stripchart
        self.stripchart_series_a = QtChart.QLineSeries()
        self.stripchart_series_b = QtChart.QLineSeries()
        self.ui.stripchart.setRenderHint(QtGui.QPainter.Antialiasing)
        pen = QtGui.QPen(QtGui.QColor(self.BLUE))
        pen.setWidth(3)
        self.stripchart_series_a.setPen(pen)
        pen.setColor(QtGui.QColor(self.RED))
        self.stripchart_series_b.setPen(pen)

        # DATAQ stuff
        # self.tars = tars.Tars(tars.discovery())
        # self.tars.init()
        # self.tars.start()
        
        #  clock
        self.clock = SuperClock(time.time())
        self.start_RA = time.time()
        self.end_RA = time.time()

        # refresh timer
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.tick) # do everything
        self.timer.start(self.timer_rate) # set refresh rate

    def tick(self): # primary controller for each clock tick

        self.update_gui() # update gui

        # self.data.append(int(((math.sin((self.ticker / (8 * math.pi)))*300)**2))) # pretty sine wave
        self.ticker += random.random()*random.randint(-1,1)       # \ for the test data
        self.other_ticker += random.random()*random.randint(-1,1) # /
        self.data.append(DataPoint(self.clock.get_time(), self.ticker, self.other_ticker)) # random meander

        # self.data.append(self.tars.read_one(1)) # get data from DAQ
        
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

    def set_ra(self, start_RA, end_RA):
        self.start_RA = start_RA
        self.end_RA = end_RA
        print(start_RA, end_RA)

    def update_gui(self):
        self.ui.ra_value.setText("T%+.2fs" % (self.clock.get_time_until(self.start_RA)))
        
        # TODO: get data from declinometer
        if len(self.data) > 0:
            self.ui.channelA_value.setText("%.2f" % (self.data[len(self.data) - 1].a))
            self.ui.channelB_value.setText("%.2f" % (self.data[len(self.data) - 1].b))
        
        if not self.end_RA - self.start_RA <= 1:
            # TODO: make the progress bar always go left to right (even before obs start)
            self.ui.progressBar.setValue(int((self.clock.get_time_until(self.end_RA) / (self.end_RA - self.start_RA)) * 10 % 100))
        else:
            self.ui.progressBar.setValue(0)

    def handle_survey(self):
        self.new_observation("survey")

    def handle_scan(self):
        self.new_observation("scan")

    def handle_spectrum(self):
        self.new_observation("spectrum")

    def new_observation(self, type):
        dialog = Dialog(self, self.clock.get_time())
        dialog.setWindowTitle("New " + type.capitalize())
        dialog.show()
        dialog.exec_()
    
    def update_strip_chart(self):
        self.stripchart_series_a.append(self.data[len(self.data) - 1].a, len(self.data))
        self.stripchart_series_b.append(self.data[len(self.data) - 1].b, len(self.data))

        while (len(self.data) - self.stripchart_offset > self.stripchart_display_ticks):
            # TODO: make this not lag when there's a big delta in display_ticks
            self.stripchart_series_a.remove(0)
            self.stripchart_series_b.remove(0)
            self.stripchart_offset += 1

        # TODO: make the stripchart fill in old data when slowed down

        chart = QtChart.QChart()
        chart.addSeries(self.stripchart_series_a)
        chart.addSeries(self.stripchart_series_b)
        # chart.createDefaultAxes()
        chart.legend().hide()

        self.ui.stripchart.setChart(chart)
        
    def handle_clear(self):
        self.stripchart_offset += self.stripchart_series_a.count()
        self.stripchart_series_a.clear()
        self.stripchart_series_b.clear()


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