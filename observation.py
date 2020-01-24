import time

from datapoint import DataPoint
from precious import MyPrecious

class Observation():
    """Superclass for each of the three types of observation you might encounter on your Pokemon journey"""
    
    def __init__(self, name, start_RA, end_RA, max_dec, min_dec):
        self.name       = name
        self.composite  = False
        self.state      = "STOPPED"
        
        self.start_RA   = start_RA
        self.end_RA     = end_RA
        self.max_dec    = max_dec     # if only one dec, this is it
        self.min_dec    = min_dec

        self.start_time = None
        self.end_time   = None
        self.data_start = None
        self.data_end   = None

        # Temporary bookkeeping
        self.cal_start  = None
        self.bg_start   = None
        
        # The data list, for backup
        self.data       = []
    
    # This is the communication API
    def communicate(self, data_point):
        if self.state == "STOPPED":
            if time.time() < self.start_RA - 120:
                return 0
            else:
                return "Please start calibration"
        elif self.state == "CAL ON 1":
            if time.time() - self.cal_start < 60:
                self.write_data(data_point)
                return 0
            else:
                return "Please turn off calibration"
        elif self.state == "BG 1":
            if time.time() - self.bg_start < 60:
                self.write_data(data_point)
                return 0
            else:
                return "Starting to collect data"
        elif self.state == "DATA":
            if time.time() < self.end_RA:
                return self.data_logic(data_point)
            else:
                return "Please start calibration"
        elif self.state == "CAL ON 2":
            if time.time() - self.cal_start < 60:
                self.write_data(data_point)
                return 0
            else:
                return "Please turn off calibration"
        elif self.state == "BG 2":
            if time.time() - self.bg_start < 60:
                self.write_data(data_point)
                return 0
            else:
                return "Finished"
        elif self.state == "FINISHED":
            return "Observation is already finished"

    # These are the action APIs
    def start(self):
        self.state = "CAL ON 1"
        self.start_time = time.time()
        self.cal_start = time.time()

    def end_calibration_1(self):
        self.state = "BG 1"
        self.write('*')
        self.bg_start = time.time()
        
    def end_background_1(self):
        self.state = "DATA"
        self.write('*')
        self.data_start = time.time()

    def end_data(self):
        self.state = "CAL ON 2"
        self.write('*')
        self.data_end = time.time()
        self.cal_start = time.time()

    def end_calibration_2(self):
        self.state = "BG 2"
        self.write('*')
        self.bg_start = time.time()

    def stop(self):
        self.state = "Finished"
        self.end_time = time.time()
        self.write('*')
        self.write('*')
        self.write_meta()

    ############################ Helpers ############################
    def set_RA(self, start_RA, end_RA):
        self.start_RA = start_RA
        self.end_RA = end_RA
    
    def set_dec(self, max_dec, min_dec):
        self.max_dec = max_dec
        self.min_dec = min_dec
        
    def set_files(self, extension):
        self.file_a = MyPrecious(self.name + '_a' + extension)
        self.file_b = MyPrecious(self.name + '_b' + extension)
        self.file_comp = MyPrecious(self.name + '_comp' + extension)

    def get_last_data(self):
        return self.data[len(self.data) - 1]

    def data_logic(self, data_point):
        pass

    def write(self, string: str):
        if self.composite:
            self.file_comp.write(string)
        else:
            self.file_a.write(string)
            self.file_b.write(string)

    def write_data(self, point: DataPoint):
        if self.composite:
            self.file_comp.write(point.timestamp)
            self.file_comp.write(point.dec)
            self.file_comp.write(point.a)
            self.file_comp.write(point.b)
        else:
            self.file_a.write(point.timestamp)
            self.file_a.write(point.dec)
            self.file_a.write(point.a)
            self.file_b.write(point.timestamp)
            self.file_b.write(point.dec)
            self.file_b.write(point.b)

    def write_meta(self):
        self.write('TELESCOPE: The Mighty Forty')
        self.write('LOCAL START DATE: ' + str(self.start_time.date()))
        self.write('LOCAL START TIME: ' + str(self.start_time.time()))
        self.write('LOCAL STOP DATE: '  + str(self.end_time.date()))
        self.write('LOCAL STOP TIME: '  + str(self.end_time.time()))

class Scan(Observation):
    """Set a start and end RA"""

    def __init__(self, name, start_RA, end_RA, max_dec, min_dec):
        super().__init__(name, start_RA, end_RA, max_dec, min_dec)
        self.set_files('.md1')

    def data_logic(self, data_point):
        self.write_data(data_point)
        return 0

class Survey(Observation):
    """Set a region in sky using start and end RA/DEC"""

    def __init__(self, name, start_RA, end_RA, max_dec, min_dec):
        super().__init__(name, start_RA, end_RA, max_dec, min_dec)
        self.set_files('.md2')
        self.out_boundary = False
        
    def data_logic(self, data_point):
        if data_point.dec < self.min_dec or data_point.dec > self.max_dec:
            if self.out_boundary:
                return "Beep!"
            else:
                self.write('*')
                self.out_boundary = True
                return "Beep!"
        else:
            self.out_boundary = False
            self.write_data(data_point)
            return 0

class Spectrum(Observation):
    """for all your spectrum observation needs"""

    def __init__(self, name, start_RA, end_RA, max_dec, min_dec):
        super().__init__(name, start_RA, end_RA, max_dec, min_dec)
        self.set_files('.md2')
        
    def data_logic(self, data_point):
        pass