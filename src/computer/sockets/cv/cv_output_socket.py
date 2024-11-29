from abc import ABC, abstractmethod
from machine import PWM
from multiplexed_input import IO


class CVOutputSocket(ABC, IO):
    """The CV output sockets of the Computer.

    Inverted PWM output.
    Two-pole active filtered. Use 11-bit PWM at 60 kHz.
    2047 = -6V
    1024 = 0V
    0 = +6V
    Requires firmware calibration for precise values.
    """

    @property
    @abstractmethod
    def pin_id(self):
        pass

    def __init__(self):
        self.pwm = PWM(self.pin_id, freq=60000, duty_u16=32768)

    def write(self, value):
        self.pwm.duty_u16(value)


class CVOutputSocketOne(CVOutputSocket):
    """The first (left-most) CV output socket of the Computer."""
    @property
    def pin_id(self):
        return 23


class CVOutputSocketTwo(CVOutputSocket):
    """The second (right-most) CV output socket of the Computer."""
    @property
    def pin_id(self):
        return 22
