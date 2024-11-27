from multiplexed_source import MultiplexedSource


class MainKnob(MultiplexedSource):

    @property
    def mux_logic_a_pin_value(self):
        return 0

    @property
    def mux_logic_b_pin_value(self):
        return 0

    @property
    def mux_io_pin_id(self):
        return 28
