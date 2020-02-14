import time

from ..observation import Observation, Scan, Survey, Spectrum
from ..datapoint import DataPoint
from ..comm import Comm

def test1():
    scan = Scan()
    scan.set_name("scan")

    survey = Survey()
    survey.set_name("survey")

    spectrum = Spectrum()
    spectrum.set_name("spectrum")

    baseline = time.time()
    timestamps = [-130, -65, 0, 105, 170, 235]
    datapoint = DataPoint(baseline % 86400, 1, 2, 45)

    for obs in [scan, survey, spectrum]:
        obs.set_RA(baseline, baseline + 100)
        obs.set_dec(60, 30)
        obs.set_data_freq(10)

        print("-----" + obs.name + "-----")
        for i in range(6):
            print(obs.communicate(datapoint, timestamps[i]))
            print(obs.state)
            obs.next()
        print(obs.state)
        