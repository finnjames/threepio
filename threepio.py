from enum import Enum
import time
from functools import reduce
from typing import Callable

from PyQt5 import QtChart, QtCore, QtGui, QtWidgets, QtMultimedia

from dialogs import AlertDialog, CreditsDialog, DecDialog, ObsDialog, RADialog
from layouts import threepio_ui, quit_ui
from tools import (
    Comm,
    DataPoint,
    Survey,
    Scan,
    Spectrum,
    SuperClock,
    Tars,
    MiniTars,
    discovery,
    LogTask,
    Observation,
    Alert,
    DecCalc,
    ObsType,
)


class Threepio(QtWidgets.QMainWindow):
    """
    Green Bank Observatory's 40-Foot Telescope's very own data acquisition system.
    Extends Qt's QMainWindow class and is the main window of the application.
    """

    # basic time
    BASE_PERIOD = 10  # ms = 100Hz
    GUI_UPDATE_PERIOD = 1000  # ms = 1Hz
    STRIPCHART_PERIOD = 16.7  # ms = 60Hz

    # palette
    BLUE = 0x2196F3
    RED = 0xFF5252

    class Mode(Enum):
        NORMAL = 0
        TESTING = 1

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
        self.mode = Threepio.Mode.NORMAL

        # "console" output
        self.message_log: list[LogTask] = []
        self.log(">>> THREEPIO")
        self.update_console()

        # clock
        self.clock = SuperClock()
        with open("ra-cal.txt", "r") as f:  # get data from file
            i = f.readline().strip()
            e = float(f.readline())
            RADialog.set_clock(self.clock, i, e)

        # initialize stripchart
        self.stripchart_display_seconds = 8
        self.should_clear_stripchart = False
        stripchart_log_task = self.log("Initializing stripchart...")
        self.stripchart_series_a = QtChart.QLineSeries()
        self.stripchart_series_b = QtChart.QLineSeries()
        self.axis_y = QtChart.QValueAxis()
        self.chart = QtChart.QChart()
        self.ui.stripchart.setRenderHint(QtGui.QPainter.Antialiasing)
        pen = QtGui.QPen(QtGui.QColor(self.BLUE))
        pen.setWidth(1)
        self.stripchart_series_a.setPen(pen)
        pen.setColor(QtGui.QColor(self.RED))
        self.stripchart_series_b.setPen(pen)
        self.initialize_stripchart()  # should this include more of the above?
        stripchart_log_task.set_status(0)

        self.update_stripchart_speed()

        stripchart_log_task = self.log("Initializing buttons...")
        # connect buttons
        self.ui.stripchart_speed_slider.valueChanged.connect(
            self.update_stripchart_speed
        )

        self.ui.actionInfo.triggered.connect(self.handle_credits)

        self.ui.actionScan.triggered.connect(self.handle_scan)
        self.ui.actionSurvey.triggered.connect(self.handle_survey)
        self.ui.actionSpectrum.triggered.connect(self.handle_spectrum)
        self.ui.actionGetInfo.triggered.connect(self.handle_get_info)

        self.ui.actionDec.triggered.connect(self.dec_calibration)
        self.ui.actionRA.triggered.connect(self.ra_calibration)

        self.ui.actionNormal.triggered.connect(self.set_state_normal)
        self.ui.actionTesting.triggered.connect(self.set_state_testing)
        self.ui.actionLegacy.triggered.connect(self.toggle_state_legacy)

        self.ui.chart_clear_button.clicked.connect(self.clear_stripchart)
        stripchart_log_task.set_status(0)

        # Tars/DATAQ
        dataq, arduino = discovery()
        self.tars = Tars(parent=self, device=dataq)
        self.tars.start()
        self.minitars = MiniTars(parent=self, device=arduino)
        self.minitars.start()

        # bleeps and bloops
        stripchart_log_task = self.log("Initializing audio...")
        self.click_sound = QtMultimedia.QSoundEffect()
        url = QtCore.QUrl()
        self.click_sound.setSource(url.fromLocalFile("assets/beep3.wav"))
        self.click_sound.setVolume(0.5)
        # self.click_sound.play()
        self.last_beep_time = 0.0
        self.tobeepornottobeep = False
        stripchart_log_task.set_status(0)

        # alerts
        self.open_alert = None
        self.alert_thread: set[QtCore.QThread] = set()
        self.worker = None

        # establish observation
        self.observation = None
        self.observation_state = False
        self.completed_one_calibration = False

        # establish data array & most recent dec
        self.data = []
        self.current_dec = 0.0
        self.current_data_point = None

        # tars communication interpretation
        self.previous_transmission = None

        # telescope visualization
        self.dec_scene = QtWidgets.QGraphicsScene()
        self.ui.dec_view.setScene(self.dec_scene)
        self.update_dec_view()

        # run initial calibration
        self.dec_calc = DecCalc()
        self.dec_calc.load_dec_cal()

        # primary clock
        stripchart_log_task = self.log("Initializing clock...")
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.tick)  # do everything
        self.timer.start(self.BASE_PERIOD)  # set refresh rate
        # assign timers to functions meant to fire periodically
        self.clock.add_timer(1000, self.update_gui)
        self.data_timer = self.clock.add_timer(1000, self.update_data)
        stripchart_log_task.set_status(0)

        # measure refresh rate
        self.time_of_last_fps_update = time.perf_counter()
        self.ticks_since_last_fps_update = 0

        # alert user that threepio is done initializing
        self.message("Ready!!!")

    def tick(self):
        """
        Primary controller for each clock tick. Fires as fast as possible up to 100Hz.
        Anything meant to update as often as possible should be placed here. Everything
        else should be assigned to a timer.
        """

        # attempt to grab latest data point; it won't always be stored
        tars_data = self.tars.read_latest()  # get data from DAQ
        minitars_data = self.minitars.read_latest()  # get data from Arduino
        sidereal_timestamp = self.clock.get_sidereal_seconds()

        # if data was available above, save it
        if tars_data is not None and minitars_data is not None:
            self.current_dec = self.dec_calc.calculate_declination(
                minitars_data
            )  # get dec
            self.current_data_point = DataPoint(  # create data point
                sidereal_timestamp,  # ra
                self.current_dec,  # dec
                tars_data[0][1],  # channel a
                tars_data[1][1],  # channel b
            )
            self.data.append(self.current_data_point)  # add to data list

        self.clock.run_timers()  # run all timers that are due

        # update every tick
        self.update_stripchart()
        self.update_dec_view()

        self.ticks_since_last_fps_update += 1  # for measuring fps

    def update_data(self) -> None:
        if not self.check_observation_state():
            return

        period = 1000 / self.observation.freq  # Hz -> ms
        self.data_timer.set_period(period)

        transmission = self.observation.communicate(
            self.current_data_point, self.clock.get_time()
        )

        obs_type = self.observation.obs_type

        if transmission != self.previous_transmission:  # TODO: should these be special?
            if transmission is Comm.START_CAL:
                alerts = [
                    Alert("Turn the calibration switches ON", "Okay"),
                    Alert("Are the calibration switches ON?", "Yes"),
                ]
                if self.completed_one_calibration:
                    if self.observation.obs_type is ObsType.SURVEY:
                        alerts = [
                            Alert("STOP the telescope", "Okay"),
                            Alert("Has the telescope been stopped?", "Yes"),
                        ] + alerts
                    elif self.observation.obs_type is ObsType.SPECTRUM:
                        alerts = [
                            Alert("Set frequency to 1319.5MHz", "Okay"),
                            Alert("Is the frequency set to 1319.5MHz?", "Yes"),
                        ] + alerts

                def callback():
                    self.clock.reset_anchor_time()
                    self.observation.next()
                    self.message("Taking calibration data!!!")

                self.alert(*alerts, callback=callback)
                self.completed_one_calibration = True  # only alert on second cal

            elif transmission is Comm.START_BG:

                def callback():
                    self.clock.reset_anchor_time()
                    self.observation.next()
                    self.message("Taking background data!!!")

                self.alert(
                    Alert("Turn the calibration switches OFF", "Okay"),
                    Alert("Are the calibration switches OFF?", "Yes"),
                    callback=callback,
                )

        if transmission is Comm.START_WAIT:
            self.observation.next()
            self.message(f"Waiting for {obs_type.name.lower()} to begin...")
        elif transmission is Comm.START_DATA:
            self.observation.next()
            self.message(f"Taking {obs_type.name.lower()} data!!!")
        elif transmission is Comm.FINISHED:
            self.observation.next()
            self.message(f"{obs_type.name.capitalize()} complete!!!")
            self.observation = None
        elif transmission is Comm.SEND_TEL_NORTH:
            self.message("Send telescope NORTH at max speed!!!", beep=False, log=False)
            self.tobeepornottobeep = True
        elif transmission is Comm.SEND_TEL_SOUTH:
            self.message("Send telescope SOUTH at max speed!!!", beep=False, log=False)
            self.tobeepornottobeep = True
        elif transmission is Comm.END_SEND_TEL:
            self.message(
                f"Taking {obs_type.name.lower()} data!!!", beep=False, log=False
            )
        elif transmission is Comm.FINISH_SWEEP:
            self.message("Finishing last sweep!!!", beep=False, log=False)
        elif transmission is Comm.BEEP:
            self.tobeepornottobeep = True
        elif transmission is Comm.NEXT:
            self.observation.next()
        elif transmission is Comm.NO_ACTION:
            pass

        self.previous_transmission = transmission

    def set_state_normal(self):
        self.ui.actionNormal.setChecked(True)
        self.ui.actionTesting.setChecked(False)
        self.ui.testing_frame.hide()
        self.adjustSize()
        self.setFixedSize(800, 640)
        self.mode = Threepio.Mode.NORMAL

    def set_state_testing(self):
        self.ui.actionNormal.setChecked(False)
        self.ui.actionTesting.setChecked(True)
        self.setFixedSize(800, 826)
        self.ui.testing_frame.show()
        self.mode = Threepio.Mode.TESTING

    def toggle_state_legacy(self):
        """lol"""
        self.legacy_mode = not self.legacy_mode
        self.setStyleSheet(
            "background-color:#00ff00; color:#ff0000" if self.legacy_mode else ""
        )
        url = QtCore.QUrl()
        self.click_sound.setSource(
            url.fromLocalFile(
                f"assets/beep{'-legacy' if self.legacy_mode else '3'}.wav"
            )
        )
        self.ui.actionLegacy.setChecked(self.legacy_mode)

    def check_observation_state(self) -> bool:
        if (
            self.observation_state
            and self.observation is None
            or not self.observation_state
            and self.observation is not None
        ):
            self.toggle_observation_state()

        return self.observation_state

    def toggle_observation_state(self) -> None:
        # disable resetting RA/Dec after loading obs
        self.observation_state = not self.observation_state
        for a in (
            self.ui.actionRA,
            self.ui.actionDec,
            self.ui.actionSurvey,
            self.ui.actionScan,
            self.ui.actionSpectrum,
        ):
            a.setDisabled(self.observation_state)
        self.ui.actionGetInfo.setEnabled(self.observation_state)

    @staticmethod
    def handle_credits():
        dialog = CreditsDialog()
        dialog.exec_()

    def update_stripchart_speed(self):
        self.stripchart_display_seconds = 120 - (
            (110 / 6) * self.ui.stripchart_speed_slider.value()
        )

    def update_gui(self):
        # current_time = self.clock.get_time()
        if self.tobeepornottobeep:
            self.beep(message="update_gui")
            self.tobeepornottobeep = False

        self.ui.ra_value.setText(self.clock.get_formatted_sidereal_time())  # RA
        self.ui.dec_value.setText(f"{self.current_dec:.4f}°")  # dec
        if self.observation is not None:
            self.ui.sweep_value.setText(
                str(self.observation.sweep_number)
                if self.observation.sweep_number != -1
                else "n/a"
            )  # sweep number

        self.update_progress_bar()
        self.update_fps()
        self.update_console()
        self.update_voltage()

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
                + ("{:0>2}".format(hours) + ":" if hours != 0 else "")
                + ("{:0>2}".format(minutes) + ":" if minutes != 0 else "")
                + "{:0>2}".format(seconds)
            )
            return

        self.ui.progressBar.setFormat("n/a")
        self.ui.progressBar.setValue(0)

    def update_dec_view(self):
        angle = self.current_dec - self.clock.GB_LATITUDE

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

    def update_fps(self):
        """updates the fps counter to display current refresh rate"""
        current_time = time.perf_counter()
        time_since_last_fps_update = current_time - self.time_of_last_fps_update

        try:
            new_fps = "%.2fHz" % (
                self.ticks_since_last_fps_update / time_since_last_fps_update
            )
        except ZeroDivisionError:
            new_fps = -1.0

        self.ui.refresh_value.setText(new_fps)
        self.time_of_last_fps_update = current_time
        self.ticks_since_last_fps_update = 0

    def initialize_stripchart(self):
        self.chart.addSeries(self.stripchart_series_b)
        self.chart.addSeries(self.stripchart_series_a)

        self.chart.legend().hide()

        self.ui.stripchart.setChart(self.chart)

    def update_stripchart(self):
        try:
            # parse latest data point
            # TODO: this will duplicate points if one fails to read
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
        except IndexError:  # no data yet
            pass

    def clear_stripchart(self):
        self.should_clear_stripchart = True

    def update_voltage(self):
        if len(self.data) > 0:
            self.ui.channelA_value.setText("%.4fV" % self.data[len(self.data) - 1].a)
            self.ui.channelB_value.setText("%.4fV" % self.data[len(self.data) - 1].b)

    def handle_survey(self):
        obs = Survey()
        self.new_observation(obs)

    def handle_scan(self):
        obs = Scan()
        self.new_observation(obs)

    def handle_spectrum(self):
        obs = Spectrum()
        self.new_observation(obs)

    def new_observation(self, obs: Observation):
        dialog = ObsDialog(self, obs, self.clock)
        dialog.setWindowTitle("New " + obs.obs_type.name.capitalize())
        dialog.exec_()
        self.completed_one_calibration = False

    def handle_get_info(self):
        if self.observation is not None:
            pass
        dialog = ObsDialog(self, self.observation, self.clock, info=True)
        dialog.setWindowTitle("Current " + self.observation.obs_type.name.capitalize())
        dialog.exec_()

    def dec_calibration(self):
        dialog = DecDialog(self.minitars, self)
        if self.mode is Threepio.Mode.TESTING:
            dialog.show()
        dialog.exec_()

        self.dec_calc.load_dec_cal()

    def ra_calibration(self, cancelable=True):
        dialog = RADialog(self, self.clock, cancelable=cancelable)
        dialog.show()
        dialog.exec_()

    def message(self, message, beep=True, log=True):
        if log:
            self.log(message)
        if beep:
            self.beep(message="message")
        self.ui.message_label.setText(message)

    def log(self, message, allow_dups=False) -> LogTask:
        if (
            len(self.message_log) == 0
            or allow_dups
            or message != self.message_log[-1].message
        ):
            new_log_task = LogTask(message)
            try:
                new_log_task.set_sidereal_str(self.clock.get_formatted_sidereal_time())
            except AttributeError:
                pass
            self.message_log.append(new_log_task)
            print(new_log_task.get_message())
            return new_log_task

    def update_console(self):
        """refresh console with the latest statuses and last 7 logs"""
        self.ui.console_label.setText(
            reduce(
                lambda c, a: c + "\n" + a,
                [i.get_message() for i in self.message_log[-7:]],
            )
        )

    def alert(self, *alerts, callback: Callable[[], None] = lambda: None):
        new_thread = QtCore.QThread()
        self.alert_thread.add(new_thread)
        self.worker = self.AlertWorker(self)
        self.worker.moveToThread(new_thread)
        # connect signals and slots
        new_thread.started.connect(lambda: self.worker.run(*alerts, callback=callback))
        self.worker.finished.connect(new_thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)

        def cleanup():
            self.alert_thread.remove(new_thread)
            new_thread.deleteLater()

        new_thread.finished.connect(cleanup)

        new_thread.start()

    class AlertWorker(QtCore.QObject):
        finished = QtCore.pyqtSignal()
        progress = QtCore.pyqtSignal(int)

        def __init__(self, threepio):
            super().__init__()
            self.threepio = threepio

        def run(self, *alerts, callback: Callable[[], None]):
            for alert in alerts:
                self.threepio.alert_aux(alert.text, alert.button)
            callback()
            self.finished.emit()

    def alert_aux(self, alert_text, button_text):
        self.log(alert_text)
        alert = AlertDialog(alert_text, button_text)
        self.beep(message="alert")
        alert.show()
        alert.exec_()

    # noinspection PyUnusedLocal
    def beep(self, message=""):
        """message is for debugging"""
        self.click_sound.play()
        self.last_beep_time = time.time()
        # print("beep!", message, time.time())

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
    app.setWindowIcon(QtGui.QIcon(f"assets/robot.png"))
    window = Threepio()
    window.set_state_normal()
    # window.set_state_testing()
    window.show()
    sys.exit(app.exec_())  # exit with code from app


if __name__ == "__main__":
    main()
