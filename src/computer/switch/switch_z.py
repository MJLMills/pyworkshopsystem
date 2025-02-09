from base.multiplexed_input import MultiplexedInput
from src.connect.signal import Signal


class SwitchZ(MultiplexedInput):
    """The Z-switch.

    The switch has three states:

    Up - latching, high value on read - always 65535
    Middle - latching, medium value on read - ranges 32311 to 32407 over 200 secs (converged after 140 secs)
    Down - momentary, low value on read - ranges 176 to 272 over 200 secs (converged after 4 secs)
    """
    __IO_PIN_ID = 28
    __MIN_VALUE_U16 = 0
    __MAX_VALUE_U16 = 65535
    __MUX_LOGIC_A_PIN_VALUE = True
    __MUX_LOGIC_B_PIN_VALUE = True

    __DOWN_MID_BOUNDARY = 16292
    __MID_UP_BOUNDARY = 48971
    __UP_MAX = 65535

    __DOWN = 0
    __MIDDLE = 1
    __UP = 2

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

        self.__set_state()

    @property
    def io_pin_id(self) -> int:
        """The unique identifier of the GPIO pin used by this class."""
        return self.__IO_PIN_ID

    @property
    def min_value(self) -> int:
        return self.__MIN_VALUE_U16

    @property
    def max_value(self) -> int:
        return self.__MAX_VALUE_U16

    @property
    def mux_logic_a_pin_value(self) -> bool:
        """The value of the first multiplexer login pin for this input."""
        return self.__MUX_LOGIC_A_PIN_VALUE

    @property
    def mux_logic_b_pin_value(self) -> bool:
        """The value of the second multiplexer login pin for this input."""
        return self.__MUX_LOGIC_B_PIN_VALUE

    def is_up(self):
        return self.state == self.__UP

    def is_middle(self):
        return self.state == self.__MIDDLE

    def is_down(self):
        return self.state == self.__DOWN

    def __set_state(self):
        super().read()

        value = self.ranged_variable.value
        if 0 <= value < SwitchZ.__DOWN_MID_BOUNDARY:
            self.state = SwitchZ.__DOWN
        elif SwitchZ.__DOWN_MID_BOUNDARY <= value < SwitchZ.__MID_UP_BOUNDARY:
            self.state = SwitchZ.__MIDDLE
        else: # SwitchZ.__MID_UP_BOUNDARY <= value <= SwitchZ.__UP_MAX:
            self.state = SwitchZ.__UP

    def read(self, set_logic=True) -> None:
        """Read the switch and emit appropriate signals."""
        previous_state = self.state
        self.__set_state()

        state = self.state
        if previous_state == SwitchZ.__UP and state == SwitchZ.__MIDDLE:
            self.switched_up_to_middle.emit()
            return

        if previous_state == SwitchZ.__DOWN and state == SwitchZ.__MIDDLE:
            self.switched_down_to_middle.emit()
            return

        if previous_state == SwitchZ.__MIDDLE and state == SwitchZ.__UP:
            self.switched_up.emit()
            return

        if previous_state == SwitchZ.__MIDDLE and state == SwitchZ.__DOWN:
            self.switched_down.emit()
            return
