import machine
from .input_output import IO


class Multiplexer(object):
    """The multiplexer on the Computer.

    This is a 4052 multiplexer with 2x4 channels. The multiplexer has two
    digital output pins (IDs 24 and 25) that are set to specify which analog
    input will be read via the ADC on the GPIO pins (28 and 29). The GPIO
    input pins are connected to analog inputs 2 and 3 on the ADC.

    The truth table is as follows:

    A | B | ADC Channel 2 GPIO 28 | ADC Channel 3 GPIO 29
    --|---|-----------------------|----------------------
    0 | 0 | Main Knob             | CV 1
    1 | 0 | X Knob                | CV 2
    0 | 1 | Y Knob                | CV 1
    1 | 1 | Z Switch              | CV 2
    """
    __MUX_LOGIC_A_PIN_ID = 24
    """The ID of the first multiplexer output pin."""
    __MUX_LOGIC_B_PIN_ID = 25
    """The ID of the second multiplexer output pin."""
    MUX_IO_PIN_ONE_ID = 28
    """The ID of the first multiplexer I/O pin."""
    MUX_IO_PIN_TWO_ID = 29
    """The ID of the second multiplexer I/O pin."""

    __MUX_LOGIC_A_PIN = machine.Pin(__MUX_LOGIC_A_PIN_ID,
                                    machine.Pin.OUT)
    """The digital output pin connected to the first multiplexer output."""

    __MUX_LOGIC_B_PIN = machine.Pin(__MUX_LOGIC_B_PIN_ID,
                                    machine.Pin.OUT)
    """The digital output pin connected to the second multiplexer output."""

    __MUX_IO_ADC_ONE = machine.ADC(MUX_IO_PIN_ONE_ID)
    __MUX_IO_ADC_TWO = machine.ADC(MUX_IO_PIN_TWO_ID)

    def __init__(self):
        self.mux_logic_pin_a_value = False
        self.mux_logic_pin_b_value = False

    @property
    def mux_logic_pin_a_value(self):
        return self.__MUX_LOGIC_A_PIN.value()

    @mux_logic_pin_a_value.setter
    def mux_logic_pin_a_value(self, value):
        self.__MUX_LOGIC_A_PIN.value(value)

    @property
    def mux_logic_pin_b_value(self):
        return self.__MUX_LOGIC_B_PIN.value()

    @mux_logic_pin_b_value.setter
    def mux_logic_pin_b_value(self, value):
        self.__MUX_LOGIC_B_PIN.value(value)

    def set_logic_pin_values(self, a: bool, b: bool):
        """Set the values of the multiplexer logic pins."""
        self.mux_logic_pin_a_value = a
        self.mux_logic_pin_b_value = b

    @staticmethod
    def read(pin_id):  # TODO - cache the per-pin ADCs
        return machine.ADC(pin_id).read_u16()


class MultiplexedInput(IO):
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
    """
    def __init__(self):
        super().__init__()
        self.__multiplexer = Multiplexer()

    @property
    def mux_logic_a_pin_value(self) -> bool:
        raise NotImplementedError(
            self.__class__.__name__ + \
            " does not implement mux_logic_a_pin_value."
        )

    @property
    def mux_logic_b_pin_value(self) -> bool:
        raise NotImplementedError(
            self.__class__.__name__ + \
            " does not implement mux_logic_b_pin_value."
        )

    def read(self) -> int:
        """Set up the multiplexer and read the value."""
        self.__multiplexer.set_logic_pin_values(self.mux_logic_a_pin_value,
                                                self.mux_logic_b_pin_value)

        return self.__multiplexer.read(self.pin_id)
