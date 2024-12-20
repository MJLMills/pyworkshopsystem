import machine


class LED(object):
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

    FIRST_LED_PIN_INDEX = 9

    def __init__(self, led_index):
        if led_index not in range(1, 6):
            raise ValueError("Invalid LED index: ", led_index)

        self.pin = machine.Pin(self.FIRST_LED_PIN_INDEX + led_index,
                               machine.Pin.OUT)

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