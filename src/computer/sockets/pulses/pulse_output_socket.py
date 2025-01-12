import machine
import time
from input_output import DigitalOutput


class PulseOutputSocket(DigitalOutput):
    """An output socket of the computer, sending pulses.

    Inverted digital output: 1/true = low, 0/false=high.
    Scaled via a transistor.
    Pin should be output, no pullup.
    """

    @property
    def pin(self):
        return self._pin

    def turn_on(self):
        self.pin.value(0)

    def turn_off(self):
        self.pin.value(1)

    def is_on(self):
        return self.pin.value() == 0

    def is_off(self):
        return not self.is_on()

    def pulse(self, duration):
        self.turn_on()
        time.sleep(duration)
        self.turn_off()

    def set_value(self, value):
        self.pin.value(value)


class PulseOutputSocketOne(PulseOutputSocket):
    """The first (leftmost) pulse input socket."""

    @property
    def pin_id(self) -> int:
        """The unique identifier of the GPIO pin used by this class."""
        return 8


class PulseOutputSocketTwo(PulseOutputSocket):
    """The second (rightmost) pulse input socket."""

    @property
    def pin_id(self) -> int:
        """The unique identifier of the GPIO pin used by this class."""
        return 9