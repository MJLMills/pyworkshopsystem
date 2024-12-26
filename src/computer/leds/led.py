import machine
from multiplexed_input import IO


class LED(IO):
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

    FIRST_LED_PIN_INDEX = 10

    def __init__(self, led_index):
        if led_index not in range(1, 7):
            raise ValueError("Invalid LED index: ", led_index)

        self._pin_id = self.FIRST_LED_PIN_INDEX + (led_index - 1)
        self.pin = machine.Pin(self.pin_id,
                               machine.Pin.OUT)

    @property
    def pin_id(self) -> int:
        """The unique identifier of the GPIO pin used by this class."""
        return self._pin_id

    def turn_on(self):
        self.pin.value(1)

    def turn_off(self):
        self.pin.value(0)

    @property
    def value(self):
        return self.pin.value()

    @value.setter
    def value(self, value):
        self.pin.value(value)
