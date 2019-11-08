"""clock for keeping track of the time ;)"""

from PyQt5 import QtCore, QtWidgets, QtGui, QtChart
from astropy.time import Time 
from astropy.coordinates import Longitude
import time

class SuperClock():
    """Clock object for encapsulation; keeps track of the time(tm)"""
    
    SIDEREAL = 1.00273790935
    LONGITUDE = 38.437235
    
    def __init__(self, starting_sidereal_time = time.time()):
        self.starting_time = time.time()
        self.starting_sidereal_time = starting_sidereal_time
    
    def get_time(self):
        return time.time()
    
    def get_time_until(self, destination_time): # TODO: this should be sidereal
        return time.time() - destination_time
    
    def get_local_time(self):
        return time.localtime(time.time())
    
    def get_sidereal_time(self): # TODO: make this actually be sidereal
        astro_time = Time(time.time(), format="unix")
        # sidereal = astro_time.sidereal_time("apparent", longitude=self.LONGITUDE, model='IAU2000A')
        # print(sidereal)
        sidereal = Time(time.time(), format="unix")
        return sidereal.fits[-12:][:11] # TODO: make this less wack