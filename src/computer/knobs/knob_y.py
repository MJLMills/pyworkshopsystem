from base.multiplexed_input import MultiplexedInput


class KnobY(MultiplexedInput):
    """The knob marked Y."""
    __IO_PIN_ID = 28
    __MIN_VALUE_U16 = 192
    __MAX_VALUE_U16 = 65535
    __MUX_LOGIC_A_PIN_VALUE = False
    __MUX_LOGIC_B_PIN_VALUE = True

    def __init__(self):
        super().__init__()

    @property
    def io_pin_id(self) -> int:
        """The unique identifier of the GPIO pin used by knob Y."""
        return self.__IO_PIN_ID

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
