"""clock for keeping track of the time ;)"""

import time, datetime
from typing import Callable


class SuperClock:
    """Clock object for encapsulation; keeps track of the time(tm)"""

    SIDEREAL = 1.00273790935  # the number of sidereal seconds per second
    GB_LATITUDE = 38.437235

    class Timer:
        def __init__(self, period: float, callback: Callable[[], None]):
            """
            Args:
                period (int): in milliseconds
                callback (Callable): function to call when the timer runs

            Attributes:
                offset (int): the number of times the timer has run
            """
            self.period = float(period)  # ms
            self.offset = 0
            self.callback = callback

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
        self.starting_time = self.anchor_time = time.time()
        # number of seconds since last sidereal midnight, assigned when ra is set
        self.starting_sidereal_time = 0

        self.timers = []

    def get_time(self) -> float:
        return time.time()

    def run_timers(self) -> None:
        """run all timers"""
        for timer in self.timers:
            timer.run_if_appropriate(self.anchor_time)

    def reset_timers(self) -> None:
        """set offset of all timers to 0"""
        for timer in self.timers:
            timer.offset = 0

    def add_timer(self, period, callback) -> None:
        """set a timer to call a function periodically"""
        new_timer = SuperClock.Timer(period, callback)
        self.timers.append(new_timer)
        return new_timer

    def reset_starting_time(self) -> None:
        """set SuperClock starting time and anchor time to current time"""
        self.starting_time = self.anchor_time = time.time()
        self.reset_timers()

    def reset_anchor_time(self) -> None:
        """set anchor time to current time"""
        self.anchor_time = time.time()
        self.reset_timers()

    def get_local_time(self) -> time.struct_time:
        return time.localtime(time.time())

    def get_time_slug(self) -> str:
        """get timestamp suitable for file naming"""
        gmtime = self.get_local_time()
        return "{:%Y.%m.%d-%H.%M}".format(datetime.datetime(*gmtime[:5]))

    def get_elapsed_time(self) -> float:
        return time.time() - self.starting_time

    def get_time_until(self, destination_time) -> float:
        """Positive means it already happened, negative means it will happen"""
        return time.time() - destination_time

    def get_sidereal_seconds(self) -> float:
        """get time-stamp-able number of sidereal seconds since last sidereal midnight"""
        sidereal_seconds = (
            self.starting_sidereal_time + self.SIDEREAL * self.get_elapsed_time()
        )
        return sidereal_seconds

    def get_sidereal_time(self) -> str:
        """return a string of formatted local sidereal time"""
        current_sidereal_time = self.get_sidereal_seconds()
        minutes, seconds = divmod(current_sidereal_time, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24
        sidereal = "%02d:%02d:%02d" % (hours, minutes, seconds)
        return sidereal
