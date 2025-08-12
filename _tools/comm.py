from enum import Enum, auto


class Comm(Enum):
    NO_ACTION = auto()
    BEEP = auto()
    START_CAL = auto()
    START_BG = auto()
    NEXT = auto()
    FINISHED = auto()
    # Extra
    START_WAIT = auto()
    START_DATA = auto()
    SEND_TEL_NORTH = auto()
    SEND_TEL_SOUTH = auto()
    END_SEND_TEL = auto()
    FINISH_SWEEP = auto()
