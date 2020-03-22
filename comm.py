from enum import Enum


class Comm(Enum):
    NO_ACTION = 0
    BEEP = 1
    START_CAL = 2
    STOP_CAL = 3
    NEXT = 4
    FINISHED = 5
