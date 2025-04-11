from computer.base.digital_output import DigitalOutput


class LED(DigitalOutput):
    """A light emitting diode on the module.

    If the pin value is set to 1 (i.e. True), the LED is illuminated.

    Methods
    -------
    turn_on
        Turn this LED on.
    turn_off
        Turn this LED off.

    Properties
    ----------
    value
        The value of this LED.
    """
    __ON_VALUE = 1
    __OFF_VALUE = 0
    __FIRST_LED_PIN_INDEX = 10

    def __init__(self, led_index):
        if led_index not in range(1, 7):
            raise ValueError("Invalid LED index: ", led_index)

        self._pin_id = self.__FIRST_LED_PIN_INDEX + (led_index - 1)
        super().__init__()

    @property
    def io_pin_id(self) -> int:
        """The unique identifier of the GPIO pin used by this class."""
        return self._pin_id

    @property
    def on_value(self) -> int:
        """The value used to represent "on" for this digital output."""
        return self.__ON_VALUE

    @property
    def off_value(self) -> int:
        """The value used to represent "off" for this digital output."""
        return self.__OFF_VALUE
