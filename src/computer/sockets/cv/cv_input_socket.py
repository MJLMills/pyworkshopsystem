from base.multiplexed_input import MultiplexedInput


class CVInputSocket(MultiplexedInput):
    """The CV input sockets of the Computer.

    CV inputs are inverted.

    Parameters
    ----------
    voltage_range : Tuple[float, float]
        The range of voltages accepted by this CV input socket.
    """
    __IO_PIN_ID = 29
    __MIN_VALUE_U16 = 65535
    __MAX_VALUE_U16 = 0

    # probably introduce a new class to share this across both types of CV input socket
    # the uncalibrated assumption is that +6V = 65535,  0V = 32768, -6V = 0
    # n = m(V) + c, c=32768, m = -65535/12 = -5461
    __GRADIENT = -__MIN_VALUE_U16 / 12
    __INTERCEPT = __MIN_VALUE_U16 / 2

    # calibration of these values is per-socket

    def __init__(self, voltage_range: tuple = None):

        if voltage_range is None:
            self._min_value = self.__MIN_VALUE_U16
            self._max_value = self.__MAX_VALUE_U16
        else:

            if voltage_range[0] is None:
                self._min_value = self.__MIN_VALUE_U16
            else:
                self._min_value = int(
                    (self.__GRADIENT * voltage_range[0]) + self.__INTERCEPT)
                # compute max_value from the voltage value
                # n = mV + c for max
                # for a socket, assuming a perfect linear relationship, only
                # need to store m  (-5504.4) and c (33334) per socket based on
                # a calibration procedure

            if voltage_range[1] is None:
                self._max_value = self.__MAX_VALUE_U16
            else:
                self._max_value = int(
                    (self.__GRADIENT * voltage_range[1]) + self.__INTERCEPT)

        super().__init__()

    @property
    def io_pin_id(self) -> int:
        """The unique identifier of the GPIO pin used by this class."""
        return self.__IO_PIN_ID

    @property
    def min_value(self) -> int:
        return self._min_value

    @property
    def max_value(self) -> int:
        return self._max_value

    def __str__(self):
        return f"min={self._min_value}, max={self._max_value}"


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
    __MUX_LOGIC_A_PIN_VALUE = True
    __MUX_LOGIC_B_PIN_VALUE = False

    @property
    def mux_logic_a_pin_value(self) -> bool:
        """The value of the first multiplexer login pin for this input."""
        return self.__MUX_LOGIC_A_PIN_VALUE

    @property
    def mux_logic_b_pin_value(self) -> bool:
        """The value of the second multiplexer login pin for this input."""
        return self.__MUX_LOGIC_B_PIN_VALUE