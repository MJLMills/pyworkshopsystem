from micropython import const
import machine
from computer.base.analog_input import AnalogInput


_MUX_IO_PIN_ONE_ID = const(28)
_MUX_IO_PIN_TWO_ID = const(29)


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
    _MUX_LOGIC_A_PIN = machine.Pin(24, machine.Pin.OUT)
    _MUX_LOGIC_B_PIN = machine.Pin(25, machine.Pin.OUT)

    _MUX_IO_ADC_ONE = machine.ADC(_MUX_IO_PIN_ONE_ID)
    _MUX_IO_ADC_TWO = machine.ADC(_MUX_IO_PIN_TWO_ID)

    _instance = None

    def __init__(self):

        if Multiplexer._instance is not None:
            raise RuntimeError("Multiplexer already initialized")

        Multiplexer._instance = self

        self._pin_a_value = getattr(self._MUX_LOGIC_A_PIN, "value")
        self._pin_b_value = getattr(self._MUX_LOGIC_B_PIN, "value")

    @classmethod
    def get_instance(cls):
        """Return the instance of the Multiplexer class."""
        if cls._instance is None:
            cls._instance = Multiplexer()
        return cls._instance

    def set_logic_pin_values(self, value_a: int, value_b: int) -> None:
        """Set the GPIO pin values for this multiplexer."""
        self._pin_a_value(value_a)
        self._pin_b_value(value_b)

    def get_adc(self, pin_id: int) -> machine.ADC:
        """Get the ADC corresponding to a specified GPIO pin ID."""
        if pin_id == _MUX_IO_PIN_ONE_ID:
            return self._MUX_IO_ADC_ONE
        elif pin_id == _MUX_IO_PIN_TWO_ID:
            return self._MUX_IO_ADC_TWO
        else:
            raise ValueError("Supplied pin ID not connected to multiplexer: ", pin_id)


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
    def __init__(self,
                 pin_id: int,
                 mux_logic_a_pin_value: int,
                 mux_logic_b_pin_value: int):

        super().__init__()

        multiplexer = Multiplexer.get_instance()

        self._adc = multiplexer.get_adc(pin_id)
        self._adc_read_u16 = self._adc.read_u16
        self._mux_logic_set_pin_values = getattr(multiplexer, "set_logic_pin_values")

        self._mux_logic_a_pin_value = mux_logic_a_pin_value
        self._mux_logic_b_pin_value = mux_logic_b_pin_value

        self._analog_input_read = super().read

    def set_logic_pin_values(self) -> None:
        """Set the values of the multiplexer logic pins for this analog input."""
        self._mux_logic_set_pin_values(
            self._mux_logic_a_pin_value,
            self._mux_logic_b_pin_value
        )

    def set_and_read(self) -> None:
        """Set multiplexer pins before reading the value from the ADC."""
        self.set_logic_pin_values()
        self._analog_input_read()

    def read_norm_probe(self) -> bool:
        self.set_logic_pin_values()
        return self._adc.read_u16() < 28000