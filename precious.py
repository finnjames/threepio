"""
Functionalities needed for working with files.
"""

from datetime import datetime

class MyPrecious:
    def __init__(self, filename: str):
        self.filename = filename
        self.buffer = []

    # Use the following functions for interacting with the file.
    def write_data(self, data: tuple):
        """
        This function accepts a tuple of values and append them to the output buffer
        one value per line. A tuple should represent one single data point with its
        values being RA, DEC and the voltage read.
        """
        for val in data:
            self.buffer_append(str(val))
    
    def write_sep(self):
        """
        Use this function for separation for calibration, turing points, etc.
        """
        self.buffer_append('*')

    def write_meta(self, start_datetime: datetime, stop_datetime: datetime):
        """
        Append meta data about the file. Use this function once with 
        """
        self.buffer_append('TELESCOPE: The Mighty Forty')
        self.buffer_append('LOCAL START DATE: ' + str(start_datetime.date()))
        self.buffer_append('LOCAL START TIME: ' + str(start_datetime.time()))
        self.buffer_append('LOCAL STOP DATE: ' + str(stop_datetime.date()))
        self.buffer_append('LOCAL STOP TIME: ' + str(stop_datetime.time()))

    def buffer_clear(self):
        self.buffer = []

    def buffer_append(self, data: str):
        self.buffer.append(data)

    def buffer_write(self):
        self.file_append('\n'.join(self.buffer))
        self.buffer_clear()

    def file_write(self, data, mode='a'):
        if mode != 'a' and mode != 'w':
            print("Write mode not recognized. Please use " +
            "'a' for append and 'w' for write (overwrite).")
        with open(self.filename, mode) as file:
            print(data, end='\n', file=file)

    def file_overwrite(self, data):
        self.file_write(data, mode='w')

    def file_append(self, data):
        self.file_write(data, mode='a')