import machine
from base.analog_input import AnalogInput


class Multiplexer(object):
    """The multiplexer attached to the Computer.

    The hardware is a 4052 multiplexer with 2 (ADC pins) by 4 (digitally
    selectable analog input pins) for 8 total channels. The multiplexer has
    two digital output pins (IDs 24 and 25) that are set to specify which
    analog input will be read via the ADC on the GPIO pins (28 and 29). The
    GPIO input pins are connected to analog inputs 2 and 3 on the ADC.

    The truth table is as follows:

    A | B | ADC Channel 2 GPIO 28 | ADC Channel 3 GPIO 29
    --|---|-----------------------|----------------------
    0 | 0 | Main Knob             | CV 1
    1 | 0 | X Knob                | CV 2
    0 | 1 | Y Knob                | CV 1
    1 | 1 | Z Switch              | CV 2

    By default, the multiplexer digital output is set to (0, 0) so reads on pin
    one will return the main knob value and pin two will return the CV 1 input
    value.
    """
    __MUX_LOGIC_A_PIN_ID = 24
    """The ID of the first multiplexer output pin."""
    __MUX_LOGIC_B_PIN_ID = 25
    """The ID of the second multiplexer output pin."""
    MUX_IO_PIN_ONE_ID = 28
    """The ID of the multiplexer's first analog input pin."""
    MUX_IO_PIN_TWO_ID = 29
    """The ID of the multiplexer's second analog input pin."""

    __MUX_LOGIC_A_PIN = machine.Pin(__MUX_LOGIC_A_PIN_ID,
                                    machine.Pin.OUT)
    """The first digital output pin connected to the multiplexer."""

    __MUX_LOGIC_B_PIN = machine.Pin(__MUX_LOGIC_B_PIN_ID,
                                    machine.Pin.OUT)
    """The second digital output pin connected to the multiplexer."""

    __MUX_IO_ADC_ONE = machine.ADC(MUX_IO_PIN_ONE_ID)
    """The ADC connected to the first multiplexer analog output."""

    __MUX_IO_ADC_TWO = machine.ADC(MUX_IO_PIN_TWO_ID)
    """The ADC connected to the second multiplexer analog output."""

    def __init__(self):

        self.mux_logic_pin_a_value = False
        self.mux_logic_pin_b_value = False

    @property
    def mux_logic_pin_a_value(self) -> bool:
        """The value at the first mux logic digital output pin."""
        return self.__MUX_LOGIC_A_PIN.value()

    @mux_logic_pin_a_value.setter
    def mux_logic_pin_a_value(self, value) -> None:
        """Set the value at the first mux logic digital output pin."""
        self.__MUX_LOGIC_A_PIN.value(value)

    @property
    def mux_logic_pin_b_value(self) -> bool:
        """The value at the second mux logic digital output pin."""
        return self.__MUX_LOGIC_B_PIN.value()

    @mux_logic_pin_b_value.setter
    def mux_logic_pin_b_value(self, value) -> None:
        """Set the value at the second mux logic digital output pin."""
        self.__MUX_LOGIC_B_PIN.value(value)

    def set_logic_pin_values(self, value_a: bool, value_b: bool) -> None:
        """Set the values of the multiplexer logic pins.

        Parameters
        ----------
        value_a
            The value to which to set the first multiplexer logic pin.
        value_b
            The value to which to set the second multiplexer logic pin.
        """
        self.mux_logic_pin_a_value = value_a
        self.mux_logic_pin_b_value = value_b

    def get_adc(self, pin_id) -> machine.ADC:
        if pin_id == self.MUX_IO_PIN_ONE_ID:
            return self.__MUX_IO_ADC_ONE
        elif pin_id == self.MUX_IO_PIN_TWO_ID:
            return self.__MUX_IO_ADC_TWO
        else:
            raise ValueError(
                "Supplied pin ID not connected to multiplexer: ", pin_id
            )


class MultiplexedInput(AnalogInput):
    """A multiplexed analog input source.

    The set of analog inputs sharing the multiplexer are the main, x and y
    knobs, the Z switch and CV input sockets 1 and 2. By subclassing this class
    and defining three necessary properties (the ID for the GPIO pin and the
    values for the two multiplexer logic pins), these inputs can all share the
    same implementation of the read method.

    Methods
    -------
    read -> int
        Read the value of this input from the multiplexer.

    Properties
    ----------
    pin_id -> int
        The unique identifier of the GPIO pin used by this class.
    mux_logic_a_pin_value -> bool
        The value of the first multiplexer login pin for this input.
    mux_logic_b_pin_value -> bool
        The value of the second multiplexer login pin for this input.
    adc -> machine.ADC
        The analog-to-digital converter attached to this input.
    """
    def __init__(self):
        super().__init__()
        self.__multiplexer = Multiplexer()
        self._adc = self.__multiplexer.get_adc(self.io_pin_id)

    @property
    def adc(self):
        """The analog-to-digital converter attached to this input."""
        return self._adc

    @property
    def mux_logic_a_pin_value(self) -> bool:
        """The value of the first multiplexer login pin for this input."""
        raise NotImplementedError(
            self.__class__.__name__ + \
            " does not implement mux_logic_a_pin_value."
        )

    @property
    def mux_logic_b_pin_value(self) -> bool:
        """The value of the second multiplexer login pin for this input."""
        raise NotImplementedError(
            self.__class__.__name__ + \
            " does not implement mux_logic_b_pin_value."
        )

    def read(self, set_logic=True) -> None:
        """Set up the multiplexer before reading the value from the ADC."""
        if set_logic:
            self.__multiplexer.set_logic_pin_values(self.mux_logic_a_pin_value,
                                                    self.mux_logic_b_pin_value)

        super().read()

