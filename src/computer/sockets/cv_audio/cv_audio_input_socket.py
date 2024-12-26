import machine
from input_output import IO


class CVAudioInputSocket(IO):
    """The CV/Audio input sockets of the computer.

    The CV/Audio analog inputs are bipolar (inverted) and DC-coupled.
    They require calibration for precise readings.
    The values returned by machine.ADC.read_u16 are in the range:
    +6v = 0
     0v = 32768
    -6v = 65535
    In practice the precision of the internal ADC is closer to 12-bit.

    The left input is normalled to the right input, so if only one
    socket is plugged in, both channels receive the same input.

    The input signals are scaled (presumably in hardware) and then
    go to channels 0 and 1 of an internal analog to digital converter
    (Note that the multiplexer makes use of channels 3 and 4 to read
    the CV inputs, knobs and switch). From there they appear to go to
    two assigned GPIO pins (26 and 27) on the Pi, from which they are
    directly readable as analog inputs.
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
    def pin_id(self) -> int:
        """The unique identifier of the GPIO pin used by this class."""
        return 27


class CVAudioInputSocketTwo(CVAudioInputSocket):
    """The right CV/Audio input socket."""

    @property
    def pin_id(self) -> int:
        """The unique identifier of the GPIO pin used by this class."""
        return 26
