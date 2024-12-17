from multiplexed_input import MultiplexedInput


class SwitchZ(MultiplexedInput):
    """The Z-switch.

    The switch has three states:

    Up - latching, high value on read.
    Middle - latching, medium value on read.
    Down - momentary, low value on read.
    """
    @property
    def mux_logic_a_pin_value(self):
        return 1

    @property
    def mux_logic_b_pin_value(self):
        return 1

    @property
    def pin_id(self) -> int:
        return 28

    def is_up(self) -> bool:
        return self.read() > 50

    def is_down(self) -> bool:
        return self.read() < 10

    def is_middle(self) -> bool:
        if not self.is_up() and not self.is_down():
            return True
        else:
            return False
