from datetime import datetime

class Observation():
    """superclass for each of the three types of observation you might encounter on your Pokemon journey"""
    
    obs_type = None
    
    def __init__(self):
        self.data = []
        self.written_to = -1
        self.calibration = False
        
        self.start_RA   = 0
        self.end_RA     = 0
        self.start_dec  = 0     # if only one dec, this is it
        self.end_dec    = 0

        self.start_time = None
        self.end_time   = None
    
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
    def start(self):
        self.start_time = datetime.now()

    def stop(self):
        self.end_time = datetime.now()
        self.precious.write('*')
        self.precious.write('*')
        self.write_meta()

    def write(self, list_of_data: list):
        """
        Take in a list of DataPoints. Each has four values: 
        RA, DEC, and voltages from the two channels.
        """
        for point in list_of_data:
            self.precious.write(point.timestamp)
            self.precious.write(point.dec)
            self.precious.write(point.a)
            self.precious.write(point.b)

    def write_meta(self):
        self.precious.write('TELESCOPE: The Mighty Forty')
        self.precious.write('LOCAL START DATE: ' + str(self.start_time.date()))
        self.precious.write('LOCAL START TIME: ' + str(self.start_time.time()))
        self.precious.write('LOCAL STOP DATE: '  + str(self.end_time.date()))
        self.precious.write('LOCAL STOP TIME: '  + str(self.end_time.time()))

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