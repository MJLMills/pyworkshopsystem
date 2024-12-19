import machine
from input_output import IO


class CVAudioInputSocket(IO):
    """The CV/Audio input sockets of the computer.

    Inverted bipolar analog input, into 12(?) bit internal ADC.
    +6V = 0
    0V = 2048
    -6V = 4095
    DC coupled, requires calibration for precise readings.
    """
    def __init__(self):
        self._adc = machine.ADC(self.pin_id)

    def read(self):
        return self._adc.read_u16()

    def read_norm(self):
        return self.read() / 65535


class CVAudioInputSocketOne(CVAudioInputSocket):
    """The left CV/Audio input socket."""
    @property
    def pin_id(self):
        return 26


class CVAudioInputSocketTwo(CVAudioInputSocket):
    """The right CV/Audio input socket."""

    @property
    def pin_id(self):
        return 27
