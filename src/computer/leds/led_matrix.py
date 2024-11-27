import machine
from .led import LED
from enum import Enum


class LEDMatrix(object):
    """The 3x2 LED matrix on the module.

    Abstracts the six LEDs on the panel as a 3x2 (row-major)
    matrix.
    """
    class ColumnIndices(Enum):
        LEFT: 0
        RIGHT: 1

    LEDS = (
        (LED(led_index=1), LED(led_index=2)),
        (LED(led_index=3), LED(led_index=4)),
        (LED(led_index=5), LED(led_index=6))
    )

    def __init__(self, start_value=0):

        if start_value not in {0, 1}:
            start_value = 0

        for led_a, led_b in LEDMatrix.LEDS:
            led_a.value = start_value
            led_b.value = start_value

    @staticmethod
    def turn_on():
        for led_a, led_b in LEDMatrix.LEDS:
            led_a.turn_on()
            led_b.turn_on()

    @staticmethod
    def turn_off():
        for led_a, led_b in LEDMatrix.LEDS:
            led_a.turn_on()
            led_b.turn_on()

    @staticmethod
    def get(row_index, col_index):
        return LEDMatrix.LEDS[row_index][col_index]

    @staticmethod
    def turn_row_on(row_index):
        if row_index not in {0, 1, 2}:
            raise ValueError("Invalid LED row index: ", row_index)

        for led in LEDMatrix.LEDS[row_index]:
            led.value = 1

    @staticmethod
    def turn_row_off(row_index):
        if row_index not in {0, 1, 2}:
            raise ValueError("Invalid LED row index: ", row_index)

        for led in LEDMatrix.LEDS[row_index]:
            led.value = 0

    @staticmethod
    def turn_column_on(col_index, num_leds):
        if col_index not in {0, 1}:
            raise ValueError("Invalid LED column index: ", col_index)

        for row in LEDMatrix.LEDS[0:num_leds]:
            row[col_index].value = 1

    @staticmethod
    def turn_left_column_on(num_leds):
        LEDMatrix.turn_column_on(LEDMatrix.ColumnIndices["LEFT"], num_leds)

    @staticmethod
    def turn_right_column_on(num_leds):
        LEDMatrix.turn_column_on(LEDMatrix.ColumnIndices["RIGHT"], num_leds)

    @staticmethod
    def turn_column_off(col_index):
        if col_index not in {0, 1}:
            raise ValueError("Invalid LED column index: ", col_index)

        for row in LEDMatrix.LEDS:
            row[col_index].value = 1
