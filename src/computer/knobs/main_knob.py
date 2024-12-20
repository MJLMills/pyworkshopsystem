from multiplexed_input import MultiplexedInput


class MainKnob(MultiplexedInput):
    """The main (big) knob on the Computer module.

    The raw value read from the knob is a 16-bit unsigned integer
    with range from 0 to 65535 inclusive. This class maps the raw
    values into a range specified by the user, defaulting to the
    full range of the 16-bit unsigned integer.
    """

    def __init__(self, max_value=None, min_value=None):
        super().__init__()
        if max_value is None:
            self._max_value = 65535
        else:
            self._max_value = max_value

        if min_value is None:
            self._min_value = 224
        else:
            self._min_value = min_value

    def read(self):
        value = super().read()
        normalized_value = (value - self._min_value) / (self._max_value - self._min_value)
        return self._min_value + (int(normalized_value * self._max_value))

    @property
    def max_value(self):
        return self._max_value

    @property
    def mux_logic_a_pin_value(self):
        return 0

    @property
    def mux_logic_b_pin_value(self):
        return 0

    @property
    def pin_id(self):
        return 28
