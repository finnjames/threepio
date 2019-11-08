"""classes for the three types of observations as well as DataPoint"""

class Observation():
    """superclass for each of the three types of observation you might encounter on your Pokemon journey"""
    
    obs_type = None
    
    data = []
    written_to = -1
    
    start_RA = 0
    end_RA = 0
    start_dec = 0 # if only one dec, this is it
    end_dec = 0
    
    def __init__(self):
        pass
    
    def set_RA(self, start_RA, end_RA):
        self.start_RA = start_RA
        self.end_RA = end_RA
    
    def set_dec(self, start_dec, end_dec):
        self.start_dec = start_dec
        self.end_dec = end_dec
        
    def set_precious(self, precious):
        self.precious = precious
    
    def add_data(self, data_point):
        self.data.append(data_point)
    
    def get_last_data(self):
        return self.data[len(self.data) - 1]
    
    # TODO: implement MyPrecious encapsulation


class Scan(Observation):
    """for all your scan observation needs"""
    obs_type = "Scan"
    data = []
    
    def set_dec(self, start_dec, end_dec):
        self.start_dec = start_dec

class Survey(Observation):
    """for all your survey observation needs"""
    obs_type = "Survey"
    data = []

class Spectrum(Observation):
    """for all your spectrum observation needs"""
    obs_type = "Spectrum"
    data = []
    
    def set_dec(self, start_dec, end_dec):
        self.start_dec = start_dec

class DataPoint():
    """each data point taken, has a timestamp and two voltage channels"""
    def __init__(self, timestamp, a, b, dec):
        self.timestamp = timestamp
        self.a = a
        self.b = b
        self.dec = dec
        
    def to_tuple(self):
        return (self.timestamp, self.a, self.b, self.dec)