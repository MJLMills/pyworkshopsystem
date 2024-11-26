import machine
from . import InputSocket


class PulseInputSocket(InputSocket):  # should be abstract
    """
    Inverted digital input: Low input = High reading.
    For example, use a falling edge to track the start of a pulse.
    NB: Input pin must have the pull-up enabled, this powers the transistor.
    """
    def __init__(self, pin_id):

        self._pin = machine.Pin(pin_id,
                                machine.Pin.IN,
                                machine.Pin.PULL_UP)

    @property
    def pin(self):
        return self._pin


class PulseInputSocketOne(PulseInputSocket):
    """The first (leftmost) pulse input socket."""

    PIN_ID = 2
    """The ID of the pin carrying the signal from this socket."""

    def __init__(self):
        super().__init__(pin_id=self.PIN_ID)


class PulseInputSocketTwo(PulseInputSocket):
    """The second (rightmost) pulse input socket."""

    PIN_ID = 3
    """The ID of the pin carrying the signal from this socket."""

    def __init__(self):
        super().__init__(pin_id=self.PIN_ID)
