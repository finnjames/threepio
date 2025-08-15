import time
from tools import Comm, MyPrecious, Observation, ObsType


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
