"""
Small version of Tars, meant to be used with the Arduino declinometer as opposed to the DataQ.
"""

import serial
import serial.tools.list_ports

import time
import math
import random as r


def discovery() -> str:
    """only use for minitars testing"""
    # Get a list of active com ports to scan for possible DATAQ Instruments devices
    available_ports = serial.tools.list_ports.comports()

    arduino = None
    for p in available_ports:
        if "VID:PID=2341:0043" in p.hwid:
            arduino = p.device

    return arduino


class MiniTars:
    def __init__(self, parent=None, device=None):
        self.parent = parent
        self.testing = True
        self.acquiring = False
        if device is not None:
            self.testing = False
            self.ser = serial.Serial(device)

    def start(self):
        if not self.testing:
            self.acquiring = True

    def stop(self):
        if not self.testing:
            self.ser.close()
            self.acquiring = False

    def read_one(self) -> list:
        """
        This reads one datapoint from the buffer.
        """
        if not self.testing:
            if self.in_waiting() < 1:
                return None
            line = self.ser.readline()  # read a byte string
            self.ser.flushInput()
            print(line)
            if line:
                try:
                    string = (
                        line.decode().strip()
                    )  # convert byte string to unicode string and remove trailing newline
                    data = tuple([float(i) for i in string.split(",")])

                    # check format of data
                    if isinstance(data, tuple) and list(map(type, data)) == [
                        float,
                        float,
                        float,
                    ]:
                        return data

                except UnicodeDecodeError:
                    pass
                except ValueError:
                    pass
        else:
            return self.random_data()

    def read_latest(self) -> list:
        """
        This function reads the last datapoint from the buffer and clears the buffer.
        Use this as a real-time sampling method.
        """
        if not self.testing:
            return self.read_one()
        else:
            return self.random_data()

    # Helpers

    def in_waiting(self) -> int:
        if not self.testing:
            return self.ser.in_waiting

    # Testing

    def random_data(self):
        """for testing"""
        t = time.time() / 8

        n = r.choice([-0.2, 1]) / (64 * (r.random() + 0.02))
        try:
            n *= 0.08 * self.parent.ui.noise_dial.value() ** 2
        except AttributeError:
            pass

        fx = math.sin(4 * t)
        fy = math.sin(4 * t + (2 * math.pi / 3))
        fz = math.sin(4 * t + (4 * math.pi / 3))

        x = fx + n
        y = fy + n
        z = fz + n

        return (x, y, z)


def main():
    arduino = discovery()

    while not arduino:
        print("No declinometer detected, retrying in 3 seconds.")
        time.sleep(3)
        arduino = discovery()

    print("Found a declinometer on", arduino)
    minitars = MiniTars(device=arduino)

    minitars.start()

    while True:
        data = minitars.read_latest()
        print(data)
        if data is not None:
            print(minitars.testing)
            print(data)


if __name__ == "__main__":
    main()
