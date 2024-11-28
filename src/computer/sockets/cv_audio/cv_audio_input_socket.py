from src.computer.sockets import InputSocket
import machine


class CVAudioInputSocket(InputSocket):
    """
    Inverted bipolar analog input, into 12(?) bit internal ADC.
    +6V = 0
    0V = 2048
    -6V = 4095
    DC coupled, requires calibration for precise readings.
    """
    def __init__(self, number):
        self.adc = machine.ADC(number)

    def read(self):
        raise self.adc.read_u16()


class CVAudioInputSocketOne(CVAudioInputSocket):
    """The left audio input socket."""

    PIN_ID = 26

    def __init__(self):
        super().__init__(number=1)


class CVAudioInputSocketTwo(CVAudioInputSocket):
    """The right audio input socket."""
    PIN_ID = 27

    def __init__(self):
        super().__init__(number=2)
