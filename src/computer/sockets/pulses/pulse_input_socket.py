from abc import ABC
import machine
from multiplexed_input import IO


class PulseInputSocket(ABC, IO):  # should be abstract
    """
    Inverted digital input: Low input = High reading.
    For example, use a falling edge to track the start of a pulse.
    NB: Input pin must have the pull-up enabled, this powers the transistor.
    """
    def __init__(self):

        self._pin = machine.Pin(self.pin_id,
                                machine.Pin.IN,
                                machine.Pin.PULL_UP)


class PulseInputSocketOne(PulseInputSocket):
    """The first (leftmost) pulse input socket."""

    PIN_ID = 2
    """The ID of the pin carrying the signal from this socket."""

    @property
    def pin_id(self):
        return self.PIN_ID


class PulseInputSocketTwo(PulseInputSocket):
    """The second (rightmost) pulse input socket."""

    PIN_ID = 3
    """The ID of the pin carrying the signal from this socket."""

    @property
    def pin_id(self):
        return self.PIN_ID