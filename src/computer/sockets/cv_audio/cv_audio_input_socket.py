import machine
from base.analog_input import AnalogInput


class CVAudioInputSocket(AnalogInput):
    """The CV/Audio input sockets of the computer.

    The CV/Audio analog inputs are bipolar (inverted) and DC-coupled.
    They require calibration for precise readings.
    The values returned by machine.ADC.read_u16 are in the range:
    +6v = 0
     0v = 32768
    -6v = 65535
    In practice the precision of the internal ADC is closer to 12-bit.

    The left input is normalled to the right input, so if only one
    socket is plugged in, both channels receive the same input.

    The input signals are scaled (presumably in hardware) and then
    go to channels 0 and 1 of an internal analog to digital converter
    (Note that the multiplexer makes use of channels 3 and 4 to read
    the CV inputs, knobs and switch). From there they appear to go to
    two assigned GPIO pins (26 and 27) on the Pi, from which they are
    directly readable as analog inputs.
    """
    __MIN_VALUE_U16 = 32768  # 65535
    __MAX_VALUE_U16 = 0

    # probably introduce a new class to share this across both types of CV input socket
    # the uncalibrated assumption is that +6V = 65535,  0V = 32768, -6V = 0
    # n = m(V) + c, c=32768, m = -65535/12 = -5461
    __GRADIENT = -__MIN_VALUE_U16 / 12
    __INTERCEPT = __MIN_VALUE_U16 / 2

    # calibration of these values is per-socket

    def __init__(self, voltage_range: tuple = None):
        self._adc = machine.ADC(self.io_pin_id)
        self.set_voltage_range(voltage_range)

        super().__init__()

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

    def read(self) -> None:
        """Read a 12-bit uint value from the RP2040's ADC."""
        value = self.ranged_variable.value
        self.ranged_variable.value = self.adc.read_u16()

        if abs(self.ranged_variable.value - value) > 32:
            self.value_changed.emit(ranged_variable=self.ranged_variable)

    @property
    def adc(self):
        return self._adc

    @property
    def min_value(self) -> int:
        return self.__MIN_VALUE_U16

    @property
    def max_value(self) -> int:
        return self.__MAX_VALUE_U16


class CVAudioInputSocketOne(CVAudioInputSocket):
    """The left CV/Audio input socket."""
    __IO_PIN_ID = 27

    @property
    def io_pin_id(self) -> int:
        """The unique identifier of the GPIO pin used by this class."""
        return self.__IO_PIN_ID


class CVAudioInputSocketTwo(CVAudioInputSocket):
    """The right CV/Audio input socket."""
    __IO_PIN_ID = 26

    @property
    def io_pin_id(self) -> int:
        """The unique identifier of the GPIO pin used by this class."""
        return self.__IO_PIN_ID
