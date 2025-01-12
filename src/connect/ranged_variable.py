from typing import Union


class RangedVariable(object):
    """A variable constrained to a specific range.

    The variable has a value that is constrained to lie within a specific
    range. It is designed to enable mappings to be constructed between
    pairs of ranged variables. The formula to compute an output value for a
    given input value requires the input value and the minimum and maximum
    values of the input and output values.

    Hardware variables are inherently ranged. For inputs, variables read
    from an ADC or digital pin will have fixed ranges. For outputs, hardware
    imposes a limit on the range of values that can be written.
    """
    def __init__(self,
                 value: Union[int, float],
                 minimum: Union[int, float, "RangedVariable"],
                 maximum: Union[int, float, "RangedVariable"]):

        self._minimum = minimum
        self._maximum = maximum
        self.value = value

    @property
    def value(self) -> Union[int, float]:
        """The current value of this ranged variable."""
        return self._value

    @value.setter
    def value(self, value: Union[int, float]) -> None:
        """Set the current value of this ranged variable."""
        if self.minimum_value <= value <= self.maximum_value:
            self._value = value
        else:
            raise ValueError(f"Value outside range: {value}, {self._minimum}, {self._maximum}")

    @property
    def minimum_value(self) -> Union[int, float]:
        """The minimum value of this ranged variable."""
        if isinstance(self._minimum, RangedVariable):
            return self._minimum.value
        else:
            return self._minimum

    @minimum_value.setter
    def minimum_value(self, minimum: Union[int, float]) -> None:
        """Set the minimum value of this ranged variable."""
        if isinstance(self._minimum, RangedVariable):
            self._minimum.value = minimum
        else:
            self._minimum = minimum

    @property
    def maximum_value(self) -> Union[int, float]:
        """The maximum value of this ranged variable."""
        if isinstance(self._maximum, RangedVariable):
            return self._maximum.value
        else:
            return self._maximum

    @maximum_value.setter
    def maximum_value(self, maximum: Union[int, float]) -> None:
        """Set the maximum value of this ranged variable."""
        if isinstance(self._maximum, RangedVariable):
            self._maximum.value = maximum
        else:
            self._maximum = maximum

    def update_value(self):
        """Update the value of this ranged variable."""
        pass

    def __str__(self):
        str_rep = self.__class__.__name__ + ": "
        str_rep += f"value = {self.value}, "
        str_rep += f"minimum value = {self.minimum_value}, "
        str_rep += f"maximum value = {self.maximum_value}"

        return str_rep
