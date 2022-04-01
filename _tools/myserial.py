import serial


# noinspection PyUnresolvedReferences,PyProtectedMember
class MySerial(serial.Serial):
    def _reconfigure_port(self, *args, **kwargs):
        try:
            super()._reconfigure_port(*args, **kwargs)
        except serial.SerialException:
            pass
