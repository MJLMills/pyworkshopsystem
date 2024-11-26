import machine


class LEDMatrix(object):
    """
    Abstracts the six LEDs on the panel as a 2x3 (row-major)
    matrix.
    """
    led_1 = machine.Pin(PinId.LED_1, machine.Pin.OUT)
    led_2 = machine.Pin(PinId.LED_2, machine.Pin.OUT)
    led_3 = machine.Pin(PinId.LED_3, machine.Pin.OUT)
    led_4 = machine.Pin(PinId.LED_4, machine.Pin.OUT)
    led_5 = machine.Pin(PinId.LED_5, machine.Pin.OUT)
    led_6 = machine.Pin(PinId.LED_6, machine.Pin.OUT)

    LEDS = (
        (led_1, led_2),
        (led_3, led_4),
        (led_5, led_6)
    )

    def __init__(self, start_value=0):

        if start_value not in {0, 1}:
            start_value = 0

        for led in LEDMatrix.LEDS:
            led.value(start_value)

    @staticmethod
    def get(i, j):
        return LEDMatrix.LEDS[i, j]

    @staticmethod
    def turn_row_on(index):
        if index not in {0, 1, 2}:
            return  # look up what to do with error raising

        for led in LEDMatrix.LEDS[index]:
            led.value(1)

    @staticmethod
    def turn_row_off(index):
        if index not in {0, 1, 2}:
            return  # look up what to do with error raising

        for led in LEDMatrix.LEDS[index]:
            led.value(0)

    @staticmethod
    def turn_column_on(index):
        if index not in {0, 1}:
            return  # look up what to do with error raising

        for row in LEDMatrix.LEDS:
            row[index].value(1)

    @staticmethod
    def turn_column_off(index):
        if index not in {0, 1}:
            return  # look up what to do with error raising

        for row in LEDMatrix.LEDS:
            row[index].value(1)
