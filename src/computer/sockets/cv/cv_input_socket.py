from base.multiplexed_input import MultiplexedInput


class CVInputSocket(MultiplexedInput):
    """The CV input sockets of the Computer.

    CV inputs are not inverted.
    -5V reads ~350
    0V reads ~2030
    +5V reads ~3700
    (these are from the docs and are hinting at calibration from the uint12
    values to actual voltages)
    """
    __IO_PIN_ID = 29
    __MIN_VALUE_U16 = 0
    __MAX_VALUE_U16 = 65535

    @property
    def pin_id(self) -> int:
        """The unique identifier of the GPIO pin used by this class."""
        return self.__IO_PIN_ID

    @property
    def min_value(self) -> int:
        return self.__MIN_VALUE_U16

    @property
    def max_value(self) -> int:
        return self.__MAX_VALUE_U16


class CVInputSocketOne(CVInputSocket):
    """The first (left-most) CV input socket of the Computer."""
    __MUX_LOGIC_A_PIN_VALUE = False
    __MUX_LOGIC_B_PIN_VALUE = False

    @property
    def mux_logic_a_pin_value(self) -> bool:
        """The value of the first multiplexer login pin for this input."""
        return self.__MUX_LOGIC_A_PIN_VALUE

    @property
    def mux_logic_b_pin_value(self) -> bool:
        """The value of the second multiplexer login pin for this input."""
        return self.__MUX_LOGIC_B_PIN_VALUE


class CVInputSocketTwo(CVInputSocket):
    """The second (right-most) CV input socket of the Computer."""
    __MUX_LOGIC_A_PIN_VALUE = False
    __MUX_LOGIC_B_PIN_VALUE = True

    @property
    def mux_logic_a_pin_value(self) -> bool:
        """The value of the first multiplexer login pin for this input."""
        return self.__MUX_LOGIC_A_PIN_VALUE

    @property
    def mux_logic_b_pin_value(self) -> bool:
        """The value of the second multiplexer login pin for this input."""
        return self.__MUX_LOGIC_B_PIN_VALUE