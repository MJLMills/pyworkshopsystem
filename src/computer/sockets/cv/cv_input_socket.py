from micropython import const
from computer.base.multiplexed_input import MultiplexedInput
from connect.ranged_variable import RangedVariable


class CVInputSocket(MultiplexedInput):
    """The CV input sockets of the Computer.

    CV inputs are inverted.

    Parameters
    ----------
    voltage_range : Tuple[float, float]
        The range of voltages accepted by this CV input socket.
    """
    _IO_PIN_ID: int = const(29)

    __MIN_VALUE_U16 = 65535
    __MAX_VALUE_U16 = 0

    # probably introduce a new class to share this across both types of CV input socket
    # the uncalibrated assumption is that +6V = 65535,  0V = 32768, -6V = 0
    # n = m(V) + c, c=32768, m = -65535/12 = -5461
    __GRADIENT = -__MIN_VALUE_U16 / 12
    __INTERCEPT = __MIN_VALUE_U16 / 2

    # calibration of these values is per-socket

    def __init__(self, voltage_range: tuple = None):

        self.set_voltage_range(voltage_range)

        super().__init__(
            self._IO_PIN_ID,
            self._MUX_LOGIC_A_PIN_VALUE,
            self._MUX_LOGIC_B_PIN_VALUE,
        )

    def set_voltage_range(self,
                          voltage_range: tuple = None):  # needs to mess with the ranged variable's extrema

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

        self.ranged_variable = RangedVariable(
            value=self.min_value,
            minimum=self.min_value,
            maximum=self.max_value
        )

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
    _MUX_LOGIC_A_PIN_VALUE = const(0)
    _MUX_LOGIC_B_PIN_VALUE = const(1)

    def __init__(self):
        super().__init__(
            self._IO_PIN_ID,
            self._MUX_LOGIC_A_PIN_VALUE,
            self._MUX_LOGIC_B_PIN_VALUE,
        )


class CVInputSocketTwo(CVInputSocket):
    """The second (right-most) CV input socket of the Computer."""
    _MUX_LOGIC_A_PIN_VALUE = const(1)
    _MUX_LOGIC_B_PIN_VALUE = const(0)

    def __init__(self):
        super().__init__(
            self._IO_PIN_ID,
            self._MUX_LOGIC_A_PIN_VALUE,
            self._MUX_LOGIC_B_PIN_VALUE,
        )