# Threepio 🤖

The new data acquisition system for the 40-foot radio telescope at the [Green Bank Observatory](https://greenbankobservatory.org/). This software is part of the [ERIRA](https://www.danreichart.com/erira) program.

## Dependencies

Threepio uses `PyQt5` for GUI and `pySerial` for communication to the data collection hardware, including a [SOLAR-360-2-RS232](https://www.leveldevelopments.com/products/inclinometers/inclinometer-sensors/single-axis-inclinometer-sensors/solar-360-series/solar-360-2-rs232-inclinometer-sensor-single-axis-180-rs232-with-tc/) inclinometer and a DataQ A2D card.

## Setting Up

### For Linux & macOS
Clone the repo and `cd` into it.
```
$ git clone https://github.com/finnjames/threepio.git
$ cd threepio
```

Threepio requires Python 3.13.x. Using a virtual environment is strongly recommended.
```
$ python --version
Python 3.13.6
$ python -m venv --upgrade-deps venv
```

Activate the virtual environment.
```
$ source ./venv/bin/activate
```

Install dependencies.
```
(venv) $ pip install -r requirements.txt
```

Run
```
(venv) $ python threepio.py
```

### For Windows
Clone the repo and `cd` into it.
```
$ git clone https://github.com/finnjames/threepio.git
$ cd threepio
```

Threepio requires Python 3.13.x. Using a virtual environment is strongly recommended.
```
$ python --version
Python 3.13.6
$ python -m venv --upgrade-deps venv
```

Activate the virtual environment.
```
$ .\venv\Scripts\Activate.ps1
```

Install dependencies.
```
(venv) $ python -m pip install -r requirements.txt
```

Run
```
(venv) $ python threepio.py
```
