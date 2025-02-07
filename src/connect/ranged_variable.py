class RangedVariable(object):
    """A variable constrained to a specific range.

    The variable has a value that is constrained to lie within a specific
    (modifiable) range. It is designed to enable mappings to be constructed
    between pairs of ranged variables. The formula to compute an output value
    for a given input value requires the input value and the minimum and
    maximum values of the input and output values.

    Hardware variables are inherently ranged. For inputs, variables read
    from an ADC or digital pin will have fixed ranges. For outputs, hardware
    imposes a limit on the range of values that can be written.

    Parameters
    ----------
    value : int or float
        The current value of this ranged variable.
    minimum : int or float or RangedVariable
        The lowest allowed value of this ranged variable.
        This may itself be a ranged variable.
    maximum : int or float or RangedVariable
        The highest allowed value of this ranged variable.
        This may itself be a ranged variable.
    """

    def __init__(self,
                 value,
                 minimum,
                 maximum):

        self._minimum = minimum
        self._maximum = maximum
        self._value = value

        self._numerical_min = min(self.minimum_value, self.maximum_value)
        self._numerical_max = max(self.minimum_value, self.maximum_value)

    @property
    def value(self):
        """The current value of this ranged variable."""
        return self._value

    @value.setter
    def value(self, value) -> None:
        """Set the current value of this ranged variable.

        This method ensures that the range of the ranged variable is respected.

        Parameters
        ----------
        value : int or float
            The value to which to set this ranged variable's value.
        """
        if self._numerical_min <= value <= self._numerical_max:
            self._value = value

    @property
    def minimum(self):
        """The minimum of this ranged variable.

        Returns
        -------
        int or float or RangedVariable
            The lowest allowed value of this ranged variable.
        """
        return self._minimum

    @property
    def maximum(self):
        """The maximum of this ranged variable.

        Returns
        -------
        int or float or RangedVariable
            The highest allowed value of this ranged variable.
        """
        return self._maximum

    @property
    def minimum_value(self):
        """The current value of the minimum of this ranged variable.

        This method always returns the numerical value of the minimum, whether
        it is inherently numerical or a ranged variable.

        Returns
        -------
        int or float
            The current value of the minimum of this ranged variable.
        """
        if isinstance(self._minimum, RangedVariable):
            return self._minimum.value
        else:
            return self._minimum

    @minimum_value.setter
    def minimum_value(self, minimum) -> None:
        """Set the value of the minimum of this ranged variable.

        Parameters
        ----------
        minimum : int or float
            The value to which to set the minimum of this ranged variable.
        """
        if isinstance(self._minimum, RangedVariable):
            self._minimum.value = minimum
        else:
            self._minimum = minimum

        self._numerical_min = min(self.minimum_value, self.maximum_value)
        self._numerical_max = max(self.minimum_value, self.maximum_value)

    @property
    def maximum_value(self):
        """The current value of the maximum of this ranged variable.

        This method always returns the numerical value of the maximum, whether
        it is inherently numerical or a ranged variable.

        Returns
        -------
        int or float
            The current value of the maximum of this ranged variable.
        """
        if isinstance(self._maximum, RangedVariable):
            return self._maximum.value
        else:
            return self._maximum

    @maximum_value.setter
    def maximum_value(self, maximum) -> None:
        """Set the value of the maximum of this ranged variable.

        Parameters
        ----------
        maximum : int or float
            The value to which to set the maximum of this ranged variable.
        """
        if isinstance(self._maximum, RangedVariable):
            self._maximum.value = maximum
        else:
            self._maximum = maximum

        self._numerical_min = min(self.minimum_value, self.maximum_value)
        self._numerical_max = max(self.minimum_value, self.maximum_value)

    @property
    def value_range(self):
        """The range of values which this ranged variable can take.

        Returns
        -------
        int or float
            The range of values which this ranged variable can take.
        """
        return self.maximum_value - self.minimum_value

    def map_value(self, ranged_variable):
        """Update the value of this ranged variable from another.

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

    def __str__(self) -> str:
        """Create a human-readable representation of this object."""
        str_rep = self.__class__.__name__ + ": "
        str_rep += f"value = {self._value}, "
        str_rep += f"minimum value ({type(self._minimum)}) = {self._minimum}, "
        str_rep += f"maximum value ({type(self._minimum)}) = {self._maximum}"

        return str_rep
