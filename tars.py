"""
This module includes a Tars class that encapsulate a serialpy object and provides
simple methods for initializing, starting, stopping, resetting, and reading from
the DATAQ device connected via a USB serial connection. The module also includes
a few helper functions relevant to the tasks.
"""

import serial
import serial.tools.list_ports
import time

def discovery() -> str:
    # Get a list of active com ports to scan for possible DATAQ Instruments devices
    available_ports = serial.tools.list_ports.comports()

    for p in available_ports:
        if "VID:PID=0683:4109" in p.hwid:
            return p.device
    
    return None

def convert(buffer: list, volt: int, channel: int) -> float:
    return volt * int.from_bytes(buffer, byteorder='little', signed=True) / 32768

class Tars:
    """
    A wrapper class of a serial object which supports functionalities
    specifically useful for DATAQ instruments.
    """

    RANGE_VOLT = (10, 5, 2, 1, 0.5, 0.2)
    RANGE_RATE = (50000, 20000, 10000, 5000, 2000,
                  1000, 500, 200, 100, 50, 20, 10)

    def __init__(self, device: str):
        self.ser = serial.Serial(device)
        self.acquiring = False
        self.channels = [
            0x0100, # channel 0, ±5 V range
            0x0101, # channel 1, ±5 V range
            0x0102, # channel 2, ±5 V range
        ]

    def send(self, command: str):
        self.ser.write((command + '\r').encode())
    
    def init(self):
        self.send("stop")
        self.send("encode 0")       # 0 = binary, 1 = ascii
        self.send("ps 0")           # small pocket size for responsiveness

        for i in range(0, len(self.channels)):
            self.send("slist " + str(i) + " " + str(self.channels[i]))

        # Define sample rate = 10 Hz:
        # 60,000,000/(srate * dec) = 60,000,000/(11718 * 512) = 10 Hz
        self.send("dec 5120")
        self.send("srate 11718")
    
    def start(self):
        self.send("start")
        self.acquiring = True

    def reset(self):
        self.send("reset 1")
    
    def stop(self):
        self.send("stop")
        self.ser.reset_input_buffer()
        self.acquiring = False

    def in_waiting(self) -> int:
        return self.ser.in_waiting

    def read_one(self, channel: int) -> float:
        buffer = self.ser.read(2)
        return self.RANGE_VOLT[channel >> 8] * int.from_bytes(buffer, byteorder='little', signed=True) / 32768
    
    def read_all(self) -> list:
        if self.in_waiting() < (2 * len(self.channels)):
            return None
        return [(channel, self.read_one(channel)) for channel in self.channels]

def main():
    device_name = discovery()

    while not device_name:
        print("No DATAQ Device detected, retrying in 3 seconds.")
        time.sleep(3)
        device_name = discovery()

    print("Found a DATAQ Instruments device on", device_name)
    device = Tars(device_name)

    device.init()
    time.sleep(3)
    device.start()

    while(True):
        device.read_all()

if __name__ == "__main__":
    main()