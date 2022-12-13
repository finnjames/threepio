"""
Small version of Tars, meant to be used with the Arduino declinometer as opposed to the
DataQ.
"""
from typing import Optional

import serial
from .myserial import MySerial
import serial.tools.list_ports

import time
import math


def discovery():
    """Get a list of active com ports and scan for declinometer"""
    available_ports = serial.tools.list_ports.comports()

    declinometer = None
    for p in available_ports:
        if "VID:PID=0403:6001" in p.hwid:
            declinometer = p.device

    return declinometer


class MiniTars:
    def __init__(self, parent=None, device=None):
        self.parent = parent
        self.testing = True
        self.acquiring = False
        if device is not None:
            self.testing = False
            self.ser = MySerial(device)
            self.ser.baudrate = 38400
        else:
            self.parent.log("Declinometer not found, simulating data")

    def start(self):
        if not self.testing:
            self.acquiring = True

    def stop(self):
        if not self.testing:
            self.ser.reset_input_buffer()
            self.acquiring = False

    def read_one(self) -> Optional[float]:
        """
        This reads one datapoint from the buffer.
        """
        if not self.testing:
            if self.in_waiting() < 1:
                return None
            return self.buffer_read()
        else:
            return self.random_data()

    def read_latest(self) -> float:
        """
        This function reads the last datapoint from the buffer and clears the buffer.
        Use this as a real-time sampling method.
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

    def in_waiting(self) -> int:
        if not self.testing:
            return self.ser.in_waiting

    def buffer_read(self) -> Optional[float]:
        """read angle from serial buffer"""
        if not self.testing:
            if self.in_waiting() < 1:
                return None
            # TODO: clean up
            # print("start")
            # print("get-360".encode("ascii"))
            # self.ser.write(bytes("get-360".encode("ascii")))
            # line = self.ser.read(size=8)
            line = self.ser.read_until(
                expected="\r".encode("ascii")
            )  # read a byte string TODO: encoding necessary?
            # print(line.decode())
            # print(f"minitars: {line}")
            try:
                print(f"minitars: {float(line.decode())}")
                return float(line.decode())
            except (UnicodeDecodeError, ValueError):
                pass
            return None

    # Testing

    def random_data(self) -> float:
        """for testing"""
        if self.parent.ui.dec_auto_check_box.isChecked():
            return math.sin(time.time() / 2) * 100
        return float(self.parent.ui.declination_slider.value())


def main():
    declinometer = discovery()

    while not declinometer:
        print("No declinometer detected, retrying in 3 seconds.")
        time.sleep(3)
        declinometer = discovery()

    print("Found a declinometer on", declinometer)
    minitars = MiniTars(device=declinometer)

    minitars.start()

    while True:
        data = minitars.read_latest()
        # print(data)
        if data is not None:
            print(minitars.testing)
            print(data)


if __name__ == "__main__":
    main()
