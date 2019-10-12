"""
Functionalities needed for working with files.
"""

def write_to(filename: str, data, mode='a'):
    with open(filename, mode) as file:
        print(data, end='\n', file=file)

def write_over(filename: str, data):
    write_to(filename, data, mode='w')

def write_append(filename: str, data):
    write_to(filename, data, mode='a')
