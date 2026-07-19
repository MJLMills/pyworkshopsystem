from computer.base import MultiplexedInput


class MainKnob(MultiplexedInput):
    """The main (big) knob on the Computer module.

    The raw value read from the knob is a 16-bit unsigned integer
    with range from 0 to 65535 inclusive. This class maps the raw
    values into a range specified by the user, defaulting to the
    full range of the 16-bit unsigned integer.

    """
    IO_PIN_ID = 28
    MIN_VALUE_U16 = 224
    MAX_VALUE_U16 = 65535
    MUX_LOGIC_PIN_A_VALUE = False
    MUX_LOGIC_PIN_B_VALUE = False

    def __init__(self):
        super().__init__()

    @property
    def io_pin_id(self) -> int:
        """The unique identifier of the GPIO pin used by this class."""
        return MainKnob.IO_PIN_ID

    @property
    def min_value(self) -> int:
        return MainKnob.MIN_VALUE_U16

    @property
    def max_value(self) -> int:
        return MainKnob.MAX_VALUE_U16
