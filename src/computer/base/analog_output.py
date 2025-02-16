from base.hardware_component import HardwareComponent
from src.connect.ranged_variable import RangedVariable


class AnalogOutput(HardwareComponent):
    """A hardware analog output.

    There are four analog outputs on the Computer, each of which is a socket.
    Two are dedicated to CV and are written to using PWM. The other two may be
    used for CV or audio, and are written to through the Computer's DAC.

    Parameters
    ----------
    m : int

    See Also
    --------
    CVAudioOutputSocket
        The CV/Audio output sockets of the Computer.
    CVOutputSocket
        The CV output sockets of the Computer.
    """

    def __init__(self, m: int = 0):
        self.min_value = RangedVariable(
            minimum=self.hardware_max / 2,
            maximum=m,
            value=0
        )

        self.max_value = RangedVariable(
            minimum=self.hardware_max / 2,
            maximum=self.hardware_max - m,
            value=self.hardware_max - m
        )

        self.ranged_variable = RangedVariable(
            value=self.min_value.value,
            minimum=self.min_value,
            maximum=self.max_value
        )

    @property
    def hardware_min(self) -> int:
        """The minimum value writeable to this analog output."""
        raise NotImplementedError(
            self.__class__.__name__ + " does not implement max_value."
        )

    @property
    def hardware_max(self) -> int:
        """The maximum value writeable to this analog output."""
        raise NotImplementedError(
            self.__class__.__name__ + " does not implement max_value."
        )

    def write(self, value):
        """Write the provided value to this analog output."""
        raise NotImplementedError(
            self.__class__.__name__ + " does not implement write."
        )

    def map_min_value(self, ranged_variable):
        """Update this analog output's ranged variable's minimum's value from another.

        Parameters
        ----------
        ranged_variable : RangedVariable
            The ranged variable from which to map this analog output's ranged variable's minimum's value.
        """
        self.min_value.map_value(ranged_variable)

    def map_max_value(self, ranged_variable):
        """Update this analog output's ranged variable's maximum's value from another.

        Parameters
        ----------
        ranged_variable : RangedVariable
            The ranged variable from which to map this analog output's ranged variable's maximum's value.
        """
        self.max_value.map_value(ranged_variable)

    def map_range(self, ranged_variable):
        """Update this analog output's range from a ranged variable.

        Parameters
        ----------
        ranged_variable : RangedVariable
            The ranged variable from which to map this analog output's range.
        """

        self.min_value.map_value(ranged_variable)
        self.max_value.map_value(ranged_variable)

    def map_and_write_value(self, ranged_variable):
        """Update and write the value of this analog output's ranged variable from another.

        Parameters
        ----------
        ranged_variable : RangedVariable
            The ranged variable from which to map this analog output's ranged variable's value.
        """
        self.ranged_variable.map_value(ranged_variable)
        self.write(self.ranged_variable.value)
