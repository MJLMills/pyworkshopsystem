import machine


# TODO - replace the pins in this with LED instances
class LEDMatrix(object):
    """
    Abstracts the six LEDs on the panel as a 2x3 (row-major)
    matrix.
    """
    led_pin_1 = machine.Pin(10, machine.Pin.OUT)
    led_pin_2 = machine.Pin(11, machine.Pin.OUT)
    led_pin_3 = machine.Pin(12, machine.Pin.OUT)
    led_pin_4 = machine.Pin(13, machine.Pin.OUT)
    led_pin_5 = machine.Pin(14, machine.Pin.OUT)
    led_pin_6 = machine.Pin(15, machine.Pin.OUT)

    LED_PINS = (
        (led_pin_1, led_pin_2),
        (led_pin_3, led_pin_4),
        (led_pin_5, led_pin_6)
    )

    def __init__(self, start_value=0):

        if start_value not in {0, 1}:
            start_value = 0

        for led_pin in LEDMatrix.LED_PINS:
            led_pin.value(start_value)

    @staticmethod
    def get(i, j):
        return LEDMatrix.LED_PINS[i, j]

    @staticmethod
    def turn_row_on(index):
        if index not in {0, 1, 2}:
            return  # look up what to do with error raising

        for led in LEDMatrix.LED_PINS[index]:
            led.value(1)

    @staticmethod
    def turn_row_off(index):
        if index not in {0, 1, 2}:
            return  # look up what to do with error raising

        for led in LEDMatrix.LED_PINS[index]:
            led.value(0)

    @staticmethod
    def turn_column_on(index):
        if index not in {0, 1}:
            return  # look up what to do with error raising

        for row in LEDMatrix.LED_PINS:
            row[index].value(1)

    @staticmethod
    def turn_column_off(index):
        if index not in {0, 1}:
            return  # look up what to do with error raising

        for row in LEDMatrix.LED_PINS:
            row[index].value(1)
