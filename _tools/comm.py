from enum import Enum


class Comm(Enum):
    NO_ACTION = 0
    BEEP = 1
    START_CAL = 2
    START_BG = 3
    NEXT = 4
    FINISHED = 5
    # extra
    START_WAIT = 6
    START_DATA = 7
    SEND_TEL_NORTH = 8
    SEND_TEL_SOUTH = 9
    END_SEND_TEL = 10
    FINISH_SWEEP = 11
