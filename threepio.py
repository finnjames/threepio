r"""
  __  __                    _
 / /_/ /  _______ ___ ___  (_)__    ___  __ __
/ __/ _ \/ __/ -_) -_) _ \/ / _ \_ / _ \/ // /
\__/_//_/_/  \__/\__/ .__/_/\___(_) .__/\_, /
                   /_/           /_/   /___/

The helpful companion to the 40' telescope
Written with frustration by Shengjie, Isabel, and Finn

"""

import time

from PyQt5 import QtChart, QtCore, QtGui, QtWidgets

from dialogs import AlertDialog, CreditsDialog, DecDialog, ObsDialog, RADialog
from layouts import threepio_ui
from tools import Comm, DataPoint, Survey, Scan, Spectrum, SuperClock, Tars


# from playsound import playsound # TODO: test on Windows

class Threepio(QtWidgets.QMainWindow):
    """Main class for the app"""

    # basic time
    timer_rate = 10  # ms
    # how many data points to draw to stripchart
    stripchart_display_seconds = 8
    stripchart_offset = 0

    # test data
    ticker = 0
    other_ticker = 0
    foo = 0.0

    # speed measurement
    tick_time = 0.0
    timing_margin = 0.995

    # stripchart
    stripchart_low = -1
    stripchart_high = 1

    # declination calibration arrays
    x = []
    y = []

    # palette
    BLUE = 0x2196f3
    RED = 0xff5252

    # tars communication interpretation
    transmission = None
    old_transmission = None

    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        # use main_ui for window setup
        self.ui = threepio_ui.Ui_MainWindow()
        self.setStyleSheet(open('stylesheet.qss').read())
        self.ui.setupUi(self)
        self.setWindowTitle("Threepio")

        # hide the close/minimize/fullscreen buttons
        self.setWindowFlags(QtCore.Qt.Window |
                            QtCore.Qt.WindowTitleHint |
                            QtCore.Qt.CustomizeWindowHint)

        # connect buttons
        self.ui.stripchart_speed_slider.valueChanged.connect(self.update_speed)
        # self.ui.speed_slower_radio.clicked.connect(self.update_speed)
        # self.ui.speed_default_radio.clicked.connect(self.update_speed)

        self.ui.actionInfo.triggered.connect(self.handle_credits)

        self.ui.actionScan.triggered.connect(self.handle_scan)
        self.ui.actionSurvey.triggered.connect(self.handle_survey)
        self.ui.actionSpectrum.triggered.connect(self.handle_spectrum)

        self.ui.actionDec.triggered.connect(self.dec_calibration)
        self.ui.actionRA.triggered.connect(self.ra_calibration)

        self.ui.chart_clear_button.clicked.connect(self.handle_clear)

        self.ui.chart_legacy_button.clicked.connect(self.legacy_mode)

        # initialize stripchart
        self.stripchart_series_a = QtChart.QLineSeries()
        self.stripchart_series_b = QtChart.QLineSeries()
        self.ui.stripchart.setRenderHint(QtGui.QPainter.Antialiasing)
        pen = QtGui.QPen(QtGui.QColor(self.BLUE))
        pen.setWidth(1)
        self.stripchart_series_a.setPen(pen)
        pen.setColor(QtGui.QColor(self.RED))
        self.stripchart_series_b.setPen(pen)

        self.update_speed()

        # DATAQ stuff
        self.tars = Tars()
        self.tars.setup()
        self.tars.start()

        # clock
        self.clock = None
        self.set_time()

        # establish observation
        self.observation = None

        # establish data array & most recent dec
        self.data = []
        self.current_dec = 0.0

        # run initial calibration
        self.load_dec_cal()

        # refresh timer
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.tick)  # do everything
        self.timer.start(self.timer_rate)  # set refresh rate

    def tick(self):  # primary controller for each clock tick

        # TODO: make this use DAQ data
        self.foo += .1
        if self.foo > 90.0:
            self.foo = 0.0

        # for speed testing

        self.update_gui()  # update gui

        # print(time.time() - self.tick_time)

        # TODO: make this a little less redundant

        if self.observation is None:

            period = self.timer_rate * 0.001

            if (time.time() - self.tick_time) > (period * self.timing_margin):
                self.tick_time = time.time()

                tars_data = self.tars.read_latest()  # get data from DAQ

                self.current_dec = self.calculate_declination(tars_data[2][1])
                data_point = DataPoint(self.clock.get_sidereal_seconds(), self.current_dec, tars_data[0][1],
                                       tars_data[1][1])

                self.data.append(data_point)

                self.update_strip_chart()  # make the stripchart scroll

        else:

            # can't reset RA/Dec after loading obs
            self.ui.actionRA.setEnabled(False)
            self.ui.actionDec.setEnabled(False)

            period = 1 / self.observation.freq

            if (time.time() - self.tick_time) > (period * self.timing_margin):

                self.tick_time = time.time()

                tars_data = self.tars.read_latest()  # get data from DAQ

                self.current_dec = self.calculate_declination(tars_data[2][1])
                data_point = DataPoint(self.clock.get_sidereal_seconds(), self.current_dec, tars_data[0][1],
                                       tars_data[1][1])

                self.data.append(data_point)
                self.old_transmission = self.transmission
                self.transmission = self.observation.communicate(
                    data_point, time.time())
                # print(self.transmission, time.time(), self.observation.state)

                self.update_strip_chart()  # make the stripchart scroll

                if self.transmission != self.old_transmission:
                    if self.transmission == Comm.START_CAL:
                        self.alert("Set calibration switches to ON")
                        self.alert("Are the calibration switches on?")
                        self.observation.next()
                        self.message("Taking calibration data...")
                    elif self.transmission == Comm.STOP_CAL:
                        self.alert("Set calibration switches to OFF")
                        self.alert("Are the calibration switches off?")
                        self.observation.next()
                        self.message("Taking background data...")
                    elif self.transmission == Comm.NEXT:
                        self.observation.next()
                    elif self.transmission == Comm.FINISHED:
                        self.observation.next()
                        self.message("Finished.")
                    elif self.transmission == Comm.BEEP:
                        self.beep()
                    elif self.transmission == Comm.NO_ACTION:
                        pass

                time_until_start = self.observation.start_RA - time.time()
                if time_until_start <= 0 and (self.observation.end_RA - time.time()) > 0:
                    self.message("Taking observation data...")

    def legacy_mode(self):
        """lol"""
        f = open("stylesheet.qss", "w")
        f.write("background-color:#00ff00; color: #ff0000")
        self.setStyleSheet("background-color:#00ff00; color: #ff0000")
        self.setAutoFillBackground(True)

    def handle_credits(self):
        dialog = CreditsDialog()
        dialog.show()
        dialog.exec_()

    def set_time(self):
        if self.clock is None:
            new_clock = SuperClock()
        else:
            new_clock = self.clock

        # TODO: abstract this better
        dialog = RADialog(new_clock)
        dialog.show()
        dialog.exec_()

        self.clock = new_clock

    def update_speed(self):
        self.stripchart_display_seconds = (120 / 6) * (6 - ((6.5 / 6) * self.ui.stripchart_speed_slider.value()))

    def update_gui(self):
        self.ui.ra_value.setText(self.clock.get_sidereal_time())  # show RA
        self.ui.dec_value.setText(
            "%.2f" % self.calculate_declination(self.current_dec))  # show dec
        self.update_progress_bar()

        if len(self.data) > 0:
            self.ui.channelA_value.setText(
                "%.2f" % self.data[len(self.data) - 1].a)
            self.ui.channelB_value.setText(
                "%.2f" % self.data[len(self.data) - 1].b)

    def update_progress_bar(self):
        # this mess makes the progress bar display "T+/- XX.XX" when
        # assigned, and progress the bar when taking data
        if self.observation is not None:
            if not self.observation.end_RA - self.observation.start_RA <= 1:
                if self.clock.get_time_until(self.observation.start_RA) > 0 and self.clock.get_time_until(
                        self.observation.end_RA) < 0:
                    self.ui.progressBar.setValue(int((self.clock.get_time_until(self.observation.end_RA) / (
                            self.observation.end_RA - self.observation.start_RA)) * 100 % 100))
                else:
                    self.ui.progressBar.setValue(0)
                self.ui.progressBar.setFormat(
                    "T%+.1fs" % (self.clock.get_time_until(self.observation.start_RA)))
                return
        self.ui.progressBar.setFormat("n/a")
        self.ui.progressBar.setValue(0)

    def display_info(self, message):
        self.ui.message_label.setText(message)

    def update_strip_chart(self):
        new_a = self.data[len(self.data) - 1].a
        new_b = self.data[len(self.data) - 1].b
        new_ra = self.data[len(self.data) - 1].timestamp
        self.stripchart_series_a.append(new_a, new_ra)
        self.stripchart_series_b.append(new_b, new_ra)

        # while self.stripchart_display_ticks < len(self.data) - self.stripchart_offset:
        #     self.stripchart_series_a.remove(0)
        #     self.stripchart_series_b.remove(0)
        #     self.stripchart_offset += 1

        # add channels to chart
        chart = QtChart.QChart()
        chart.addSeries(self.stripchart_series_b)
        chart.addSeries(self.stripchart_series_a)

        # create and scale y axis
        axis_y = QtChart.QValueAxis()
        axis_y.setRange(
            self.clock.get_sidereal_seconds() - self.stripchart_display_seconds, self.clock.get_sidereal_seconds())
        axis_y.setVisible(False)
        chart.setAxisY(axis_y)

        self.stripchart_series_a.attachAxis(axis_y)
        self.stripchart_series_b.attachAxis(axis_y)

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
        dialog = ObsDialog(
            self, obs, self.clock)
        dialog.setWindowTitle("New " + obs.obs_type)
        dialog.show()
        dialog.exec_()

    def dec_calibration(self):
        dialog = DecDialog(self.tars)
        dialog.show()
        dialog.exec_()

        self.load_dec_cal()

    def load_dec_cal(self):
        # create y array
        i = DecDialog.start_dec
        while i <= DecDialog.end_dec:
            self.y.append(float(i))
            i += DecDialog.step

        # create x array
        c = open("dec_cal.txt", 'r').read().splitlines()  # get data from file
        for i in c:
            self.x.append(float(i))

    def calculate_declination(self, input_dec):
        """calculate the true dec from declinometer input data and calibration data"""

        # input is below data
        if input_dec < self.x[0]:  # TODO: use minimum, not first
            return ((self.y[1] - self.y[0]) / (self.x[1] - self.x[0]) * (input_dec - self.x[0])) + self.y[0]

        # input is above data
        if input_dec > self.x[-1]:  # TODO: use maximum, not last
            return ((self.y[-1] - self.y[-2]) / (self.x[-1] - self.x[-2]) * (input_dec - self.x[-1])) + self.y[-1]

        # input is within data
        for i in range(len(self.x)):
            if input_dec <= self.x[i + 1]:
                if input_dec >= self.x[i]:
                    # (Δy/Δx)x + y_0
                    return ((self.y[i + 1] - self.y[i]) / (self.x[i + 1] - self.x[i]) * (input_dec - self.x[i])) + \
                           self.y[i]

    def ra_calibration(self):
        self.set_time()

    def message(self, message):
        self.ui.message_label.setText(message)

    def alert(self, message):
        alert = AlertDialog(message)
        alert.show()
        alert.exec_()

    def beep(self):
        print("beep! ", time.time())


def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    window = Threepio()
    window.setMinimumSize(800, 600)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
