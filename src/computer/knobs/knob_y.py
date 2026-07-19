from micropython import const
from computer.base.multiplexed_input import MultiplexedInput


class KnobY(MultiplexedInput):
    """The knob marked Y."""
    IO_PIN_ID = const(28)
    MIN_VALUE_U16 = const(192)
    MAX_VALUE_U16 = const(65535)
    MUX_LOGIC_PIN_A_VALUE = const(False)
    MUX_LOGIC_PIN_B_VALUE = const(True)

    def __init__(self):
        super().__init__()

    @property
    def min_value(self) -> int:
        """The minimum value that can be read from knob Y."""
        return KnobY.MIN_VALUE_U16

    @property
    def max_value(self) -> int:
        """The maximum value that can be read from knob Y."""
        return KnobY.MAX_VALUE_U16
