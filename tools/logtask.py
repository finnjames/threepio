class LogTask:
    """
    A task that has been logged, which can then be updated to display success/failure
    """

    def __init__(self, message: str, sidereal_str: str = None):
        self.message = message
        self.sidereal_str = sidereal_str
        self.status = -1

    def get_message(self) -> str:
        r = ""
        if self.sidereal_str is not None:
            r += f"[{self.sidereal_str}] "
        r += self.message
        if self.status != -1:
            r += f" {self.__status_to_string()}"
        return r

    def set_sidereal_str(self, sidereal_str: str):
        self.sidereal_str = sidereal_str

    def set_status(self, status: int):
        """
        -1: pending
        0: success
        1: failure
        """
        self.status = status

    def __status_to_string(self):
        if self.status == -1:
            return "pending..."
        elif self.status == 0:
            return "done!"
        elif self.status == 1:
            return "failed"
        else:
            return "unknown"
