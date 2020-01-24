from datetime import datetime
import time
from datapoint import DataPoint

class Observation():
    """superclass for each of the three types of observation you might encounter on your Pokemon journey"""
    
    obs_type = None
    
    def __init__(self, name, start_RA, end_RA, start_dec, end_dec):
        self.name       = name
        self.data       = []
        self.compsite   = False
        self.state      = "STOPPED"
        
        self.start_RA   = start_RA
        self.end_RA     = end_RA
        self.start_dec  = start_dec     # if only one dec, this is it
        self.end_dec    = end_dec

        self.start_time = None
        self.end_time   = None
        self.data_start = None
        self.data_end   = None

        # Temporary bookkeeping
        self.cal_start  = None
        self.bg_start   = None

    def data_logic(self, data_point):
        pass
    
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

    def set_RA(self, start_RA, end_RA):
        self.start_RA = start_RA
        self.end_RA = end_RA
    
    def set_dec(self, start_dec, end_dec):
        self.start_dec = start_dec
        self.end_dec = end_dec
        
    def set_files(self, extension):
        self.file_a = self.name + '_a' + extension
        self.file_b = self.name + '_b' + extension
        self.file_comp = self.name + '_comp' + extension
    
    def get_last_data(self):
        return self.data[len(self.data) - 1]
    
    # TODO: implement MyPrecious encapsulation
    def start(self):
        self.state = "CAL ON 1"
        self.start_time = time.time()
        self.cal_start = time.time()

    def end_calibration_1(self):
        self.state = "BG 1"
        if self.compsite:
            self.file_comp.write('*')
        else:
            self.file_a.write('*')
            self.file_b.write('*')
        self.bg_start = time.time()
        
    def end_background_1(self):
        self.state = "DATA"
        if self.compsite:
            self.file_comp.write('*')
        else:
            self.file_a.write('*')
            self.file_b.write('*')
        self.data_start = time.time()

    def end_data(self):
        self.state = "CAL ON 2"
        if self.compsite:
            self.file_comp.write('*')
        else:
            self.file_a.write('*')
            self.file_b.write('*')
        self.data_end = time.time()
        self.cal_start = time.time()

    def end_calibration_2(self):
        self.state = "BG 2"
        if self.compsite:
            self.file_comp.write('*')
        else:
            self.file_a.write('*')
            self.file_b.write('*')
        self.bg_start = time.time()

    def end_background_2(self):
        self.stop()
        self.state = "Finished"
        
    def stop(self):
        self.state = "STOPPED"
        self.end_time = time.time()
        if self.compsite:
            self.file_comp.write('*')
            self.file_comp.write('*')
        else:
            self.file_a.write('*')
            self.file_a.write('*')
            self.file_b.write('*')
            self.file_b.write('*')
        self.write_meta()

    def write_data(self, point: DataPoint):
        self.data.append(point)
        if self.compsite:
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
        if self.compsite:
            self.file_comp.write('TELESCOPE: The Mighty Forty')
            self.file_comp.write('LOCAL START DATE: ' + str(self.start_time.date()))
            self.file_comp.write('LOCAL START TIME: ' + str(self.start_time.time()))
            self.file_comp.write('LOCAL STOP DATE: '  + str(self.end_time.date()))
            self.file_comp.write('LOCAL STOP TIME: '  + str(self.end_time.time()))
        else:
            self.file_a.write('TELESCOPE: The Mighty Forty')
            self.file_a.write('LOCAL START DATE: ' + str(self.start_time.date()))
            self.file_a.write('LOCAL START TIME: ' + str(self.start_time.time()))
            self.file_a.write('LOCAL STOP DATE: '  + str(self.end_time.date()))
            self.file_a.write('LOCAL STOP TIME: '  + str(self.end_time.time()))
            self.file_b.write('TELESCOPE: The Mighty Forty')
            self.file_b.write('LOCAL START DATE: ' + str(self.start_time.date()))
            self.file_b.write('LOCAL START TIME: ' + str(self.start_time.time()))
            self.file_b.write('LOCAL STOP DATE: '  + str(self.end_time.date()))
            self.file_b.write('LOCAL STOP TIME: '  + str(self.end_time.time()))

class Scan(Observation):
    """Set a start and end RA"""

    def __init__(self, name, start_RA, end_RA, start_dec, end_dec):
        super().__init__(name, start_RA, end_RA, start_dec, end_dec)
        self.set_files('.md1')

    def data_logic(self, data_point):
        self.write_data(data_point)
        return 0

class Survey(Observation):
    """Set a region in sky using start and end RA/DEC"""

    def __init__(self, name, start_RA, end_RA, start_dec, end_dec):
        super().__init__(name, start_RA, end_RA, start_dec, end_dec)
        self.set_files('.md2')
        
    def data_logic(self, data_point):
        pass

class Spectrum(Observation):
    """for all your spectrum observation needs"""

    def __init__(self, name, start_RA, end_RA, start_dec, end_dec):
        super().__init__(name, start_RA, end_RA, start_dec, end_dec)
        self.set_files('.md2')
        
    def data_logic(self, data_point):
        pass