from enum import Enum


class Comm(Enum):
    NO_ACTION = 0
    BEEP = 1
    START_CAL = 2
    STOP_CAL = 3
    NEXT = 4
    FINISHED = 5
    # extra
    SEND_TEL_NORTH = 6
    SEND_TEL_SOUTH = 7
    STOP_TEL = 8
