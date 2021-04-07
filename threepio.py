r"""
  __  __                    _
 / /_/ /  _______ ___ ___  (_)__    ___  __ __
/ __/ _ \/ __/ -_) -_) _ \/ / _ \_ / _ \/ // /
\__/_//_/_/  \__/\__/ .__/_/\___(_) .__/\_, /
                   /_/           /_/   /___/

"""

import time
from functools import reduce

from PyQt5 import QtChart, QtCore, QtGui, QtWidgets, QtMultimedia

from dialogs import AlertDialog, CreditsDialog, DecDialog, ObsDialog, RADialog
from layouts import threepio_ui, quit_ui
from tools import Comm, DataPoint, Survey, Scan, Spectrum, SuperClock, Tars


class Threepio(QtWidgets.QMainWindow):
    """main class for the app"""

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
    BLUE = 0x2196F3
    RED = 0xFF5252

    # green bank coords
    GB_LAT = 38.4339

    # tars communication interpretation
    transmission = None
    old_transmission = None

    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        # use main_ui for window setup
        self.ui = threepio_ui.Ui_MainWindow()
        self.setStyleSheet(open("stylesheet.qss").read())
        self.ui.setupUi(self)
        self.setWindowTitle("threepio")

        # hide the close/minimize/fullscreen buttons
        self.setWindowFlags(
            QtCore.Qt.Window | QtCore.Qt.WindowTitleHint | QtCore.Qt.CustomizeWindowHint
        )

        # "console" output
        self.message_log = ["Starting threepio..."]
        self.update_console()

        # initialize stripchart
        self.log("Initializing stripchart...")
        self.stripchart_series_a = QtChart.QLineSeries()
        self.stripchart_series_b = QtChart.QLineSeries()
        # self.stripchart_series_a.setUseOpenGL(True)
        # self.stripchart_series_b.setUseOpenGL(True)
        self.axis_y = QtChart.QValueAxis()
        self.chart = QtChart.QChart()
        # comment this for better performance
        # self.ui.stripchart.setRenderHint(QtGui.QPainter.Antialiasing)
        pen = QtGui.QPen(QtGui.QColor(self.BLUE))
        pen.setWidth(1)
        self.stripchart_series_a.setPen(pen)
        pen.setColor(QtGui.QColor(self.RED))
        self.stripchart_series_b.setPen(pen)
        self.initialize_stripchart()

        self.update_speed()

        # connect buttons
        self.ui.stripchart_speed_slider.valueChanged.connect(self.update_speed)

        self.ui.actionInfo.triggered.connect(self.handle_credits)

        self.ui.actionScan.triggered.connect(self.handle_scan)
        self.ui.actionSurvey.triggered.connect(self.handle_survey)
        self.ui.actionSpectrum.triggered.connect(self.handle_spectrum)

        self.ui.actionDec.triggered.connect(self.dec_calibration)
        self.ui.actionRA.triggered.connect(self.ra_calibration)

        self.ui.actionNormal.triggered.connect(self.set_state_normal)
        self.ui.actionTesting.triggered.connect(self.set_state_testing)
        self.ui.actionLegacy.triggered.connect(self.legacy_mode)

        self.ui.chart_clear_button.clicked.connect(self.clear_stripchart)

        self.ui.chart_legacy_button.clicked.connect(self.legacy_mode)

        self.log("Initializing buttons...")

        # Tars/DATAQ stuff
        self.tars = Tars(parent=self)
        self.tars.setup()
        self.tars.start()

        # clock
        self.clock = None
        self.set_time()

        # bleeps and bloops
        self.log("Initializing audio...")
        self.click_sound = QtMultimedia.QSoundEffect()
        url = QtCore.QUrl()
        self.click_sound.setSource(url.fromLocalFile("assets/beep3.wav"))
        self.click_sound.setVolume(0.5)
        # self.click_sound.play()
        self.last_beep_time = 0.0

        # establish observation
        self.log("Initializing observation...")
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

        # used for measuring refresh rate
        self.time_since_last_tick = 0
        self.time_of_last_tick = self.clock.get_time()
        self.time_of_last_refresh_update = self.time_of_last_tick

        # testing QGraphicsView TODO: move this into its own method
        self.dec_scene = QtWidgets.QGraphicsScene()
        self.ui.dec_view.setScene(self.dec_scene)
        self.update_dec_view()
        self.ticker = 1

    def tick(self):  # primary controller for each clock tick

        self.update_gui()  # update gui

        current_time = self.clock.get_time()
        self.time_since_last_tick = current_time - self.time_of_last_tick
        self.time_of_last_tick = current_time

        # TODO: make this a little less redundant

        if self.observation is None:

            period = self.timer_rate * 0.001  # s -> ms

            if (time.time() - self.tick_time) > (period * self.timing_margin):
                self.tick_time = time.time()

                tars_data = self.tars.read_latest()  # get data from DAQ

                self.current_dec = self.calculate_declination(tars_data[2][1])
                data_point = DataPoint(
                    self.clock.get_sidereal_seconds(),
                    self.current_dec,
                    tars_data[0][1],
                    tars_data[1][1],
                )

                self.data.append(data_point)

                self.update_stripchart()  # make the stripchart scroll

        else:

            # can't reset RA/Dec after loading obs
            self.ui.actionRA.setDisabled(True)
            self.ui.actionDec.setDisabled(True)
            self.ui.menuNew.setDisabled(True)

            period = 1 / self.observation.freq

            if (time.time() - self.tick_time) > (period * self.timing_margin):

                self.tick_time = time.time()

                tars_data = self.tars.read_latest()  # get data from DAQ

                self.current_dec = self.calculate_declination(tars_data[2][1])
                data_point = DataPoint(
                    self.clock.get_sidereal_seconds(),
                    self.current_dec,
                    tars_data[0][1],
                    tars_data[1][1],
                )

                self.data.append(data_point)
                self.old_transmission = self.transmission
                self.transmission = self.observation.communicate(
                    data_point, time.time()
                )

                self.update_stripchart()  # make the stripchart scroll

                # This is a mess, but I think it should be fine for now
                if self.transmission == Comm.START_CAL:
                    self.alert("Set calibration switches to ON", "Okay")
                    self.alert("Are the calibration switches on?", "Yes")
                    self.observation.next()
                    self.message("Taking calibration data...")
                elif self.transmission == Comm.STOP_CAL:
                    self.alert("Set calibration switches to OFF", "Okay")
                    self.alert("Are the calibration switches off?", "Yes")
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
                if time_until_start <= 0 < (self.observation.end_RA - time.time()):
                    self.message("Taking observation data...")

    def set_state_normal(self):
        self.ui.actionNormal.setChecked(True)
        self.ui.actionTesting.setChecked(False)
        self.ui.testing_frame.hide()

    def set_state_testing(self):
        self.ui.actionNormal.setChecked(False)
        self.ui.actionTesting.setChecked(True)
        self.ui.testing_frame.show()

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
        dialog = RADialog(self, new_clock)
        dialog.show()
        dialog.exec_()

        self.clock = new_clock

    def update_speed(self):
        self.stripchart_display_seconds = 120 - (
            (110 / 6) * self.ui.stripchart_speed_slider.value()
        )

    def update_gui(self):
        self.ui.ra_value.setText(self.clock.get_sidereal_time())  # show RA
        self.ui.dec_value.setText("%.2f" % self.current_dec)  # show dec
        self.update_progress_bar()

        self.update_dec_view()
        self.update_console()

        if len(self.data) > 0:
            self.ui.channelA_value.setText("%.2f" % self.data[len(self.data) - 1].a)
            self.ui.channelB_value.setText("%.2f" % self.data[len(self.data) - 1].b)

        current_time = self.clock.get_time()
        if current_time - self.time_of_last_refresh_update > 1:
            self.ui.refresh_value.setText("%06.2fHz" % self.get_refresh_rate())
            self.time_of_last_refresh_update = current_time

    def update_progress_bar(self):
        """updates the progress bar"""
        # this mess makes the progress bar display "T+/- XX.XX" when
        # assigned, and progress the bar when taking data
        if self.observation is not None:
            if not self.observation.end_RA - self.observation.start_RA <= 1:
                if (
                    self.clock.get_time_until(self.observation.start_RA)
                    > 0
                    > self.clock.get_time_until(self.observation.end_RA)
                ):
                    self.ui.progressBar.setValue(
                        int(
                            (
                                self.clock.get_time_until(self.observation.end_RA)
                                / (self.observation.end_RA - self.observation.start_RA)
                            )
                            * 100
                            % 100
                        )
                    )
                else:
                    self.ui.progressBar.setValue(0)
                self.ui.progressBar.setFormat(
                    "T%+.1fs" % (self.clock.get_time_until(self.observation.start_RA))
                )
                return

        self.ui.progressBar.setFormat("n/a")
        self.ui.progressBar.setValue(0)

    def update_dec_view(self):
        angle = self.current_dec - self.GB_LAT

        dish = QtGui.QPixmap("assets/dish.png").scaled(64, 64)
        # rotation = QtGui.QTransform().rotate(angle)
        # dish = dish.transformed(rotation)
        dish = QtWidgets.QGraphicsPixmapItem(dish)
        dish.setTransformOriginPoint(32, 32)
        dish.setRotation(angle)

        base = QtGui.QPixmap("assets/base.png").scaled(64, 64)
        base = QtWidgets.QGraphicsPixmapItem(base)

        self.dec_scene.clear()
        for i in [dish, base]:
            self.dec_scene.addItem(i)

    def display_info(self, message):
        self.ui.message_label.setText(message)

    def initialize_stripchart(self):
        # add channels to chart
        self.chart.addSeries(self.stripchart_series_b)
        self.chart.addSeries(self.stripchart_series_a)

        # hide the legend
        self.chart.legend().hide()

        # connect the Qt Designer stripchart view (`self.ui.stripchart`) with
        # `self.chart`
        self.ui.stripchart.setChart(self.chart)

    def update_stripchart(self):
        # get new data point
        new_a = self.data[len(self.data) - 1].a
        new_b = self.data[len(self.data) - 1].b
        new_ra = self.data[len(self.data) - 1].timestamp

        # add new data point to both series
        self.stripchart_series_a.append(new_a, new_ra)
        self.stripchart_series_b.append(new_b, new_ra)

        # magical song and dance in an attempt to appease the Qt gods
        self.chart.removeSeries(self.stripchart_series_b)
        self.chart.removeSeries(self.stripchart_series_a)
        self.chart.addSeries(self.stripchart_series_b)
        self.chart.addSeries(self.stripchart_series_a)

        axis_y = QtChart.QValueAxis()
        axis_y.setMin(
            self.clock.get_sidereal_seconds() - self.stripchart_display_seconds
        )
        axis_y.setMax(self.clock.get_sidereal_seconds())
        axis_y.setVisible(False)

        self.chart.setAxisY(axis_y)
        self.stripchart_series_a.attachAxis(axis_y)
        self.stripchart_series_b.attachAxis(axis_y)

    def clear_stripchart(self):
        self.stripchart_offset += self.stripchart_series_a.count()
        self.stripchart_series_a.clear()
        self.stripchart_series_b.clear()

    def get_refresh_rate(self):
        # TODO: make this an average over the last second OR last N ticks
        return 1 / self.time_since_last_tick if self.time_since_last_tick > 0 else -1.0

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
        dialog = ObsDialog(self, obs, self.clock)
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
        c = open("dec_cal.txt", "r").read().splitlines()  # get data from file
        for i in c:
            self.x.append(float(i))

    def calculate_declination(self, input_dec):
        """calculate the true dec from declinometer input and calibration data"""

        # input is below data
        if input_dec < self.x[0]:  # TODO: use minimum, not first
            return (
                (self.y[1] - self.y[0])
                / (self.x[1] - self.x[0])
                * (input_dec - self.x[0])
            ) + self.y[0]

        # input is above data
        if input_dec > self.x[-1]:  # TODO: use maximum, not last
            return (
                (self.y[-1] - self.y[-2])
                / (self.x[-1] - self.x[-2])
                * (input_dec - self.x[-1])
            ) + self.y[-1]

        # input is within data
        for i in range(len(self.x)):
            if input_dec <= self.x[i + 1]:
                if input_dec >= self.x[i]:
                    # (dy/dx)x + y_0
                    return (
                        (self.y[i + 1] - self.y[i])
                        / (self.x[i + 1] - self.x[i])
                        * (input_dec - self.x[i])
                    ) + self.y[i]

    def ra_calibration(self):
        self.set_time()

    def message(self, message):
        self.log(message)
        self.ui.message_label.setText(message)

    def log(self, message):
        # TODO: add timestamps
        # TODO: add a way to signal that a task completed successfully (like returning an object with "mark_done()" and "mark_failed" methods)
        if message != self.message_log[-1]:
            self.message_log.append(message)

    def update_console(self):
        self.ui.console_label.setText(
            reduce(lambda c, a: c + "\n" + a, self.message_log[-6:])
        )

    def alert(self, message, button_message="Close"):
        alert = AlertDialog(message, button_message)
        self.beep()
        alert.show()
        alert.exec_()

    def beep(self):
        if time.time() - self.last_beep_time > 1.0:
            self.click_sound.play()
            self.last_beep_time = time.time()
        # print("beep! ", time.time())

    def closeEvent(self, event):
        """override quit action to confirm before closing"""
        m = QtWidgets.QDialog()
        m.ui = quit_ui.Ui_Dialog()
        m.ui.setupUi(m)

        m.setWindowFlags(
            QtCore.Qt.Window | QtCore.Qt.WindowTitleHint | QtCore.Qt.CustomizeWindowHint
        )

        close = m.exec()
        if close:
            event.accept()
        else:
            event.ignore()


def main():
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    window = Threepio()
    window.set_state_normal()
    # window.set_state_testing()
    window.show()
    sys.exit(app.exec_())  # exit with code from app


if __name__ == "__main__":
    main()
