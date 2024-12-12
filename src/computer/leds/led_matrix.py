import machine
from .led import LED


class LEDMatrix(object):
    """The 3x2 LED matrix on the module.

    Abstracts the six LEDs on the panel as a 3x2 (row-major)
    matrix.
    """
    column_indices = {"LEFT": 0, "RIGHT": 1}
    row_indices = {"TOP": 0, "MIDDLE": 1, "BOTTOM": 2}

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
            led_a.turn_off()
            led_b.turn_off()

    @staticmethod
    def get(row_index, col_index):
        return LEDMatrix.LEDS[row_index][col_index]

    @staticmethod
    def turn_row_on(row_index, num_leds=2):
        if row_index not in {0, 1, 2}:
            raise ValueError("Invalid LED row index: ", row_index)

        for led in LEDMatrix.LEDS[row_index][0:num_leds]:
            led.value = 1

    @staticmethod
    def turn_top_row_on(num_leds=2):
        LEDMatrix.turn_row_on(LEDMatrix.row_indices["TOP"], num_leds)

    @staticmethod
    def turn_middle_row_on(num_leds=2):
        LEDMatrix.turn_row_on(LEDMatrix.row_indices["MIDDLE"], num_leds)

    @staticmethod
    def turn_bottom_row_on(num_leds=2):
        LEDMatrix.turn_row_on(LEDMatrix.row_indices["BOTTOM"], num_leds)

    @staticmethod
    def turn_row_off(row_index, num_leds=2):
        if row_index not in {0, 1, 2}:
            raise ValueError("Invalid LED row index: ", row_index)

        for led in LEDMatrix.LEDS[row_index][0:num_leds]:
            led.value = 0

    @staticmethod
    def turn_top_row_off(num_leds=2):
        LEDMatrix.turn_row_off(LEDMatrix.row_indices["TOP"], num_leds)

    @staticmethod
    def turn_middle_row_off(num_leds=2):
        LEDMatrix.turn_row_off(LEDMatrix.row_indices["MIDDLE"], num_leds)

    @staticmethod
    def turn_bottom_row_off(num_leds=2):
        LEDMatrix.turn_row_off(LEDMatrix.row_indices["BOTTOM"], num_leds)

    @staticmethod
    def turn_column_on(col_index, num_leds=3):
        if col_index not in {0, 1}:
            raise ValueError("Invalid LED column index: ", col_index)

        for row in LEDMatrix.LEDS[0:num_leds]:
            row[col_index].value = 1

    @staticmethod
    def turn_left_column_on(num_leds=3):
        LEDMatrix.turn_column_on(LEDMatrix.column_indices["LEFT"], num_leds)

    @staticmethod
    def turn_right_column_on(num_leds=3):
        LEDMatrix.turn_column_on(LEDMatrix.column_indices["RIGHT"], num_leds)

    @staticmethod
    def turn_column_off(col_index, num_leds=3):
        if col_index not in {0, 1}:
            raise ValueError("Invalid LED column index: ", col_index)

        for row in LEDMatrix.LEDS[0:num_leds]:
            row[col_index].value = 0

    @staticmethod
    def turn_left_column_off(num_leds=3):
        LEDMatrix.turn_column_off(LEDMatrix.column_indices["LEFT"], num_leds)

    @staticmethod
    def turn_right_column_off(num_leds=3):
        LEDMatrix.turn_column_off(LEDMatrix.column_indices["RIGHT"], num_leds)
