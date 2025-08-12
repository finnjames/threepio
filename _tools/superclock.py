"""Clock for keeping track of the time and running functions at different intervals"""

from __future__ import annotations
from math import floor
import time
import datetime
from typing import Callable
from astropy.time import Time
from astropy.coordinates import EarthLocation

SIDEREAL = 1.00273790935  # The number of sidereal seconds per second
GB_LATITUDE = 38.437235  # North
GB_LONGITUDE = -79.839835  # West (so negative)


class SuperClock:
    """Clock object for encapsulation; keeps track of the time(tm)"""

    def __init__(self):
        self.timers = []
        current_time = SuperClock.get_time()
        self.starting_epoch_time: float = 0.0
        self.anchor_time: float = 0.0
        # Time, in seconds, since the sidereal midnight before last calibration
        self.starting_sidereal_time = 0.0

        loc = EarthLocation(lat=GB_LATITUDE, lon=GB_LONGITUDE)
        t = Time(time.time(), format="unix", scale="utc", location=loc)
        current_ra = SuperClock.hours_to_seconds(t.sidereal_time("apparent").value)
        self.calibrate_sidereal_time(current_ra)

    def calibrate_sidereal_time(self, starting_sidereal_time: float):
        current_time = time.time()
        corrected_sidereal_time = (starting_sidereal_time) % 86400

        self.set_starting_time(current_time)
        self.set_starting_sidereal_time(corrected_sidereal_time)

        print(f"{self.starting_sidereal_time=}, {self.starting_epoch_time=}")

    @staticmethod
    def get_time() -> float:
        return time.time()

    @staticmethod
    def solar_to_sidereal(solar_seconds: float) -> float:
        return solar_seconds * SIDEREAL

    @staticmethod
    def sidereal_to_solar(sidereal_seconds: float) -> float:
        return sidereal_seconds / SIDEREAL

    @staticmethod
    def get_time_slug() -> str:
        """Get timestamp suitable for file naming"""
        return "{:%Y.%m.%d-%H.%M}".format(datetime.datetime(*time.localtime()[:5]))

    @staticmethod
    def get_time_until(destination_time) -> float:
        """Positive means it already happened, negative means it will happen"""
        return time.time() - destination_time

    @staticmethod
    def deformat_time_string(time_string: str) -> float:
        """Convert a string of the form HH:MM:SS to a float of seconds"""
        hours, minutes, seconds = map(float, time_string.split(":"))
        return hours * 3600 + minutes * 60 + seconds
    
    @staticmethod
    def hours_to_seconds(hours: float) -> float:
        return hours * 3600
    
    def run_timers(self) -> None:
        """Run every timer that is due to run"""
        for timer in self.timers:
            timer.run_if_appropriate(self.anchor_time)

    def reset_all_timer_offsets(self) -> None:
        """Set offset of all timers to 0"""
        for timer in self.timers:
            timer.offset = 0

    def add_timer(self, period: int, callback, name="", log=False) -> Timer:
        """Set a timer to call a function periodically"""
        new_timer = Timer(period, callback, name, log)
        self.timers.append(new_timer)
        return new_timer

    def set_starting_sidereal_time(self, sidereal_time: float) -> None:
        self.starting_sidereal_time = sidereal_time

    def set_starting_time(self, epoch_time: float) -> None:
        """Set starting time and anchor time to specified time"""
        self.starting_epoch_time = epoch_time
        self.anchor_time = epoch_time
        self.reset_all_timer_offsets()

    def reset_anchor_time(self) -> None:
        """Set anchor time to current time"""
        self.anchor_time = time.time()
        self.reset_all_timer_offsets()

    def get_elapsed_time(self) -> float:
        return time.time() - self.starting_epoch_time

    def get_starting_epoch_time(self) -> float:
        """Solar time of last calibration as epoch date"""
        return self.starting_epoch_time

    def get_starting_sidereal_time(self) -> float:
        """Sidereal time of last calibration in seconds"""
        return self.starting_sidereal_time
    
    def get_sidereal_seconds(self) -> float:
        """Sidereal seconds since the sidereal midnight before calibration"""
        return self.starting_sidereal_time + SIDEREAL * self.get_elapsed_time()

    def get_sidereal_tuple(self) -> tuple:
        """Return an hours, minutes, seconds tuple of local sidereal time"""
        current_sidereal_time = self.get_sidereal_seconds()
        minutes, seconds = divmod(current_sidereal_time, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24
        return hours, minutes, seconds

    def get_formatted_sidereal_time(self) -> str:
        """Return a string of HH:MM:SS formatted local sidereal time"""
        hours, minutes, seconds = self.get_sidereal_tuple()
        return f"{hours:02.0f}:{minutes:02.0f}:{seconds:02.0f}"


class Timer:
    """A timer for syncing things that run at different, variable rates
    
    Args:
        period (int): in milliseconds
        callback (Callable[[], None]): function to call when the timer runs
        name (str): name of the timer
        log (bool): whether to print the timer's name and status when it runs
    """

    def __init__(self, period: int, callback: Callable[[], None], name: str, log: bool):
        self.period = period  # ms
        self.callback = callback
        self.offset = 0
        self.name = name
        self.log = log

    def run(self) -> None:
        self.callback()

    def run_if_appropriate(self, anchor_time: float) -> bool:
        if self.period <= 0:
            return False
        current_time = time.time()

        # TODO: This works, right?
        if current_time > anchor_time + (self.period / 1000) * (self.offset + 1):
            self.offset = floor((current_time - anchor_time) / (self.period / 1000))

        if current_time >= (anchor_time + (self.period / 1000) * self.offset):
            if self.log:  # TODO: Should this be in production?
                print(f"{self.name}: {self.offset=}, {anchor_time=}, {current_time=}")
            self.run()
            self.offset += 1
            return True
        return False

    def set_period(self, new_period: int) -> None:
        """
        Args:
            new_period (int): in milliseconds
        """
        if self.period != new_period:
            self.offset = 0
        self.period = new_period

    def cancel(self) -> None:
        self.period = 0

    def __repr__(self) -> str:
        return f"Timer({self.period}ms, {self.callback})"
