r"""
  __  __                    _
 / /_/ /  _______ ___ ___  (_)__    ___  __ __
/ __/ _ \/ __/ -_) -_) _ \/ / _ \_ / _ \/ // /
\__/_//_/_/  \__/\__/ .__/_/\___(_) .__/\_, /
                   /_/           /_/   /___/

"""

import time, math
from functools import reduce

from PyQt5 import QtChart, QtCore, QtGui, QtWidgets, QtMultimedia

from dialogs import AlertDialog, CreditsDialog, DecDialog, ObsDialog, RADialog
from layouts import threepio_ui, quit_ui
from tools import Comm, DataPoint, Survey, Scan, Spectrum, SuperClock, Tars, discovery


class Threepio(QtWidgets.QMainWindow):
    """main class for the app"""

    # basic time
    BASE_PERIOD = 10  # ms
    STRIPCHART_PERIOD = 16.7  # ms
    VOLTAGE_PERIOD = 1000  # ms
    # how many data points to draw to stripchart
    stripchart_display_seconds = 8
    should_clear_stripchart = False

    # test data
    ticker = 0
    other_ticker = 0
    foo = 0.0

    # speed measurement
    tick_time = 0.0
    timing_margin = 0.97

    # stripchart
    stripchart_low = -1
    stripchart_high = 1

    # declination calibration lists
    x = list[float]
    y = list[float]

    # palette
    BLUE = 0x2196F3
    RED = 0xFF5252

    # green bank coords
    GB_LATITUDE = 38.4339

    # tars communication interpretation
    transmission = None
    old_transmission = None

    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        # use main_ui for window setup
        self.ui = threepio_ui.Ui_MainWindow()
        with open("stylesheet.qss") as f:
            self.setStyleSheet(f.read())
        self.ui.setupUi(self)
        self.setWindowTitle("threepio")

        # hide the close/minimize/fullscreen buttons
        self.setWindowFlags(
            QtCore.Qt.Window | QtCore.Qt.WindowTitleHint | QtCore.Qt.CustomizeWindowHint
        )

        # mode
        self.legacy_mode = False
        self.mode = "normal"

        # "console" output
        self.message_log = ["Starting threepio!!!"]
        self.update_console()

        # clock
        self.clock = None
        self.set_time()

        # initialize stripchart
        self.log("Initializing stripchart!!!")
        self.stripchart_series_a = QtChart.QLineSeries()
        self.stripchart_series_b = QtChart.QLineSeries()
        # self.stripchart_series_a.setUseOpenGL(True)
        # self.stripchart_series_b.setUseOpenGL(True)
        self.axis_y = QtChart.QValueAxis()
        self.chart = QtChart.QChart()
        # comment this for better performance
        self.ui.stripchart.setRenderHint(QtGui.QPainter.Antialiasing)
        pen = QtGui.QPen(QtGui.QColor(self.BLUE))
        pen.setWidth(1)
        self.stripchart_series_a.setPen(pen)
        pen.setColor(QtGui.QColor(self.RED))
        self.stripchart_series_b.setPen(pen)
        self.initialize_stripchart()

        self.update_speed()

        self.log("Initializing buttons!!!")
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
        self.ui.actionLegacy.triggered.connect(self.toggle_state_legacy)

        self.ui.chart_clear_button.clicked.connect(self.clear_stripchart)

        # Tars/DATAQ stuff
        device = discovery()
        self.tars = Tars(parent=self, device=device)
        self.tars.setup()
        self.tars.start()

        # bleeps and bloops
        self.log("Initializing audio!!!")
        self.click_sound = QtMultimedia.QSoundEffect()
        url = QtCore.QUrl()
        self.click_sound.setSource(url.fromLocalFile("assets/beep3.wav"))
        self.click_sound.setVolume(0.5)
        # self.click_sound.play()
        self.last_beep_time = 0.0

        # establish observation
        self.observation = None

        # establish data array & most recent dec
        self.data = []
        self.current_dec = 0.0

        # run initial calibration
        self.load_dec_cal()

        # alert user
        self.message("Ready!!!")

        # refresh timer
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.tick)  # do everything
        self.timer.start(self.BASE_PERIOD)  # set refresh rate

        # used for measuring refresh rate
        self.time_since_last_tick = 0
        self.time_since_last_stripchart_update = 0
        self.time_since_last_voltage_update = 0
        # TODO: do I need both of these type checks?
        # noinspection PyUnresolvedReferences
        self.time_of_last_tick = self.clock.get_time()  # type: ignore
        self.time_of_last_refresh_update = self.time_of_last_tick
        self.time_of_last_voltage_update = self.time_of_last_tick
        self.time_of_last_stripchart_update = self.time_of_last_tick

        # QGraphicsView TODO: move this into its own method
        self.dec_scene = QtWidgets.QGraphicsScene()
        self.ui.dec_view.setScene(self.dec_scene)
        self.update_dec_view()

    def tick(self):  # primary controller for each clock tick

        # update all of the timing vars
        current_time = self.clock.get_time()
        self.time_since_last_tick = current_time - self.time_of_last_tick
        self.time_since_last_stripchart_update = (
            current_time - self.time_of_last_stripchart_update
        )
        self.time_since_last_voltage_update = (
            current_time - self.time_of_last_voltage_update
        )

        self.time_of_last_tick = current_time

        if current_time - self.time_of_last_refresh_update > 1:
            self.ui.refresh_value.setText("%.2fHz" % self.get_refresh_rate())
            self.time_of_last_refresh_update = current_time

        # TODO: clean up main clock loop

        if self.observation is None:

            period = self.BASE_PERIOD * 0.001  # ms -> s

            if (current_time - self.tick_time) > (period * self.timing_margin):
                self.tick_time = current_time

                try:
                    tars_data = self.tars.read_latest()  # get data from DAQ

                    self.current_dec = self.calculate_declination(tars_data[2][1])

                    data_point = DataPoint(
                        self.clock.get_sidereal_seconds(),  # ra
                        self.current_dec,  # dec
                        tars_data[0][1],  # channel a
                        tars_data[1][1],  # channel b
                    )

                    self.data.append(data_point)
                except TypeError:
                    pass

                # self.update_gui()  # update gui except voltage and stripchart

        else:

            # can't reset RA/Dec after loading obs; TODO: move this elsewhere
            for a in [
                self.ui.actionRA,
                self.ui.actionDec,
                self.ui.actionSurvey,
                self.ui.actionScan,
                self.ui.actionSpectrum,
            ]:
                a.setDisabled(True)

            period = 1 / self.observation.freq

            if (current_time - self.tick_time) > (period * self.timing_margin):

                self.tick_time = current_time

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

                self.update_stripchart()

                # This is a mess, but I think it should be fine for now
                # TODO: at least move this to its own method
                if self.transmission == Comm.START_CAL:
                    self.alert("Set calibration switches to ON", "Okay")
                    self.alert("Are the calibration switches on?", "Yes")
                    self.observation.next()
                    self.message("Taking calibration data!!!")
                elif self.transmission == Comm.STOP_CAL:
                    self.alert("Set calibration switches to OFF", "Okay")
                    self.alert("Are the calibration switches off?", "Yes")
                    self.observation.next()
                    self.message("Taking background data!!!")
                elif self.transmission == Comm.NEXT:
                    self.observation.next()
                elif self.transmission == Comm.FINISHED:
                    self.observation.next()
                    self.message("Observation complete!")
                elif self.transmission == Comm.BEEP:
                    self.beep()
                elif self.transmission == Comm.NO_ACTION:
                    pass

                time_until_start = self.observation.start_RA - current_time
                if time_until_start <= 0 < (self.observation.end_RA - current_time):
                    self.message("Taking observation data!!!")

        self.update_gui()  # the GUI handles its own timingO

    def set_state_normal(self):
        self.ui.actionNormal.setChecked(True)
        self.ui.actionTesting.setChecked(False)
        self.ui.testing_frame.hide()
        self.adjustSize()
        self.setFixedSize(800, 640)
        self.mode = "normal"

    def set_state_testing(self):
        self.ui.actionNormal.setChecked(False)
        self.ui.actionTesting.setChecked(True)
        self.setFixedSize(800, 826)
        self.ui.testing_frame.show()
        self.mode = "testing"

    def toggle_state_legacy(self):
        """lol"""
        if self.legacy_mode:
            self.setStyleSheet("")
            self.legacy_mode = False
        else:
            self.setStyleSheet("background-color:#00ff00; color: #ff0000")
            self.legacy_mode = True
        self.ui.actionLegacy.setChecked(self.legacy_mode)

    @staticmethod
    def handle_credits():
        dialog = CreditsDialog()
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
        current_time = self.clock.get_time()

        self.ui.ra_value.setText(self.clock.get_sidereal_time())  # show RA
        self.ui.dec_value.setText("%.4f°" % self.current_dec)  # show dec
        self.update_progress_bar()

        self.update_dec_view()
        self.update_console()

        if self.time_since_last_voltage_update >= self.VOLTAGE_PERIOD * 0.001:
            self.update_voltage()
            self.time_of_last_voltage_update = current_time
        if self.time_since_last_stripchart_update >= self.STRIPCHART_PERIOD * 0.001:
            self.update_stripchart()
            self.time_of_last_stripchart_update = current_time

    def update_progress_bar(self):
        # T=start_RA
        if self.observation is not None:
            # if not self.observation.end_RA - self.observation.start_RA <= 1:
            if (
                self.clock.get_time_until(self.observation.start_RA)
                > 0
                > self.clock.get_time_until(self.observation.end_RA)
            ):  # between start and end time
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

            # display the time nicely
            tus = self.clock.get_time_until(
                self.observation.start_RA
            )  # time until start
            hours = int((abs_tus := abs(tus)) / 3600)
            minutes = int((abs_tus - (hours * 3600)) / 60)
            seconds = int(abs_tus - (hours * 3600) - (minutes * 60))
            self.ui.progressBar.setFormat(
                "T"
                + ("-" if tus < 0 else "+")
                + (str(hours) + ":" if hours != 0 else "")
                + (str(minutes) + ":" if minutes != 0 else "")
                + str(seconds)
            )
            return

        self.ui.progressBar.setFormat("n/a")
        self.ui.progressBar.setValue(0)

    def update_dec_view(self):
        angle = self.current_dec - self.GB_LATITUDE

        # telescope dish
        dish = QtGui.QPixmap("assets/dish.png")
        dish = QtWidgets.QGraphicsPixmapItem(dish)
        dish.setTransformOriginPoint(32, 32)
        dish.setTransformationMode(QtCore.Qt.SmoothTransformation)
        dish.setY(16)
        dish.setRotation(angle)

        # telescope base
        base = QtGui.QPixmap("assets/base.png")
        base = QtWidgets.QGraphicsPixmapItem(base)
        base.setTransformationMode(QtCore.Qt.SmoothTransformation)

        self.dec_scene.clear()
        for i in [dish, base]:
            self.dec_scene.addItem(i)

    def display_info(self, message):
        self.ui.message_label.setText(message)

    def initialize_stripchart(self):
        self.chart.addSeries(self.stripchart_series_b)
        self.chart.addSeries(self.stripchart_series_a)

        self.chart.legend().hide()

        self.ui.stripchart.setChart(self.chart)

    def update_stripchart(self):
        # get new data point
        new_a = self.data[len(self.data) - 1].a
        new_b = self.data[len(self.data) - 1].b
        new_ra = self.data[len(self.data) - 1].timestamp

        # add new data point to both series
        self.stripchart_series_a.append(new_a, new_ra)
        self.stripchart_series_b.append(new_b, new_ra)

        # we use these value several times
        current_sideral_seconds = self.clock.get_sidereal_seconds()
        oldest_y = current_sideral_seconds - self.stripchart_display_seconds

        # remove the trailing end of the series
        clear_it = self.should_clear_stripchart  # prevents a race hazard?
        for i in [self.stripchart_series_a, self.stripchart_series_b]:
            if clear_it:
                i.clear()
            elif i.count() > 2 and i.at(1).y() < oldest_y:
                i.removePoints(0, 2)
        self.should_clear_stripchart = False

        # These lines are required to prevent a Qt error
        self.chart.removeSeries(self.stripchart_series_b)
        self.chart.removeSeries(self.stripchart_series_a)
        self.chart.addSeries(self.stripchart_series_b)
        self.chart.addSeries(self.stripchart_series_a)

        axis_y = QtChart.QValueAxis()
        axis_y.setMin(oldest_y)
        axis_y.setMax(current_sideral_seconds)
        axis_y.setVisible(False)

        self.chart.setAxisY(axis_y)
        self.stripchart_series_a.attachAxis(axis_y)
        self.stripchart_series_b.attachAxis(axis_y)

    def clear_stripchart(self):
        self.should_clear_stripchart = True

    def update_voltage(self):
        if len(self.data) > 0:
            self.ui.channelA_value.setText("%.4fV" % self.data[len(self.data) - 1].a)
            self.ui.channelB_value.setText("%.4fV" % self.data[len(self.data) - 1].b)

    def get_refresh_rate(self):
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
        dialog.exec_()

    def dec_calibration(self):
        dialog = DecDialog(self.tars, self)
        if self.mode == "testing":
            dialog.show()
        dialog.exec_()

        self.load_dec_cal()

    def load_dec_cal(self):
        # create y array
        self.y = []
        i = DecDialog.south_dec
        while i <= DecDialog.north_dec:
            self.y.append(float(i))
            i += abs(DecDialog.step)

        # create x array
        self.x = []
        with open("dec-cal.txt", "r") as f:  # get data from file
            c = f.read().splitlines()
            for i in c:
                self.x.append(float(i))

    def calculate_declination(self, input_dec: float):
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

    def message(self, message, beep=True, log=True):
        if log:
            self.log(message)
        if beep:
            self.beep()
        self.ui.message_label.setText(message)

    def log(self, message, allowDups=False):
        # TODO: add a way to signal that a task completed successfully (like returning
        #  an object with "mark_done()" and "mark_failed" methods)
        if allowDups or message != self.message_log[-1][11:]:
            try:
                self.message_log.append(f"[{self.clock.get_sidereal_time()}] {message}")
            except AttributeError:
                self.message_log.append(message)

    def update_console(self):
        self.ui.console_label.setText(
            reduce(lambda c, a: c + "\n" + a, self.message_log[-7:])
        )

    def alert(self, message, button_message="Close"):
        self.log(message)
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
    icon_type = "icns" if sys.platform == "darwin" else "png"
    app.setWindowIcon(QtGui.QIcon(f"assets/robot.{icon_type}"))
    window = Threepio()
    window.set_state_normal()
    # window.set_state_testing()
    window.show()
    sys.exit(app.exec_())  # exit with code from app


if __name__ == "__main__":
    main()
