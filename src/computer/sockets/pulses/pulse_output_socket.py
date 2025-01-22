from base.digital_output import DigitalOutput


class PulseOutputSocket(DigitalOutput):
    """An output socket of the computer, sending pulses.

    Inverted digital output: 1/true = low, 0/false=high.
    Scaled via a transistor.
    Pin should be output, no pullup.
    """
    __ON_VALUE = 0
    __OFF_VALUE = 1

    @property
    def on_value(self) -> int:
        """The value used to represent "on" for this digital output."""
        return self.__ON_VALUE

    @property
    def off_value(self) -> int:
        """The value used to represent "off" for this digital output."""
        return self.__OFF_VALUE

class PulseOutputSocketOne(PulseOutputSocket):
    """The first (leftmost) pulse input socket."""

    @property
    def io_pin_id(self) -> int:
        """The unique identifier of the GPIO pin used by this class."""
        return 8


class PulseOutputSocketTwo(PulseOutputSocket):
    """The second (rightmost) pulse input socket."""

    @property
    def io_pin_id(self) -> int:
        """The unique identifier of the GPIO pin used by this class."""
        return 9