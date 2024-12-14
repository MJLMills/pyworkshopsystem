from multiplexed_input import MultiplexedInput


class KnobX(MultiplexedInput):

    @property
    def mux_logic_a_pin_value(self):
        return 0

    @property
    def mux_logic_b_pin_value(self):
        return 1

    @property
    def pin_id(self):
        return 28

    def read(self):
        value = super().read()
        return value
