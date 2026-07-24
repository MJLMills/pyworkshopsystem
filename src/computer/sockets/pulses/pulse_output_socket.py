from computer.base.digital_output import DigitalOutput


class PulseOutputSocket(DigitalOutput):
    """An output socket of the computer, sending pulses.

    Inverted digital output: 1/true = low, 0/false=high.
    Scaled via a transistor.
    Pin should be output, no pullup.
    """
    ON_VALUE = 0
    OFF_VALUE = 1


class PulseOutputSocketOne(PulseOutputSocket):
    """The first (leftmost) pulse input socket."""
    IO_PIN_ID = 8


class PulseOutputSocketTwo(PulseOutputSocket):
    """The second (rightmost) pulse input socket."""
    IO_PIN_ID = 9
