"""clock for keeping track of the time ;)"""

import time
import datetime
from typing import Callable


class SuperClock:
    """Clock object for encapsulation; keeps track of the time(tm)"""

    SIDEREAL = 1.00273790935  # the number of sidereal seconds per second
    GB_LATITUDE = 38.437235

    class Timer:

        """A timer for syncing things that run at different, variable rates

        Attributes:
            offset (int): the number of times the timer has run
        """

        def __init__(self, period: float, callback: Callable[[], None]):
            """
            Args:
                period (int): in milliseconds
                callback (Callable): function to call when the timer runs
            """
            self.period = float(period)  # ms
            self.callback = callback
            self.offset = 0

        def run(self) -> None:
            self.callback()

        def run_if_appropriate(self, anchor_time: float) -> bool:
            while time.time() > (
                anchor_time + (self.period / 1000) * (self.offset + 1)
            ):
                self.offset += 1  # can this be done in O(1)?

            if self.period > 0 and (
                time.time() >= (anchor_time + (self.period / 1000) * self.offset)
            ):
                self.run()
                self.offset += 1
                return True
            return False

        def set_period(self, new_period) -> None:
            """
            Args:
                new_period (int): in milliseconds
            """
            if self.period != new_period:
                self.offset = 0
            self.period = new_period

        def cancel(self) -> None:
            self.period = 0.0

        def __repr__(self) -> str:
            return f"Timer({self.period}ms, {self.callback})"

    def __init__(self):
        self.timers = []
        self.starting_time = None
        self.anchor_time = None
        self.set_starting_time(time.time())
        # number of seconds since last sidereal midnight, assigned when ra is set
        self.starting_sidereal_time = 0

    @staticmethod
    def get_time() -> float:
        return time.time()

    @staticmethod
    def solar_to_sidereal(solar_seconds: float) -> float:
        return solar_seconds * SuperClock.SIDEREAL

    @staticmethod
    def sidereal_to_solar(sidereal_seconds: float) -> float:
        return sidereal_seconds / SuperClock.SIDEREAL

    def run_timers(self) -> None:
        """run all timers"""
        for timer in self.timers:
            timer.run_if_appropriate(self.anchor_time)

    def reset_timers(self) -> None:
        """set offset of all timers to 0"""
        for timer in self.timers:
            timer.offset = 0

    def add_timer(self, period, callback) -> Timer:
        """set a timer to call a function periodically"""
        new_timer = SuperClock.Timer(period, callback)
        self.timers.append(new_timer)
        return new_timer

    def get_starting_time(self) -> float:
        return self.starting_time

    def set_starting_sidereal_time(self, sidereal_time: int) -> None:
        self.starting_sidereal_time = sidereal_time

    def set_starting_time(self, epoch_time) -> None:
        """set starting time and anchor time to specified time"""
        if epoch_time is None:
            epoch_time = time.time()
        self.starting_time = self.anchor_time = epoch_time
        self.reset_timers()

    def reset_anchor_time(self) -> None:
        """set anchor time to current time"""
        self.anchor_time = time.time()
        self.reset_timers()

    def get_local_time(self) -> time.struct_time:
        return time.localtime(self.get_time())

    def get_time_slug(self) -> str:
        """get timestamp suitable for file naming"""
        gmtime = self.get_local_time()
        return "{:%Y.%m.%d-%H.%M}".format(datetime.datetime(*gmtime[:5]))

    def get_time_until(self, destination_time) -> float:
        """Positive means it already happened, negative means it will happen"""
        return self.get_time() - destination_time

    def get_elapsed_time(self) -> float:
        return self.get_time() - self.starting_time

    def get_sidereal_seconds(self) -> float:
        """get timestamp-able number of sidereal seconds since last sidereal midnight"""
        return (
            self.starting_sidereal_time + SuperClock.SIDEREAL * self.get_elapsed_time()
        )

    def get_solar_seconds(self) -> float:
        """sidereal_to_solar(get_sidereal_seconds())"""
        return self.sidereal_to_solar(self.get_sidereal_seconds())

    def get_sidereal_tuple(self) -> tuple:
        """return a tuple of local sidereal time"""
        current_sidereal_time = self.get_sidereal_seconds()
        minutes, seconds = divmod(current_sidereal_time, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24
        return hours, minutes, seconds

    def get_formatted_sidereal_time(self) -> str:
        """return a string of formatted local sidereal time"""
        hours, minutes, seconds = self.get_sidereal_tuple()
        return f"{hours:02.0f}:{minutes:02.0f}:{seconds:02.0f}"
