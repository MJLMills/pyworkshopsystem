import time
from base.digital_output import DigitalOutput


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

    FIRST_LED_PIN_INDEX = 10

    def __init__(self, led_index):
        if led_index not in range(1, 7):
            raise ValueError("Invalid LED index: ", led_index)

        self._pin_id = self.FIRST_LED_PIN_INDEX + (led_index - 1)
        super().__init__()

    @property
    def pin(self):
        return self._pin

    @property
    def pin_id(self) -> int:
        """The unique identifier of the GPIO pin used by this class."""
        return self._pin_id

    def turn_on(self):
        self.pin.value(1)

    def turn_off(self):
        self.pin.value(0)

    def toggle(self):
        if self.value == 1:
            self.turn_off()
        elif self.value == 0:
            self.turn_on()

    @property
    def value(self):
        return self.pin.value()

    @value.setter
    def value(self, value):
        self.pin.value(value)

    def set_value(self, value):
        self.pin.value(value)

    def pulse(self, time_s):
        self.toggle()
        time.sleep(time_s)
        self.toggle()

