"""clock for keeping track of the time ;)"""

import time, datetime


class SuperClock:
    """Clock object for encapsulation; keeps track of the time(tm)"""

    SIDEREAL = 1.00273790935  # the number of sidereal seconds per second
    LONGITUDE = 38.437235

    class Timer:
        def __init__(self, period: float, callback):
            """
            Args:
                period (int): in milliseconds
                callback (function): function to call when the timer runs

            Attributes:
                offset (int): the number of times the timer has run
            """
            self.period = float(period)
            self.offset = 0
            self.callback = callback

        def run(self):
            self.callback()

        def run_if_appropriate(self, starting_time):
            while time.time() > (
                starting_time + (self.period / 1000) * (self.offset + 1)
            ):
                self.offset += 1

            if self.period > 0 and (
                time.time() >= (starting_time + (self.period / 1000) * self.offset)
            ):
                self.run()
                self.offset += 1
                return True
            return False

        def set_period(self, new_period):
            """
            Args:
                new_period (int): in milliseconds
            """
            self.period = new_period

        def cancel(self):
            self.period = 0

        def __repr__(self):
            return f"Timer({self.period}ms, {self.callback})"

    def __init__(self):
        self.starting_time = time.time()
        self.starting_sidereal_time = (
            # TODO: is this still used?
            0  # number of seconds since last sidereal midnight
        )

        self.timers = []

    def run_timers(self):
        """run all timers"""
        for timer in self.timers:
            timer.run_if_appropriate(self.starting_time)

    def add_timer(self, period, callback):
        """set a timer to call a function periodically"""
        new_timer = SuperClock.Timer(period, callback)
        self.timers.append(new_timer)
        return new_timer

    def get_time(self):
        return time.time()

    def get_time_slug(self):
        """get timestamp suitable for file naming"""
        gmtime = self.get_local_time()
        return "{:%Y.%m.%d-%H.%M}".format(datetime.datetime(*gmtime[:5]))

    def get_elapsed_time(self):
        return time.time() - self.starting_time

    def get_time_until(self, destination_time):
        """Positive means it already happened, negative means it will happen"""
        return time.time() - destination_time

    def get_local_time(self):
        return time.localtime(time.time())

    def get_sidereal_seconds(self):
        """get time-stamp-able number of sidereal seconds since last sidereal midnight"""
        sidereal_seconds = self.starting_sidereal_time + self.SIDEREAL * (
            self.get_elapsed_time()
        )
        return sidereal_seconds

    def get_sidereal_time(self):
        """return a string of formatted local sidereal time"""
        current_sidereal_time = self.get_sidereal_seconds()
        minutes, seconds = divmod(current_sidereal_time, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24
        sidereal = "%02d:%02d:%02d" % (hours, minutes, seconds)
        return sidereal
