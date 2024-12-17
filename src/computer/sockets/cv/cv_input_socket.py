import machine
from multiplexed_input import MultiplexedInput


class CVInputSocket(MultiplexedInput):
    """The CV input sockets of the Computer.

    CV inputs are not inverted.
    -5V reads ~350
    0V reads ~2030
    +5V reads ~3700
    """

    @property
    def pin_id(self):
        return 29  # try not to redefine this here as a literal, get from multiplexer by name?

    def read_norm(self):
        return self.read() / 65535


class CVInputSocketOne(CVInputSocket):
    """The first (left-most) CV input socket of the Computer."""

    @property
    def mux_logic_a_pin_value(self):
        return 0

    @property
    def mux_logic_b_pin_value(self):
        return 0


class CVInputSocketTwo(CVInputSocket):
    """The second (right-most) CV input socket of the Computer."""

    @property
    def mux_logic_a_pin_value(self):
        return 0

    @property
    def mux_logic_b_pin_value(self):
        return 1