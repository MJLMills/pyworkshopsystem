import machine


class LED(object):
    """
    LEDs are driven through an NPN transistor array from the +12V rail.
    1/true = LED is illuminated.
    """

    FIRST_LED_INDEX = 9

    def __init__(self, index):
        if index not in range(1, 6):
            raise ValueError()

        self.led_pin = machine.Pin(self.FIRST_LED_INDEX + index,
                                   machine.Pin.OUT)

    @property
    def pin(self):
        return self.led_pin

    def turn_on(self):
        self.led_pin.value(1)

    def turn_off(self):
        self.led_pin.value(0)
