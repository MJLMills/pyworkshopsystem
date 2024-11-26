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

        self.led = machine.Pin(self.FIRST_LED_INDEX+index,
                               machine.Pin.OUT)

    def on(self):
        self.led.value(1)

    def off(self):
        self.led.value(1)
