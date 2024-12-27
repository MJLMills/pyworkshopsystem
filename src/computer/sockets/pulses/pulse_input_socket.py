import machine
from input_output import IO


class PulseInputSocket(IO):
    """
    Inverted digital input: Low input = High reading.
    For example, use a falling edge to track the start of a pulse.
    NB: Input pin must have the pull-up enabled, this powers the transistor.

    Simple digital on/off signals, buffered and scaled with transistors.
    Use them for clocks, pulses, gates. They could also produce unfiltered PWM signals, so could maybe be used for gnarly audio (loud!) or gritty CV.
    They’ll often be used to trigger the envelopes, which are Serge-style voltage controlled slopes
    The gates are about 5-6v
    """
    def __init__(self):

        self._pin = machine.Pin(self.pin_id,
                                machine.Pin.IN,
                                machine.Pin.PULL_UP)

    def set_irq(self, handler):
        self._pin.irq(handler=handler, trigger=machine.Pin.IRQ_FALLING)

    def read(self):
        return self._pin.value()

    def is_high(self):
        return self.read() == 0

    def is_low(self):
        return self.read() == 1


class PulseInputSocketOne(PulseInputSocket):
    """The first (leftmost) pulse input socket."""

    @property
    def pin_id(self):
        """The unique identifier of the GPIO pin used by this class."""
        return 2


class PulseInputSocketTwo(PulseInputSocket):
    """The second (rightmost) pulse input socket."""

    @property
    def pin_id(self):
        """The unique identifier of the GPIO pin used by this class."""
        return 3