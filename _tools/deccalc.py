class DecCalc:

    SOUTH_DEC = -25
    NORTH_DEC = 95
    STEP = 10

    def __init__(self):
        self.fx: list[DecCalc.XY] = []

    class XY:
        """x and y value pair"""

        def __init__(self, x, y):
            try:
                self.x = float(x)
                self.y = float(y)
            except ValueError:
                raise ValueError("values must be numbers")

        def __str__(self) -> str:
            return str(f"{self.x:0.2f} {self.y:0.2f}")

    @staticmethod
    def get_dec_list() -> list[float]:
        r = []
        i = DecCalc.SOUTH_DEC
        while i <= DecCalc.NORTH_DEC:
            r.append(i)
            i += DecCalc.STEP
        return r

    def load_dec_cal(self) -> int:
        """read the dec calibration from file and store it in memory"""

        def set_fx(x_lines: list):
            y_decs = self.get_dec_list()
            self.fx = [self.XY(x.strip(), y) for x, y in zip(x_lines, y_decs)]

        try:
            with open("dec-cal.txt", "r") as f:  # get data from file
                set_fx(f.readlines())
                return 0

        except FileNotFoundError:
            set_fx([i for i in map(lambda a: str(a * 0.01), range(-90, 91, 15))])
            raise FileNotFoundError

    def calculate_declination(self, input_dec: float) -> float:
        """calculate the true dec from declinometer input and calibration data"""

        fx = self.fx

        if input_dec < fx[0].x:  # input is below data
            return (
                (fx[1].y - fx[0].y) / (fx[1].x - fx[0].x) * (input_dec - fx[0].x)
            ) + fx[0].y
        elif input_dec > fx[-1].x:  # input is above data
            return (
                (fx[-1].y - fx[-2].y) / (fx[-1].x - fx[-2].x) * (input_dec - fx[-1].x)
            ) + fx[-1].y
        else:  # input is within data
            for i, _ in enumerate(self.fx):
                if input_dec <= fx[i + 1].x:
                    if input_dec >= fx[i].x:
                        # (dy/dx)x + y_0
                        return (
                            (fx[i + 1].y - fx[i].y)
                            / (fx[i + 1].x - fx[i].x)
                            * (input_dec - fx[i].x)
                        ) + fx[i].y
