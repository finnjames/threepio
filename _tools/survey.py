from tools import Comm, MyPrecious, Observation, ObsType


class Survey(Observation):
    """2D 'nodding' map of a region of the radio sky."""

    def __init__(self):
        super().__init__()
        self.obs_type = ObsType.SURVEY

        self.sweep_number = 1

        self.outside = True

    def set_files(self):
        assert self.name
        self.file_a = MyPrecious(self.name + "_a.md2")
        self.file_b = MyPrecious(self.name + "_b.md2")
        self.file_comp = MyPrecious(self.name + "_comp.md2")

    def data_logic(self, data_point) -> Comm:
        if data_point.dec < self.min_dec or data_point.dec > self.max_dec:
            if not self.outside:
                self.write("*")
            self.outside = True
            if data_point.dec < self.min_dec:
                return Comm.SEND_TEL_NORTH
            elif data_point.dec > self.max_dec:
                return Comm.SEND_TEL_SOUTH
        else:
            if self.outside:
                self.outside = False
                self.sweep_number += 1
                return Comm.END_SEND_TEL
        self.write_data(data_point)
        return Comm.NO_ACTION
