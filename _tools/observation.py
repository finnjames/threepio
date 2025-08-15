import time
from enum import Enum
from math import floor

from tools import Comm, DataPoint, MyPrecious, ObsRecord


class ObsType(Enum):
    """Observation type."""

    SCAN = 0
    SURVEY = 1
    SPECTRUM = 2
    UNSPECIFIED = 3


class State(Enum):
    NO_STATE = 0  # Do not use! indicates error has occurred
    OFF = 1
    CAL_1 = 2
    BG_1 = 3
    DATA = 4
    CAL_2 = 5
    BG_2 = 6
    DONE = 7
    WAITING = 8  # Extra


class Observation:
    """
    Superclass for each of the three types of observation: Scan, Survey, and Spectrum.

    To interact with any type of the observation object (e.g. an Oberservation object
    obs), first set its properties using the three 'obs.set_xxx()' API. Then,
    call the method 'obs.communication()' every 'obs.freq' seconds. Then, when the
    comm method returns a message other than 'Comm.NO_ACTION', prompt user for the
    appropriate action and call 'obs.next()' once to proceed into next stage. An
    observation is finished when the 'communication()' method returns 'Comm.FINISHED'.
    """

    def __init__(self):
        self.name = "Untitled"
        self.composite = False
        self.obs_type = ObsType.UNSPECIFIED

        # Parameters
        self.bg_dur = 60
        self.cal_dur = 60

        # Calibration and BG share the same sampling frequency, while the data has
        # its own sampling frequency. Only the data frequency is user-editable. When
        # running the program, the sampling frequency is automatically set by the
        # current state and is stored in 'self.freq'.
        self.cal_freq = 1
        self.data_freq = 6

        # Will be set accordingly in each state.
        self.freq = self.cal_freq

        self.state = State.OFF

        self.state_time_interval: tuple = (-1.0, -1.0)

        # Info
        self.start_time = None
        self.end_time = None
        self.min_dec = None  # If only one dec, this is it
        self.max_dec = None

        self.start_time = None
        self.end_time = None

        self.sweep_number = -1

        # File interface
        self.file_a = None
        self.file_b = None
        self.file_comp = None

        # Record keeping for later display/testing
        self.input_record: ObsRecord | None = None

        # Temporary bookkeeping
        self.cal_start = None
        self.bg_start = None

        self.data_start = None
        self.data_end = None

    # Settings API
    def set_start_and_end_times(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time

    def set_dec(self, min_dec: float | None, max_dec: float | None):
        if min_dec is None:
            raise ValueError("Min dec is not defined")
        assert min_dec
        if max_dec is not None and max_dec < min_dec:
            raise ValueError("Max dec must be greater min dec")
        assert max_dec
        self.min_dec = float(min_dec)
        self.max_dec = float(max_dec)

    def set_data_time(self, data_start, data_end):
        self.data_start = data_start
        self.data_end = data_end

    def set_name(self, name: str):
        self.name = name
        self.set_files()

    def set_data_freq(self, data_freq):
        self.data_freq = data_freq

    def set_input_record(self, input_record: ObsRecord):
        self.input_record = input_record

    # Communication API
    def communicate(self, data_point, timestamp: float) -> Comm:
        # assert self.start_time
        # assert self.end_time
        # assert self.cal_start
        # assert self.bg_start

        user_start_time = self.start_time - (self.bg_dur + self.cal_dur + 30)

        if self.state == State.OFF:
            self.state_time_interval = (-1.0, user_start_time)
            if timestamp < user_start_time:  # A 30-second buffer for user actions
                return Comm.NO_ACTION
            else:
                return Comm.START_CAL
        elif self.state == State.CAL_1:
            if floor(timestamp - self.cal_start) < self.cal_dur:
                self.write_data(data_point)
                return Comm.NO_ACTION
            else:
                return Comm.START_BG
        elif self.state == State.BG_1:
            if floor(timestamp - self.bg_start) < self.bg_dur:
                self.write_data(data_point)
                return Comm.NO_ACTION
            else:
                return Comm.START_WAIT
        elif self.state == State.WAITING:
            if timestamp < self.start_time:
                return Comm.NO_ACTION
            else:
                return Comm.START_DATA
        elif self.state == State.DATA:
            if timestamp < self.start_time:
                return Comm.NO_ACTION
            elif timestamp < self.end_time:
                return self.data_logic(data_point)
            # TODO: This logic should probably not be here
            elif self.obs_type is ObsType.SURVEY and self.data_logic(
                data_point
            ) not in [Comm.SEND_TEL_NORTH, Comm.SEND_TEL_SOUTH]:
                return Comm.FINISH_SWEEP
            else:
                return Comm.START_CAL
        elif self.state == State.CAL_2:
            if floor(timestamp - self.cal_start) < self.cal_dur:
                self.write_data(data_point)
                return Comm.NO_ACTION
            else:
                return Comm.START_BG
        elif self.state == State.BG_2:
            if floor(timestamp - self.bg_start) < self.bg_dur:
                self.write_data(data_point)
                return Comm.NO_ACTION
            else:
                return Comm.FINISHED
        elif self.state == State.DONE:
            return Comm.FINISHED
        return Comm.NO_ACTION

    # This is the action API
    def next(self, override=None):
        if override is not None:
            self.state = override
        else:
            if self.state == State.OFF:
                self.start_calibration_1()
            elif self.state == State.CAL_1:
                self.end_calibration_1()
            elif self.state == State.BG_1:
                self.end_background_1()
            elif self.state == State.WAITING:
                self.start_data()
            elif self.state == State.DATA:
                self.start_calibration_2()
            elif self.state == State.CAL_2:
                self.end_calibration_2()
            elif self.state == State.BG_2:
                self.stop()
            else:
                pass  # When state == DONE, do nothing
        return self.state

    def start_calibration_1(self):
        self.state = State.CAL_1
        self.start_time = time.time()
        self.cal_start = time.time()
        self.freq = self.cal_freq
        self.state_time_interval = (self.cal_start, self.cal_start + self.cal_dur)

    def end_calibration_1(self):
        self.state = State.BG_1
        self.write("*")
        self.bg_start = time.time()
        self.state_time_interval = (self.bg_start, self.bg_start + self.bg_dur)

    def end_background_1(self):
        self.state = State.WAITING

    def start_data(self):
        self.state = State.DATA
        self.write("*")
        self.freq = self.data_freq
        self.state_time_interval = (self.start_time, self.end_time)

    def start_calibration_2(self):
        self.state = State.CAL_2
        self.write("*")
        self.cal_start = time.time()
        self.freq = self.cal_freq
        self.state_time_interval = (self.cal_start, self.cal_start + self.cal_dur)

    def end_calibration_2(self):
        self.state = State.BG_2
        self.write("*")
        self.bg_start = time.time()
        self.state_time_interval = (self.bg_start, self.bg_start + self.bg_dur)

    def stop(self):
        self.state = State.DONE
        self.end_time = time.time()
        self.state_time_interval = (-1.0, self.end_time)
        self.write("*")
        self.write("*")
        self.write_meta()
        self.close_file()

    # To be implemented in each subclass
    def set_files(self):
        """This function generates appropriate file types (.md1 or .md2) based on
        observation type."""
        pass

    def data_logic(self, data_point) -> Comm:
        """
        This function defines the behavior of observation during the main data
        collection period. For example, in Survey this method is responsible for
        tracking if the dec is too high or too low. In Spectrum, this method tells
        the UI to beep to remind the user to change frequency.
        """
        return Comm.NO_ACTION

    # Helpers

    def write(self, string: str):
        assert self.file_comp
        assert self.file_a
        assert self.file_b
        if self.composite:
            self.file_comp.write(string)
        else:
            self.file_a.write(string)
            self.file_b.write(string)

    def write_data(self, point: DataPoint):
        # print(f"{point.timestamp}, dec: {point.dec}")
        self.write("%.2f" % point.timestamp)
        self.write("%.4f" % point.dec)
        assert self.file_comp
        assert self.file_a
        assert self.file_b
        if self.composite:
            self.file_comp.write("%.4f" % point.a)
            self.file_comp.write("%.4f" % point.b)
        else:
            self.file_a.write("%.4f" % point.a)
            self.file_b.write("%.4f" % point.b)

    def write_meta(self):
        self.write("TELESCOPE: The Mighty Forty")
        self.write("LOCAL START DATE: " + get_date(self.start_time))
        self.write("LOCAL START TIME: " + get_time(self.start_time))
        self.write("LOCAL STOP DATE: " + get_date(self.end_time))
        self.write("LOCAL STOP TIME: " + get_time(self.end_time))

    def close_file(self):
        assert self.file_comp
        assert self.file_a
        assert self.file_b
        if self.composite:
            self.file_comp.close()
        else:
            self.file_a.close()
            self.file_b.close()


class Scan(Observation):
    """A 'drift scan' across a source."""

    def __init__(self):
        super().__init__()
        self.obs_type = ObsType.SCAN

    def set_files(self):
        self.file_a = MyPrecious(self.name + "_a.md1")
        self.file_b = MyPrecious(self.name + "_b.md1")
        self.file_comp = MyPrecious(self.name + "_comp.md1")

    def data_logic(self, data_point) -> Comm:
        self.write_data(data_point)
        return Comm.NO_ACTION


class Survey(Observation):
    """2D 'nodding' map of a region of the radio sky."""

    def __init__(self):
        super().__init__()
        self.obs_type = ObsType.SURVEY

        self.sweep_number = 1

        self.outside = True

    def set_files(self):
        assert self.name
        self.file_a = MyPrecious(self.name + "_a.md2")
        self.file_b = MyPrecious(self.name + "_b.md2")
        self.file_comp = MyPrecious(self.name + "_comp.md2")

    def data_logic(self, data_point) -> Comm:
        if data_point.dec < self.min_dec or data_point.dec > self.max_dec:
            if not self.outside:
                self.write("*")
            self.outside = True
            if data_point.dec < self.min_dec:
                return Comm.SEND_TEL_NORTH
            elif data_point.dec > self.max_dec:
                return Comm.SEND_TEL_SOUTH
        else:
            if self.outside:
                self.outside = False
                self.sweep_number += 1
                return Comm.END_SEND_TEL
        self.write_data(data_point)
        return Comm.NO_ACTION


class Spectrum(Observation):
    """Spectrums are similar to Scans, except that they measure many frequencies."""

    def __init__(self):
        super().__init__()
        self.obs_type = ObsType.SPECTRUM

        self.cal_dur = 20
        self.bg_dur = 20

        self.cal_freq = 3
        self.data_freq = 10

        # These are the radio frequency (e.g. 1319.5 Mhz), not the sampling frequency!
        self.interval = 1
        self.freq_time = None
        self.timing_margin = 0.97

    # def set_start_and_end_times(self, start_time, end_time):
    #     super().set_start_and_end_times(start_time, start_time + 180)

    def set_data_time(self, data_start, data_end):
        super().set_data_time(data_start, data_start + 180)

    def set_files(self):
        self.file_a = MyPrecious(self.name + "_a.md1")
        self.file_b = MyPrecious(self.name + "_b.md1")
        self.file_comp = MyPrecious(self.name + "_comp.md1")

    def data_logic(self, data_point) -> Comm:
        if self.freq_time is None:
            self.freq_time = time.time()
            self.write_data(data_point)
            return Comm.NO_ACTION
        elif time.time() - self.freq_time < self.timing_margin * self.interval:
            self.write_data(data_point)
            return Comm.NO_ACTION
        else:
            self.freq_time = time.time()
            self.write_data(data_point)
            return Comm.BEEP


def get_date(epoch_time) -> str:
    return time.strftime("%m/%d/%Y", time.localtime(epoch_time))


def get_time(epoch_time) -> str:
    return time.strftime("%I:%M:%S %p", time.localtime(epoch_time))
