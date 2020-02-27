# TODO:
# 1. Figure out a consistent way to deal with time
#   DONE a) when time is used for starting/ending certain stages of the observation
#   DONE b) when appending metadata about the observation such as start and end time and date.

import time
from enum import Enum

from comm import Comm
from datapoint import DataPoint
from precious import MyPrecious

class Observation():
    """
    Superclass for each of the three types of observation you might encounter on your Pokemon journey
    
    To interact with any type of the observation object (e.g an Oberservation object obs), first set
    its properties using the three 'obs.set_xxx()' API. Then, call the method 'obs.communication()' 
    every 'obs.freq' seconds. Then when the comm method returns a message other than 'Comm.NO_ACTION',
    prompt user for the appropriate action and call 'obs.next()' once to proceed into next stage.
    An observation is finished when the 'communication()' method returns 'Comm.FINISHED'.
    """
    
    def __init__(self):
        self.name       = None
        self.composite  = False
        self.obs_type   = None

        # Parameters
        self.bg_dur     = 60
        self.cal_dur    = 60

        # Calibration and BG share the same sampling frequency, while the data has its own sampling
        #   frequency. Only the data frequency is user-editable. When running the program, the sampling
        #   frequency is automatically set by the current state and is stored in 'self.freq'.
        self.cal_freq   = 1
        self.data_freq  = 1

        # Will be set accordingly in each state.
        self.freq       = self.cal_freq

        self.state      = self.State.OFF
        
        # Info
        self.start_RA   = None
        self.end_RA     = None
        self.max_dec    = None     # if only one dec, this is it
        self.min_dec    = None

        self.start_time = None
        self.end_time   = None

        # File interface
        self.file_a     = None
        self.file_b     = None
        self.file_comp  = None

        # Temporary bookkeeping
        self.cal_start  = None
        self.bg_start   = None
        
        self.data_start = None
        self.data_end   = None
        
        # # The data list, for backup
        # self.data       = []
    
    # Settings API
    def set_RA(self, start_RA, end_RA):
        self.start_RA = start_RA
        self.end_RA = end_RA
    
    def set_dec(self, max_dec, min_dec = None):
        self.max_dec = max_dec
        self.min_dec = min_dec
        
    def set_data_time(self, data_start, data_end):
        self.data_start = data_start
        self.data_end = data_end

    def set_name(self, name):
        self.name = name
        self.set_files()

    def set_data_freq(self, data_freq):
        self.data_freq = data_freq

    # This is the communication API
    def communicate(self, data_point, timestamp = None):
        if timestamp == None:
            timestamp = time.time()
            
        if self.state == self.State.OFF:
            if timestamp < self.start_RA - (self.bg_dur + self.cal_dur + 30):
                # A 30 seconds buffer for user actions
                return Comm.NO_ACTION
            else:
                return Comm.START_CAL
        elif self.state == self.State.CAL_1:
            if timestamp - self.cal_start < self.cal_dur:
                self.write_data(data_point)
                return Comm.NO_ACTION
            else:
                return Comm.STOP_CAL
        elif self.state == self.State.BG_1:
            if timestamp - self.bg_start < self.bg_dur:
                self.write_data(data_point)
                return Comm.NO_ACTION
            else:
                return Comm.NEXT
        elif self.state == self.State.DATA:
            if timestamp < self.start_RA:
                return Comm.NO_ACTION
            elif timestamp < self.end_RA:
                return self.data_logic(data_point)
            else:
                return Comm.START_CAL
        elif self.state == self.State.CAL_2:
            if timestamp - self.cal_start < self.cal_dur:
                self.write_data(data_point)
                return Comm.NO_ACTION
            else:
                return Comm.STOP_CAL
        elif self.state == self.State.BG_2:
            if timestamp - self.bg_start < self.bg_dur:
                self.write_data(data_point)
                return Comm.NO_ACTION
            else:
                return Comm.FINISHED
        elif self.state == self.State.DONE:
            return Comm.FINISHED

    # This is the action API
    def next(self):
        if self.state == self.State.OFF:
            self.start_calibration_1()
        elif self.state == self.State.CAL_1:
            self.end_calibration_1()
        elif self.state == self.State.BG_1:
            self.end_background_1()
        elif self.state == self.State.DATA:
            self.start_calibration_2()
        elif self.state == self.State.CAL_2:
            self.end_calibration_2()
        elif self.state == self.State.BG_2:
            self.stop()
        else:
            pass # state == DONE, do nothing

    # State machine
    class State(Enum):
        OFF     = 1
        CAL_1   = 2
        BG_1    = 3
        DATA    = 4
        CAL_2   = 5
        BG_2    = 6
        DONE    = 7

    def start_calibration_1(self):
        self.state = self.State.CAL_1
        self.start_time = time.time()
        self.cal_start = time.time()
        self.freq = self.cal_freq

    def end_calibration_1(self):
        self.state = self.State.BG_1
        self.write('*')
        self.bg_start = time.time()
        
    def end_background_1(self):
        self.state = self.State.DATA
        self.write('*')
        self.freq = self.data_freq

    def start_calibration_2(self):
        self.state = self.State.CAL_2
        self.write('*')
        self.cal_start = time.time()
        self.freq = self.cal_freq

    def end_calibration_2(self):
        self.state = self.State.BG_2
        self.write('*')
        self.bg_start = time.time()

    def stop(self):
        self.state = self.State.DONE
        self.end_time = time.time()
        self.write('*')
        self.write('*')
        self.write_meta()

    # To be implemented in each subclass
    def set_files(self):
        """This function generates appropriate file types (.md1 or .md2) based on observation type"""
        pass

    def data_logic(self, data_point):
        """
        This function defines the behavior of observation during the main data collection period.
        For example, in Survey this method is responsible for tracking if the dec is too high or too
        low. In Spectrum, this method tells the UI to beep to remind the user to change frequency.s
        """
        pass
        
    ############################ Helpers ############################

    def write(self, string: str):
        if self.composite:
            self.file_comp.write(string)
        else:
            self.file_a.write(string)
            self.file_b.write(string)

    def write_data(self, point: DataPoint):
        self.write("%.2f" % point.timestamp)
        self.write("%.2f" % point.dec)
        if self.composite:
            self.file_comp.write("%.4f" % point.a)
            self.file_comp.write("%.4f" % point.b)
        else:
            self.file_a.write("%.4f" % point.a)
            self.file_b.write("%.4f" % point.b)

    def write_meta(self):
        self.write('TELESCOPE: The Mighty Forty')
        self.write('LOCAL START DATE: ' + get_date(self.start_time))
        self.write('LOCAL START TIME: ' + get_time(self.start_time))
        self.write('LOCAL STOP DATE: '  + get_date(self.end_time))
        self.write('LOCAL STOP TIME: '  + get_time(self.end_time))

    # def get_last_data(self):
    #     return self.data[len(self.data) - 1]

class Scan(Observation):
    """Set a start and end RA"""

    def __init__(self):
        super().__init__()
        self.obs_type   = "Scan"

        self.data_freq  = 1

    def set_files(self):
        self.file_a = MyPrecious(self.name + '_a.md1')
        self.file_b = MyPrecious(self.name + '_b.md1')
        self.file_comp = MyPrecious(self.name + '_comp.md1')

    def data_logic(self, data_point):
        self.write_data(data_point)
        return Comm.NO_ACTION

class Survey(Observation):
    """Set a region in sky using start and end RA/DEC"""

    def __init__(self):
        super().__init__()
        self.obs_type   = "Survey"

        self.data_freq  = 1
        self.outside    = False
        
    def set_files(self):
        self.file_a = MyPrecious(self.name + '_a.md2')
        self.file_b = MyPrecious(self.name + '_b.md2')
        self.file_comp = MyPrecious(self.name + '_comp.md2')

    def data_logic(self, data_point):
        if data_point.dec < self.min_dec or data_point.dec > self.max_dec:
            if self.outside:
                return Comm.BEEP
            else:
                self.write('*')
                self.outside = True
                return Comm.BEEP
        else:
            self.outside = False
            self.write_data(data_point)
            return Comm.NO_ACTION

class Spectrum(Observation):
    """for all your spectrum observation needs"""

    def __init__(self):
        super().__init__()
        self.obs_type   = "Spectrum"

        self.cal_dur    = 20
        self.bg_dur     = 20

        self.cal_freq   = 3
        self.data_freq  = 10

        # These are the radio frequency (e.g. 1319.5 Mhz), not the sampling frequency!
        self.interval   = 1
        self.freq_time  = None
        
    def set_RA(self, start_RA, end_RA):
        return super().set_RA(start_RA, start_RA + 180)
        
    def set_data_time(self, data_start, data_end):
        return super().set_data_time(data_start, data_start + 180)

    def set_files(self):
        self.file_a = MyPrecious(self.name + '_a.md1')
        self.file_b = MyPrecious(self.name + '_b.md1')
        self.file_comp = MyPrecious(self.name + '_comp.md1')

    def data_logic(self, data_point):
        if self.freq_time is None:
            self.freq_time = time.time()
            self.write_data(data_point)
            return Comm.NO_ACTION
        elif time.time() - self.freq_time < self.interval:
            self.write_data(data_point)
            return Comm.NO_ACTION
        else:
            self.last_change = time.time()
            self.write_data(data_point)
            return Comm.BEEP

def get_date(epoch_time) -> str:
    return time.strftime('%m/%d/%Y', time.localtime(epoch_time))

def get_time(epoch_time) -> str:
    return time.strftime('%I:%M:%S %p', time.localtime(epoch_time))