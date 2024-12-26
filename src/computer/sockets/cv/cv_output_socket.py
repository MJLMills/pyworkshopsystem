from machine import PWM
from multiplexed_input import IO


class CVOutputSocket(IO):
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
        self.pwm = PWM(self.pin_id,
                       freq=60000,
                       duty_u16=duty_cycle)

    def write(self, value):
        self.pwm.duty_u16(65535 - value)

    def write_norm_value(self, value):
        if not (0.0 <= value <= 1.0):
            print("Normalized input exceeded range:", value)

        self.write(int((1.0 - value) * 65535))


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
