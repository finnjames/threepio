"""
This module includes a Tars class that encapsulate a serialpy object and provides
simple methods for initializing, starting, stopping, resetting, and reading from
the DATAQ device connected via a USB serial connection. The module also includes
a few helper functions relevant to the tasks.
"""

from typing import Optional

import serial
from .myserial import MySerial
import serial.tools.list_ports
import time

import random as r  # for testing
import math


def discovery() -> tuple:
    # Get a list of active com ports to scan for possible DATAQ Instruments devices
    available_ports = serial.tools.list_ports.comports()

    dataq = None
    declinometer = None
    for p in available_ports:
        if "VID:PID=0683:4109" in p.hwid:
            dataq = p.device
        if "VID:PID=0403:6001" in p.hwid:
            declinometer = p.device

    return dataq, declinometer


def convert(buffer: list, volt: int) -> float:
    return volt * int.from_bytes(buffer, byteorder="little", signed=True) / 32768


class Tars:
    """
    A wrapper class of a serial object which supports functionalities
    specifically useful for DATAQ instruments.
    """

    RANGE_VOLT = (10, 5, 2, 1, 0.5, 0.2)
    RANGE_RATE = (50000, 20000, 10000, 5000, 2000, 1000, 500, 200, 100, 50, 20, 10)

    def __init__(self, parent=None, device=None):
        self.parent = parent
        if device is not None:
            self.testing = False

            self.ser = MySerial(device)
            self.channels = [
                0x0100,  # channel 0, telescope channel A, ±5 V range
                0x0101,  # channel 1, telescope channel B, ±5 V range
                0x0102,  # channel 2, declinometer, ±5 V range
            ]
            self.acquiring = False

            self.setup()
        else:
            self.testing = True
            self.parent.log("DataQ not found, simulating data")

    def start(self):
        if not self.testing:
            self.send("start")
            self.acquiring = True

    def reset(self):
        if not self.testing:
            self.send("reset 1")

    def stop(self):
        if not self.testing:
            self.send("stop")
            self.ser.reset_input_buffer()
            self.acquiring = False

    def read_one(self) -> Optional[list]:
        """
        This reads one datapoint from the buffer. Each datapoint has three channels:
        channel 0: telescope channel A
        channel 1: telescope channel B
        channel 2: declinometer
        """
        if self.testing:
            return self.random_data()

        if self.in_waiting() < (2 * len(self.channels)):
            return None
        return [
            (channel & 3, self.buffer_read(channel)) for channel in self.channels
        ]

    def read_latest(self) -> list:
        """
        This function reads the last datapoint from the buffer and clears the buffer.
        Use this as a real-time sampling method. Each datapoint has three channels:
        channel 0: telescope channel A
        channel 1: telescope channel B
        channel 2, declinometer
        """
        if not self.testing:
            current = self.read_one()
            latest = None
            while current is not None:
                latest = current
                current = self.read_one()
            return latest
        else:
            return self.random_data()

    # Helpers

    def send(self, command: str):
        if not self.testing:
            self.ser.write((command + "\r").encode())

    def setup(self):
        if not self.testing:
            self.send("stop")
            self.send("encode 0")  # 0 = binary, 1 = ascii
            self.send("ps 0")  # small pocketsize for responsiveness

            for i in range(0, len(self.channels)):
                self.send("slist " + str(i) + " " + str(self.channels[i]))

            # Define sample rate = 100 Hz:
            # 60,000,000/(srate * dec) = 60,000,000/(1171 * 512) = 100 Hz
            self.send("dec 512")
            self.send("srate 1171")

            # self.send("dec 512")
            # self.send("srate 11718")

    def in_waiting(self) -> int:
        if not self.testing:
            return self.ser.in_waiting
        return None

    def buffer_read(self, channel: int) -> Optional[float]:
        """
        This function reads one value from the serial buffer. I.e. it will only read *one channel* at a time.
        Therefore, do not use this function by itself. If data is not always read in pairs of three there's no
        way to tell the channels apart.
        """
        if not self.testing:
            if self.in_waiting() < 2:
                return None
            buffer = self.ser.read(2)
            return (
                Tars.RANGE_VOLT[channel >> 8]
                * int.from_bytes(buffer, byteorder="little", signed=True)
                / 32768
            )
        return None

    # Testing

    def random_data(self):
        """sometimes it's not worth asking"""
        x = time.time() / 8

        n = r.choice([-0.2, 1]) / (64 * (r.random() + 0.02))
        n *= 0.08 * self.parent.ui.noise_dial.value() ** 2

        v = self.parent.ui.variance_dial.value()

        c = 1 if self.parent.ui.calibration_check_box.isChecked() else 0

        f = 0
        # f = math.sin(4 * x)

        g = (
            2.6 / (math.sin(2 * x) + 1.4)
            + 0.4 * math.sin(8 * x)
            - 0.8 * math.sin(4 * x)
            + (1 / (math.sin(8 * x) + 1.4))
        )

        a = f + g * v + n + c
        b = a - 0.1 * self.parent.ui.polarization_dial.value() * g * (v / 2 + 1)

        a, b = (i / 272 + c + 1 for i in (a, b))  # normalize, kinda

        # a, b, dec
        return [
            (0, a),
            (1, b),
            (2, float(self.parent.ui.declination_slider.value()) / 100),
        ]


def main():
    device_name = discovery()

    while not device_name:
        print("No DATAQ Device detected, retrying in 3 seconds.")
        time.sleep(3)
        device_name = discovery()

    print("Found a DATAQ Instruments device on", device_name)
    device = Tars(device_name)

    device.setup()
    time.sleep(3)
    device.start()

    while True:
        data = device.read_latest()
        if data is not None:
            print(data)


if __name__ == "__main__":
    main()
