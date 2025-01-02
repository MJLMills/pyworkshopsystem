from multiplexed_input import MultiplexedInput


class KnobX(MultiplexedInput):
    """The knob marked X."""

    def __init__(self):
        super().__init__()

    @property
    def min_value(self) -> int:
        return 14

    @property
    def max_value(self) -> int:
        return 4095

    @property
    def pin_id(self) -> int:
        """The unique identifier of the GPIO pin used by this class."""
        return 28

    @property
    def mux_logic_a_pin_value(self) -> bool:
        """The value of the first multiplexer login pin for this input."""
        return True

    @property
    def mux_logic_b_pin_value(self) -> bool:
        """The value of the second multiplexer login pin for this input."""
        return False
