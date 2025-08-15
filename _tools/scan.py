from tools import Comm, MyPrecious, Observation, ObsType


class Scan(Observation):
    """A 'drift scan' across a source."""

    def __init__(self):
        super().__init__()
        self.obs_type = ObsType.SCAN

    def set_files(self):
        self.file_a = MyPrecious(self.name + "_a.md1")
        self.file_b = MyPrecious(self.name + "_b.md1")
        self.file_comp = MyPrecious(self.name + "_comp.md1")

    def data_logic(self, data_point) -> Comm:
        self.write_data(data_point)
        return Comm.NO_ACTION
