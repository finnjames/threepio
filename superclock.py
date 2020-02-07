"""clock for keeping track of the time ;)"""

from PyQt5 import QtCore, QtWidgets, QtGui, QtChart
from astropy.time import Time 
from astropy.coordinates import Longitude
import time

class SuperClock():
    """Clock object for encapsulation; keeps track of the time(tm)"""
    
    SIDEREAL = 1.00273790935 # the number of sidereal seconds per second
    LONGITUDE = 38.437235
    
    def __init__(self):
        self.starting_time = time.time()
        self.starting_sidereal_time = self.starting_time
        
    def get_time(self):
        return time.time()
    
    def get_elapsed_time(self):
        return time.time() - self.starting_time
    
    def get_time_until(self, destination_time): # TODO: this should be sidereal
        return time.time() - destination_time
    
    def get_local_time(self):
        return time.localtime(time.time())
    
    def get_sidereal_time(self): 
        """return a string of formatted local sidereal time"""
        current_sidereal_time = self.starting_sidereal_time + self.SIDEREAL*(self.get_elapsed_time())
        hours = time.localtime(current_sidereal_time)[3]
        minutes = time.localtime(current_sidereal_time)[4]
        seconds = time.localtime(current_sidereal_time)[5]
        sidereal = "%02d:%02d:%02d" % (hours, minutes, seconds)
        return sidereal
    
    def get_sidereal_seconds(self):
        epoch_date = time.localtime(self.starting_time)
        sidereal_seconds = 3600*epoch_date[3] + 60*epoch_date[4] + epoch_date[5]
        sidereal_seconds = self.SIDEREAL * (sidereal_seconds + (self.get_elapsed_time()))
        return sidereal_seconds