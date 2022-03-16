from dataclasses import dataclass
from PyQt5 import QtCore


@dataclass(frozen=True)
class InputRecord:
    start_time: QtCore.QTime
    end_time: QtCore.QTime
    min_dec: str
    max_dec: str
    data_acquisition_rate_value: int
    file_name_value: str
