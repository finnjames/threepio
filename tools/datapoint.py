class DataPoint:
    """each data point taken (timestamp, dec, a, b)"""

    def __init__(self, timestamp, dec, a, b):
        self.timestamp = timestamp
        self.dec = dec
        self.a = a
        self.b = b

    def with_int_time(self):
        print(round(self.dec))
        return DataPoint(round(self.timestamp), self.dec, self.a, self.b)

    def to_tuple(self):
        return self.timestamp, self.dec, self.a, self.b
