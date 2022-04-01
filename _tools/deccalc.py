from dialogs import DecDialog


class DecCalc:
    def __init__(self):
        self.y = []
        self.x = []

    def load_dec_cal(self):
        """read the dec calibration from file and store it in memory"""
        # create y array
        self.y = []
        i = DecDialog.SOUTH_DEC
        while i <= DecDialog.NORTH_DEC:
            self.y.append(float(i))
            i += abs(DecDialog.STEP)

        # create x array
        self.x = []
        with open("dec-cal.txt", "r") as f:  # get data from file
            c = f.read().splitlines()
            for i in c:
                self.x.append(float(i))

    def calculate_declination(self, input_dec: float):
        """calculate the true dec from declinometer input and calibration data"""

        if input_dec < self.x[0]:  # input is below data
            return (
                (self.y[1] - self.y[0])
                / (self.x[1] - self.x[0])
                * (input_dec - self.x[0])
            ) + self.y[0]
        elif input_dec > self.x[-1]:  # input is above data
            return (
                (self.y[-1] - self.y[-2])
                / (self.x[-1] - self.x[-2])
                * (input_dec - self.x[-1])
            ) + self.y[-1]
        else:  # input is within data
            for i in range(len(self.x)):
                if input_dec <= self.x[i + 1]:
                    if input_dec >= self.x[i]:
                        # (dy/dx)x + y_0
                        return (
                            (self.y[i + 1] - self.y[i])
                            / (self.x[i + 1] - self.x[i])
                            * (input_dec - self.x[i])
                        ) + self.y[i]
