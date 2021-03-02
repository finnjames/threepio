# Threepio 🤖

The new data acquisition system for the 40-foot radio telescope at the [Green Bank Observatory](https://greenbankobservatory.org/). This software is part of the [ERIRA](https://www.danreichart.com/erira) program.

## Dependencies

**Threepio** uses `PyQt5` for GUI and `pySerial` for communication to the data collection hardware (DataQ).

## Setting Up

Clone the repo and `cd` into it.
```
$ git clone https://github.com/radiolevity/threepio.git
$ cd threepio
```

**Threepio** requires Python 3.7.x. Using a virtual environment is strongly recommended.
```
$ python --version
Python 3.7.10
$ python -m venv env
```

Activate the virtual environment.
```
$ source ./env/bin/activate
```

Update pip and install dependencies.
```
env $ pip install --upgrade pip
env $ pip install -r requirements.txt
```

Run
```
env $ python threepio.py
```
