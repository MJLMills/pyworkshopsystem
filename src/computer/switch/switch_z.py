from micropython import const
from computer.base.multiplexed_input import MultiplexedInput
from connect.signal import Signal


class SwitchZ(MultiplexedInput):
    """The Z-switch.

    The switch has three states:

    Up - latching, high value on read - always 65535
    Middle - latching, medium value on read - ranges 32311 to 32407 over 200 secs (converged after 140 secs)
    Down - momentary, low value on read - ranges 176 to 272 over 200 secs (converged after 4 secs)

    values corresponding to each state:
    DOWN = 0
    MIDDLE = 1
    UP = 2
    Direct values are used for comparisons to save time.

    Read values at the boundary between the three switch states:
    DOWN_MID_BOUNDARY = 16292
    MID_UP_BOUNDARY = 48971
    UP_MAX = 65535
    Direct values are used for comparisons to save time.

    """
    IO_PIN_ID = const(28)
    MIN_VALUE_U16 = const(0)
    MAX_VALUE_U16 = const(65535)
    MUX_LOGIC_PIN_A_VALUE = const(True)
    MUX_LOGIC_PIN_B_VALUE = const(True)

    def __init__(self):

        super().__init__()

        self.switched_up = Signal()
        """Signal emitted when the switch is moved to the up position."""
        self.switched_up_to_middle = Signal()
        """Signal emitted when the switch is moved from the up to the middle position."""
        self.switched_down_to_middle = Signal()
        """Signal emitted when the switch is moved from the down to the middle position."""
        self.switched_down = Signal()
        """Signal emitted when the switch is moved to the down position."""

        # State transition map: (previous_state, current_state) -> signal
        self._transitions = {
            (2, 1): self.switched_up_to_middle,  # UP -> MIDDLE
            (0, 1): self.switched_down_to_middle,  # DOWN -> MIDDLE
            (1, 2): self.switched_up,  # MIDDLE -> UP
            (1, 0): self.switched_down,  # MIDDLE -> DOWN
        }

        self.__set_state()

    @property
    def min_value(self) -> int:
        return SwitchZ.MIN_VALUE_U16

    @property
    def max_value(self) -> int:
        return SwitchZ.MAX_VALUE_U16

    def is_up(self):
        return self.state == 2

    def is_middle(self):
        return self.state == 1

    def is_down(self):
        return self.state == 0

    def __set_state(self):
        super().read()

        value = self.ranged_variable.value
        if 0 <= value < 16292:
            self.state = 0  # switch is down
        elif 16292 <= value < 48971:
            self.state = 1  # switch is in the middle
        else: # 48971 <= value <= 65535:
            self.state = 2  # switch is up

    def read(self, set_logic=True) -> None:
        """Read the switch and emit appropriate signals."""
        previous_state = self.state
        self.__set_state()

        signal_to_emit = self._transitions.get((previous_state, self.state))
        if signal_to_emit:
            signal_to_emit.emit()
