import machine
from abc import ABC, abstractmethod


# multiplexer should be a module to avoid multiple instances of this class
class Multiplexer(object):
    """The multiplexer on the Computer.

    This is a 4052 multiplexer with 2x4 channels.
    The multiplexer has two output pins that are set to
    determine which analog input will be read via the ADC on
    the I/O pins. The uC I/O pins are connected to analog inputs
    2 and 3 from the multiplexer.

    Truth table is as follows:

    A | B | ADC Channel 2 GPIO 28 | ADC Channel 3 GPIO 29
    --|---|-----------------------|----------------------
    0 | 0 | Main Knob             | CV 1
    0 | 1 | X Knob                | CV 2
    1 | 0 | Y Knob                | CV 1
    1 | 1 | Z Switch              | CV 2
    """
    MUX_LOGIC_A_PIN_ID = 24
    """The ID of the first multiplexer output pin."""
    MUX_LOGIC_B_PIN_ID = 25
    """The ID of the second multiplexer output pin."""
    MUX_IO_PIN_ONE_ID = 28
    """The ID of the first multiplexer I/O pin."""
    MUX_IO_PIN_TWO_ID = 29
    """The ID of the second multiplexer I/O pin."""

    MUX_LOGIC_A_PIN = machine.Pin(MUX_LOGIC_A_PIN_ID,
                                  machine.Pin.OUT)

    MUX_LOGIC_B_PIN = machine.Pin(MUX_LOGIC_B_PIN_ID,
                                  machine.Pin.OUT)

    MUX_IO_ADC_ONE = machine.ADC(MUX_IO_PIN_ONE_ID)
    MUX_IO_ADC_TWO = machine.ADC(MUX_IO_PIN_TWO_ID)

    def __init__(self):
        self.mux_logic_pin_a_value = 0
        self.mux_logic_pin_b_value = 0

    @property
    def mux_logic_pin_a_value(self):
        return self.MUX_LOGIC_A_PIN.value()

    @mux_logic_pin_a_value.setter
    def mux_logic_pin_a_value(self, value):
        self.MUX_LOGIC_A_PIN.value(value)

    @property
    def mux_logic_pin_b_value(self):
        return self.MUX_LOGIC_B_PIN.value()

    @mux_logic_pin_b_value.setter
    def mux_logic_pin_b_value(self, value):
        self.MUX_LOGIC_B_PIN.value(value)

    def set_logic_pin_values(self, a, b):
        """Set the values of the logic pins."""
        self.mux_logic_pin_a_value = a
        self.mux_logic_pin_b_value = b

    @staticmethod
    def read(pin_id):
        return machine.ADC(pin_id).read_u16()


class IO(ABC):

    @property
    @abstractmethod
    def pin_id(self):
        pass

class MultiplexedInput(ABC, IO):
    """A multiplexed source of data.

    The set of inputs sharing the multiplexer are the main, x and y knobs,
    the Z switch and CV input sockets 1 and 2. By subclassing this class
    and defining the three abstract properties, these inputs can all share
    the same implementation of the read method.

    Methods
    -------
    read
        Read the value of this input from the multiplexer.
    """
    def __init__(self):
        super().__init__()
        self.__multiplexer = Multiplexer()


    @property
    @abstractmethod
    def mux_logic_a_pin_value(self):
        pass

    @property
    @abstractmethod
    def mux_logic_b_pin_value(self):
        pass

    def read(self):
        self.__multiplexer.set_logic_pin_values(self.mux_logic_a_pin_value,
                                                self.mux_logic_b_pin_value)

        return self.__multiplexer.read(self.pin_id)
