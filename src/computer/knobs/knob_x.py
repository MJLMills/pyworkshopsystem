from base.multiplexed_input import MultiplexedInput


class KnobX(MultiplexedInput):
    """The knob marked X."""
    __IO_PIN_ID = 28
    __MIN_VALUE_U16 = 224
    __MAX_VALUE_U16 = 65535
    __MUX_LOGIC_A_PIN_VALUE = True
    __MUX_LOGIC_B_PIN_VALUE = False

    def __init__(self):
        super().__init__()

    @property
    def pin_id(self) -> int:
        """The unique identifier of the GPIO pin used by this class."""
        return self.__IO_PIN_ID

    @property
    def min_value(self) -> int:
        return self.__MIN_VALUE_U16

    @property
    def max_value(self) -> int:
        return self.__MAX_VALUE_U16

    @property
    def mux_logic_a_pin_value(self) -> bool:
        """The value of the first multiplexer login pin for this input."""
        return self.__MUX_LOGIC_A_PIN_VALUE

    @property
    def mux_logic_b_pin_value(self) -> bool:
        """The value of the second multiplexer login pin for this input."""
        return self.__MUX_LOGIC_B_PIN_VALUE
