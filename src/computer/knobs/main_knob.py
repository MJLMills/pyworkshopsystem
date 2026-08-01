from micropython import const
from computer.base import MultiplexedInput


class MainKnob(MultiplexedInput):
    """The main (big) knob on the Computer module.

    The raw value read from the knob is a 16-bit unsigned integer
    with range from 0 to 65535 inclusive. This class maps the raw
    values into a range specified by the user, defaulting to the
    full range of the 16-bit unsigned integer.

    """
    _IO_PIN_ID = const(28)
    _MUX_LOGIC_A_PIN_VALUE = const(0)
    _MUX_LOGIC_B_PIN_VALUE = const(0)

    __MIN_VALUE_U16 = 224
    __MAX_VALUE_U16 = 65535

    def __init__(self):
        super().__init__()

    @property
    def min_value(self) -> int:
        return self.__MIN_VALUE_U16

    @property
    def max_value(self) -> int:
        return self.__MAX_VALUE_U16

