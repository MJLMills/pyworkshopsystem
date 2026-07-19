from computer.base.multiplexed_input import MultiplexedInput


class KnobX(MultiplexedInput):
    """The knob marked X."""
    IO_PIN_ID = 28
    MIN_VALUE_U16 = 192
    MAX_VALUE_U16 = 65535
    MUX_LOGIC_PIN_A_VALUE = True
    MUX_LOGIC_PIN_B_VALUE = False

    def __init__(self):
        super().__init__()

    @property
    def io_pin_id(self) -> int:
        """The unique identifier of the GPIO pin used by knob X."""
        return KnobX.IO_PIN_ID

    @property
    def min_value(self) -> int:
        """The minimum value that can be read from knob X."""
        return KnobX.MIN_VALUE_U16

    @property
    def max_value(self) -> int:
        """The maximum value that can be read from knob Y."""
        return KnobX.MAX_VALUE_U16
