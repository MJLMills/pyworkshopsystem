from from abc import ABC, abstractmethod
from machine import PWM
from src.computer.sockets import OutputSocket

class CVOutputSocket(ABC):
    """
    This should be an abc, the pin_id is an abstract property.

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
        return self.PIN_ID

    def __init__(self):
        self.pwm = PWM(self.PIN_ID, freq=60000, duty_u16=32768)

    def write(self, value):
        self.pwm.duty_u16(value)


class CVOutputSocketOne(OutputSocket):
    PIN_ID = 23
    ...


class CVOutputSocketTwo(OutputSocket):
    PIN_ID = 22
    ...
