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

        # TODO - this is attenuating behaviour, add attenuversion
        # user should not set min_value.minimum or maximum
        self.min_value = RangedVariable(
            minimum=0,
            maximum=self.hardware_max / 2,  # touchy
            value=0
        )

        self.max_value = RangedVariable(
            minimum=self.hardware_max / 2,
            maximum=self.hardware_max,
            value=0
        )

        self.ranged_variable = RangedVariable(
            value=self.min_value.value,
            minimum=self.min_value,
            maximum=self.max_value
        )

    def map_min_value(self, ranged_variable):
        self.min_value.map_value(ranged_variable)

    def map_max_value(self, ranged_variable):
        self.max_value.map_value(ranged_variable)

    def map_range(self, ranged_variable):
        self.min_value.map_value(ranged_variable)
        self.max_value.map_value(ranged_variable)

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

    def map_and_write_value(self, ranged_variable):
        self.ranged_variable.map_value(ranged_variable)
        self.write(self.ranged_variable.value)
