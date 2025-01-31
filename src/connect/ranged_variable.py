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

    Parameters
    ----------
    value : int or float
    minimum : int or float or RangedVariable
    maximum : int or float or RangedVariable
    """

    def __init__(self,
                 value,
                 minimum,
                 maximum):

        self._minimum = minimum
        self._maximum = maximum
        self.value = value

    @property
    def value(self):
        """The current value of this ranged variable.

        Returns
        -------
        int or float
        """
        return self._value

    @value.setter
    def value(self, value) -> None:
        """Set the current value of this ranged variable.

        Parameters
        ----------
        value : int or float
        """
        # if self.minimum_value <= value <= self.maximum_value:
        self._value = value
        # else:
        #    raise ValueError(f"Value outside range: {value}, {self._minimum}, {self._maximum}")

    @property
    def minimum_value(self):
        """The minimum value of this ranged variable.


        Returns
        -------
        int or float
        """
        if isinstance(self._minimum, RangedVariable):
            return self._minimum.value
        else:
            return self._minimum

    @minimum_value.setter
    def minimum_value(self, minimum) -> None:
        """Set the minimum value of this ranged variable.

        Parameters
        ----------
        value : int or float
        """
        if isinstance(self._minimum, RangedVariable):
            self._minimum.value = minimum
        else:
            self._minimum = minimum

    @property
    def maximum_value(self):
        """The maximum value of this ranged variable.

        Returns
        -------
        int or float
        """
        if isinstance(self._maximum, RangedVariable):
            return self._maximum.value
        else:
            return self._maximum

    @maximum_value.setter
    def maximum_value(self, maximum) -> None:
        """Set the maximum value of this ranged variable.

        Parameters
        ----------
        value : int or float
        """
        if isinstance(self._maximum, RangedVariable):
            self._maximum.value = maximum
        else:
            self._maximum = maximum

    @property
    def value_range(self):
        return self.maximum_value - self.minimum_value

    def map_value(self, ranged_variable):
        """Update the value of this ranged variable.

        This method has access to this variable's ranges, and the value and
        ranges of the variable it is to be updated from.
        Using this as a slot will require re-computation of the slope each
        time the signal fires. To avoid this would need a permanent object
        with a slot to connect to the signal which can update this variable.

        Parameters
        ----------
        ranged_variable : RangedVariable
        """
        slope = self.value_range / ranged_variable.value_range
        self.value = self.minimum_value + (slope * (
                ranged_variable.value - ranged_variable.minimum_value))

    def __str__(self):
        str_rep = self.__class__.__name__ + ": "
        str_rep += f"value = {self.value}, "
        str_rep += f"minimum value = {self.minimum_value}, "
        str_rep += f"maximum value = {self.maximum_value}"

        return str_rep
