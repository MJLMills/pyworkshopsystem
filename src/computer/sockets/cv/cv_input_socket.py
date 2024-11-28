from abc import ABC
import machine
from multiplexed_input import MultiplexedInput


class CVInputSocket(ABC, MultiplexedInput):
    """
    CV inputs are not inverted.
    -5V reads ~350
    0V reads ~2030
    +5V reads ~3700
    """
    @property
    def mux_io_pin_id(self):
        return 29  # try not to redefine this here as a literal, get from multiplexer by name?


class CVInputSocketOne(CVInputSocket):

    @property
    def mux_logic_a_pin_value(self):
        return 0

    @property
    def mux_logic_b_pin_value(self):
        return 0


class CVInputSocketTwo(CVInputSocket):

    @property
    def mux_logic_a_pin_value(self):
        return 0

    @property
    def mux_logic_b_pin_value(self):
        return 1
