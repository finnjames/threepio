
class DataPoint():
    """each data point taken, has a timestamp, a dec value, and two voltage channels"""
    def __init__(self, timestamp, a, b, dec):
        self.timestamp = timestamp
        self.a = a
        self.b = b
        self.dec = dec
        
    def to_tuple(self):
        return (self.timestamp, self.a, self.b, self.dec)