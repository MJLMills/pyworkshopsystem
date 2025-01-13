from base.hardware_component import HardwareComponent
from src.connect.ranged_variable import RangedVariable


class AnalogOutput(HardwareComponent):
    """A hardware analog output.

    There are four analog outputs on the Computer, each of which is a socket.
    Two are dedicated to CV and are written to using PWM. The other two may be
    used for CV or audio, and are written to through the Computer's DAC.

    See Also
    --------
    CVAudioOutputSocket
        The CV/Audio output sockets of the Computer.
    CVOutputSocket
        The CV output sockets of the Computer.
    """
    def __init__(self):
        self.ranged_variable = RangedVariable(
            value=self.min_value,
            minimum=self.min_value,
            maximum=self.max_value
        )

    @property
    def min_value(self) -> int:
        raise NotImplementedError(
            self.__class__.__name__ + " does not implement min_value."
        )

    @property
    def max_value(self) -> int:
        raise NotImplementedError(
            self.__class__.__name__ + " does not implement max_value."
        )

    @property
    def hardware_min(self) -> int:
        raise NotImplementedError(
            self.__class__.__name__ + " does not implement max_value."
        )

    @property
    def hardware_max(self) -> int:
        raise NotImplementedError(
            self.__class__.__name__ + " does not implement max_value."
        )

    def write(self, value):
        raise NotImplementedError(
            self.__class__.__name__ + " does not implement write."
        )
