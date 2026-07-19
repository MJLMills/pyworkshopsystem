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
    ON_VALUE = 1
    OFF_VALUE = 0
    _FIRST_LED_PIN_INDEX = 10

    def __init__(self, led_index):
        if led_index < 1 or led_index > 6:
            raise ValueError("Invalid LED index: ", led_index)

        self.IO_PIN_ID = self._FIRST_LED_PIN_INDEX + led_index - 1
        super().__init__()

    @property
    def on_value(self) -> int:
        return LED.ON_VALUE

    @property
    def off_value(self) -> int:
        return LED.OFF_VALUE
