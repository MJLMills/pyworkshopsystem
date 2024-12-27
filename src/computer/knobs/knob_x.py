from multiplexed_input import MultiplexedInput


class KnobX(MultiplexedInput):
    """The knob marked X."""

    def __init__(self, max_value=None, min_value=None):

        super().__init__()

        # redundant but depends on normalization
        if max_value is None:
            self._max_value = 65535
        else:
            self._max_value = max_value

        if min_value is None:
            self._min_value = 224
        else:
            self._min_value = min_value

        self._range = self._max_value - self._min_value

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

    def read_norm(self):
        return (self.read() - self._min_value) / self._range
