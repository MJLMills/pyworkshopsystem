from multiplexed_input import MultiplexedInput


class SwitchZ(MultiplexedInput):

    @property
    def mux_logic_a_pin_value(self):
        return 1

    @property
    def mux_logic_b_pin_value(self):
        return 1

    @property
    def mux_io_pin_id(self):
        return 28

    def is_on(self):
        return self.read() == 1

    def is_off(self):
        return not self.is_on()
