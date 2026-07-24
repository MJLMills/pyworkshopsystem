from micropython import const
from computer.base.digital_output import DigitalOutput


class LED(DigitalOutput):
    """A light emitting diode on the module.

    If the pin value is set to 1 (i.e. True), the LED is illuminated.

    Properties
    ----------
    value
        The value of this LED.
    """
    ON_VALUE = const(1)
    OFF_VALUE = const(0)
    FIRST_LED_PIN_INDEX = const(10)

    def __init__(self, led_index):
        if led_index not in range(1, 7):
            raise ValueError("Invalid LED index: ", led_index)

        self.io_pin_id = self.FIRST_LED_PIN_INDEX + (led_index - 1)
        super().__init__()

    def _resolve_pin_id(self):
        return self.io_pin_id
