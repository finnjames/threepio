"""
Functionalities needed for working with files.
"""

from datetime import datetime

class MyPrecious:
    MAX_BUFFER_SIZE = 100

    def __init__(self, filename: str):
        self.filename = filename
        self.__buffer = []

    def __del__(self):
        if self.__buffer_size() > 0:
            self.__buffer_write()

    def write(self, val):
        self.__buffer_append(str(val))
        if self.__buffer_size() > MyPrecious.MAX_BUFFER_SIZE:
            self.__buffer_write()

    def clear(self):
        self.__buffer_clear()

    def close(self):
        self.__buffer_write()

    ### Helpfer functions below ###

    def __buffer_clear(self):
        """
        Run this function at the beginning, or each time when the buffer needs to be resetted.
        """
        self.__buffer = []

    def __buffer_write(self):
        """
        Run this function to actually write to the file. It will automatically clear the buffer
        """
        self.__file_append('\n'.join(self.__buffer))
        self.__buffer_clear()

    def __buffer_append(self, data: str):
        self.__buffer.append(data)
    
    def __buffer_size(self) -> int:
        return len(self.__buffer)

    def __file_write(self, data, mode='a'):
        if mode != 'a' and mode != 'w':
            print("Write mode not recognized. Please use " +
            "'a' for append and 'w' for write (overwrite).")
        with open(self.filename, mode) as file:
            print(data, end='\n', file=file)

    def __file_overwrite(self, data):
        self.__file_write(data, mode='w')

    def __file_append(self, data):
        self.__file_write(data, mode='a')
