import machine


class LED(object):
    """
    LEDs are driven through an NPN transistor array from the +12V rail.
    1/true = LED is illuminated.
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
