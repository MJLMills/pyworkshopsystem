from multiplexed_input import MultiplexedInput


class CVInputSocket(MultiplexedInput):
    """The CV input sockets of the Computer.

    CV inputs are not inverted.
    -5V reads ~350
    0V reads ~2030
    +5V reads ~3700
    (these are from the docs and are hinting at calibration from the uint12
    values to actual voltages)
    """

    @property
    def pin_id(self):
        """The unique identifier of the GPIO pin used by this class."""
        return 29  # try not to redefine this here as a literal, get from multiplexer by name?

    @property
    def min_value(self) -> int:
        return 0

    @property
    def max_value(self) -> int:
        return 65535

class CVInputSocketOne(CVInputSocket):
    """The first (left-most) CV input socket of the Computer."""

    @property
    def mux_logic_a_pin_value(self) -> bool:
        """The value of the first multiplexer login pin for this input."""
        return False

    @property
    def mux_logic_b_pin_value(self) -> bool:
        """The value of the second multiplexer login pin for this input."""
        return False


class CVInputSocketTwo(CVInputSocket):
    """The second (right-most) CV input socket of the Computer."""

    @property
    def mux_logic_a_pin_value(self) -> bool:
        """The value of the first multiplexer login pin for this input."""
        return False

    @property
    def mux_logic_b_pin_value(self):
        """The value of the second multiplexer login pin for this input."""
        return True