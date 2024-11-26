import machine
from . import InputSocket


class CVInputSocket(InputSocket):  # should be abstract
    """
    CV inputs are not inverted.
    -5V reads ~350
    0V reads ~2030
    +5V reads ~3700
    """
    MUX_LOGIC_A_PIN_VALUE = 0  # these should be abstract properties
    MUX_LOGIC_B_PIN_VALUE = 0  # then read can be shared properly

    PIN_ID = 29
    """The multiplexer output pin from which to read."""
    ...

    def __init__(self, multiplexer):
        self.__multiplexer = multiplexer

    def read(self):
        self.__multiplexer.set_logic_pin_values(a=self.MUX_LOGIC_A_PIN_VALUE,
                                                b=self.MUX_LOGIC_B_PIN_VALUE)
        return machine.ADC(CVInputSocket.PIN_ID).read_u16()


class CVInputSocketOne(CVInputSocket):
    MUX_LOGIC_A_PIN_VALUE = 0
    MUX_LOGIC_B_PIN_VALUE = 0


class CVInputSocketTwo(CVInputSocket):
    MUX_LOGIC_A_PIN_VALUE = 0
    MUX_LOGIC_B_PIN_VALUE = 1
    ...
