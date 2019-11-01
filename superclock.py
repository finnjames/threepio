from PyQt5 import QtCore, QtWidgets, QtGui, QtChart
from astropy.time import Time
import time

class SuperClock():
    """Clock object for encapsulation; keeps track of the time(tm)"""
    
    SIDEREAL = 1.00273790935
    
    def __init__(self, starting_sidereal_time = time.time()):
        self.starting_time = time.time()
        self.starting_sidereal_time = starting_sidereal_time
    
    def get_time(self):
        return time.time()
    
    def get_elapsed_time(self):
        return time.time() - self.starting_time
    
    def get_time_until(self, destination_time):
        return time.time() - destination_time
    
    def get_local_time(self):
        return time.localtime(time.time())
    
    def get_sidereal_time(self): # TODO: make this actually be sidereal
        sidereal = self.starting_sidereal_time + ((time.time() - self.starting_time) * self.SIDEREAL)
        # print(time.time(), sidereal)
        sidereal = Time(sidereal, format="unix")
        return sidereal.fits[-12:][:11] # TODO: make this less wack