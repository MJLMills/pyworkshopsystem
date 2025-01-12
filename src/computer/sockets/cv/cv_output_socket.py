import machine
from input_output import AnalogOutput


class CVOutputSocket(AnalogOutput):  # both AnalogOutput classes have settable ranges to limit output when needed.
    """The CV output sockets of the Computer.

    These sockets use PWM output

    Inverted PWM output.
    Two-pole active filtered. Use 11-bit PWM at 60 kHz.

    The duty cycle is a 16-bit unsigned integer.

    65535 = -6V
    32768 = 0V
    0 = +6V

    Requires firmware calibration for precise values.
    """
    FREQUENCY_KHZ = 60000

    def __init__(self, duty_cycle: int = 32768):
        super().__init__()

        self.pwm = machine.PWM(self.pin_id,
                               freq=60000,
                               duty_u16=duty_cycle,
                               invert=True)

        self._ranged_min_value = RangedVariable(
            min_value=self.hardware_max / 2,
            max_value=0,
            value=0)

        self._ranged_max_value = RangedVariable(
            min_value=self.hardware_max / 2,
            max_value=self.hardware_max,
            value=self.hardware_max)

    @property
    def hardware_min(self) -> int:
        return 0

    @property
    def hardware_max(self) -> int:
        return 65535

    @property
    def min_value(self) -> int:
        """The minimum value of the analog output."""
        return self._ranged_min_value.value

    @min_value.setter
    def min_value(self, min_value: int) -> None:
        """Set the minimum value of the analog output."""
        self._ranged_min_value.value = int(min_value)

    @property
    def max_value(self) -> int:
        """The maximum value of the analog output."""
        return self._ranged_max_value.value

    @max_value.setter
    def max_value(self, max_value: int) -> None:
        """Set the maximum value of the analog output."""
        self._ranged_max_value.value = int(max_value)

    def write(self, value: int):
        """Set the PWM duty cycle equal to the provided unsigned 16-bit int value."""
        self.pwm.duty_u16(int(value))


class CVOutputSocketOne(CVOutputSocket):
    """The first (left-most) CV output socket of the Computer."""

    @property
    def pin_id(self) -> int:
        """The unique identifier of the GPIO pin used by this class."""
        return 23


class CVOutputSocketTwo(CVOutputSocket):
    """The second (right-most) CV output socket of the Computer."""

    @property
    def pin_id(self) -> int:
        """The unique identifier of the GPIO pin used by this class."""
        return 22
