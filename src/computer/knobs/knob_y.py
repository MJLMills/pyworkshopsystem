from micropython import const
from computer.base.multiplexed_input import MultiplexedInput


class KnobY(MultiplexedInput):
    """The knob marked Y."""
    _IO_PIN_ID = const(28)
    _MUX_LOGIC_A_PIN_VALUE = const(0)
    _MUX_LOGIC_B_PIN_VALUE = const(1)

    __MIN_VALUE_U16 = 192
    __MAX_VALUE_U16 = 65535

    def __init__(self):
        super().__init__()

    @property
    def min_value(self) -> int:
        """The minimum value that can be read from knob Y."""
        return self.__MIN_VALUE_U16

    @property
    def max_value(self) -> int:
        """The maximum value that can be read from knob Y."""
        return self.__MAX_VALUE_U16

    @property
    def mux_logic_a_pin_value(self) -> bool:
        """The value of the first multiplexer login pin for knob Y."""
        return self.__MUX_LOGIC_A_PIN_VALUE

    @property
    def mux_logic_b_pin_value(self) -> bool:
        """The value of the second multiplexer login pin for knob Y."""
        return self.__MUX_LOGIC_B_PIN_VALUE
