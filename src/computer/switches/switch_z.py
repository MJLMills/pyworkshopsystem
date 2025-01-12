from multiplexed_input import MultiplexedInput


class SwitchZ(MultiplexedInput):
    """The Z-switch.

    The switch has three states:

    Up - latching, high value on read - always 65535
    Middle - latching, medium value on read - ranges 32311 to 32407 over 200 secs (converged after 140 secs)
    Down - momentary, low value on read - ranges 176 to 272 over 200 secs (converged after 4 secs)
    """
    # TODO - update these to 12-bit values
    DOWN_MID_BOUNDARY = 16292 #>> 4
    MID_UP_BOUNDARY = 48971 #>> 4
    UP_MAX = 65535 #>> 4

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
        return True

    @property
    def min_value(self) -> int:
        return 0

    @property
    def max_value(self) -> int:
        return 65535

    def is_down(self) -> bool:
        """Determine whether the switch is down."""
        return 0 <= self.latest_value < SwitchZ.DOWN_MID_BOUNDARY

    def is_middle(self) -> bool:
        """Determine whether the switch is in the middle."""
        return SwitchZ.DOWN_MID_BOUNDARY <= self.latest_value < SwitchZ.MID_UP_BOUNDARY

    def is_up(self) -> bool:
        """Determine whether the switch is up."""
        return SwitchZ.MID_UP_BOUNDARY <= self.latest_value <= SwitchZ.UP_MAX
