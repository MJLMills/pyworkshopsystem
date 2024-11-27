from src.computer.sockets import OutputSocket
import machine


class PulseOutputSocket(OutputSocket):
    """An output socket of the computer, sending pulses.

    Inverted digital output: 1/true = low, 0/false=high.
    Scaled via a transistor.
    Pin should be input, no pullup.
    """
    def __init__(self, pin_id):

        self._pin = machine.Pin(pin_id,
                                machine.Pin.OUT)

    @property
    def pin(self):
        return self._pin

    def turn_on(self):
        self.pin.value(0)

    def turn_off(self):
        self.pin.value(1)


class PulseOutputSocketOne(PulseOutputSocket):
    """The first (leftmost) pulse input socket."""

    PIN_ID = 8
    """The ID of the pin carrying the signal from this socket."""

    def __init__(self):
        super().__init__(pin_id=self.PIN_ID)


class PulseOutputSocketTwo(PulseOutputSocket):
    """The second (rightmost) pulse input socket."""

    PIN_ID = 9
    """The ID of the pin carrying the signal from this socket."""

    def __init__(self):
        super().__init__(pin_id=self.PIN_ID)
