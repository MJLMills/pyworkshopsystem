from multiplexed_input import MultiplexedInput


class MainKnob(MultiplexedInput):
    """The main (big) knob on the Computer module.

    The raw value read from the knob is a 16-bit unsigned integer
    with range from 0 to 65535 inclusive. This class maps the raw
    values into a range specified by the user, defaulting to the
    full range of the 16-bit unsigned integer.
    """
    def __init__(self):
        super().__init__()

    @property
    def min_value(self) -> int:
        return 224

    @property
    def max_value(self) -> int:
        return 65535

    @property
    def pin_id(self) -> int:
        """The unique identifier of the GPIO pin used by this class."""
        return 28

    @property
    def mux_logic_a_pin_value(self) -> bool:
        """The value of the first multiplexer login pin for this input."""
        return False

    @property
    def mux_logic_b_pin_value(self) -> bool:
        """The value of the second multiplexer login pin for this input."""
        return False
