import machine
from computer.leds.led import LED


class LEDMatrix(object):
    """The 3x2 LED matrix on the module.

    Abstracts the six LEDs on the panel as a 3x2 (row-major)
    matrix.
    """
    # row indices
    TOP = 0
    MIDDLE = 1
    BOTTOM = 2

    # column indices
    LEFT = 0
    RIGHT = 1

    LEDS = (
        (LED(led_index=1), LED(led_index=2)),
        (LED(led_index=3), LED(led_index=4)),
        (LED(led_index=5), LED(led_index=6))
    )

    # Map index to (row, col) - tuple for fast lookup, None at index 0 to align with 1-based indexing
    _INDEX_MAP = (
        None,
        (0, 0), (0, 1),
        (1, 0), (1, 1),
        (2, 0), (2, 1)
    )
    """Fast conversion from running index (1-6) to matrix subscripts."""

    def __init__(self, start_value=0):

        if start_value not in {0, 1}:
            start_value = 0

        for led_a, led_b in LEDMatrix.LEDS:
            led_a.value = start_value
            led_b.value = start_value

    @staticmethod
    def turn_on(index: int = None):
        if index:
            row_index, col_index = LEDMatrix._INDEX_MAP[index]
            LEDMatrix.LEDS[row_index][col_index].turn_on()
        else:
            for led_a, led_b in LEDMatrix.LEDS:
                led_a.turn_on()
                led_b.turn_on()

    @staticmethod
    def turn_off(index: int = None):
        if index:
            row_index, col_index = LEDMatrix._INDEX_MAP[index]
            LEDMatrix.LEDS[row_index][col_index].turn_off()
        else:
            for led_a, led_b in LEDMatrix.LEDS:
                led_a.turn_off()
                led_b.turn_off()

    @staticmethod
    def get(row_index, col_index):
        return LEDMatrix.LEDS[row_index][col_index]

    @staticmethod
    def get_by_index(index):
        row_index, col_index = LEDMatrix._INDEX_MAP[index]
        return LEDMatrix.LEDS[row_index][col_index]

    @staticmethod
    def turn_row_on(row_index, num_leds=2):
        if row_index not in {0, 1, 2}:
            raise ValueError("Invalid LED row index: ", row_index)

        row = LEDMatrix.LEDS[row_index]
        for i in range(num_leds):
            row[i].value = 1

    @staticmethod
    def turn_top_row_on(num_leds=2):
        LEDMatrix.turn_row_on(LEDMatrix.TOP, num_leds)

    @staticmethod
    def turn_middle_row_on(num_leds=2):
        LEDMatrix.turn_row_on(LEDMatrix.MIDDLE, num_leds)

    @staticmethod
    def turn_bottom_row_on(num_leds=2):
        LEDMatrix.turn_row_on(LEDMatrix.BOTTOM, num_leds)

    @staticmethod
    def turn_row_off(row_index, num_leds=2):
        if row_index not in {0, 1, 2}:
            raise ValueError("Invalid LED row index: ", row_index)

        row = LEDMatrix.LEDS[row_index]
        for i in range(num_leds):
            row[i].value = 0

    @staticmethod
    def turn_top_row_off(num_leds=2):
        LEDMatrix.turn_row_off(LEDMatrix.TOP, num_leds)

    @staticmethod
    def turn_middle_row_off(num_leds=2):
        LEDMatrix.turn_row_off(LEDMatrix.MIDDLE, num_leds)

    @staticmethod
    def turn_bottom_row_off(num_leds=2):
        LEDMatrix.turn_row_off(LEDMatrix.BOTTOM, num_leds)

    @staticmethod
    def turn_column_on(col_index, num_leds=3):
        if col_index not in {0, 1}:
            raise ValueError("Invalid LED column index: ", col_index)

        for i in range(num_leds):
            LEDMatrix.LEDS[i][col_index].value = 1

    @staticmethod
    def turn_left_column_on(num_leds=3):
        LEDMatrix.turn_column_on(LEDMatrix.LEFT, num_leds)

    @staticmethod
    def turn_right_column_on(num_leds=3):
        LEDMatrix.turn_column_on(LEDMatrix.RIGHT, num_leds)

    @staticmethod
    def turn_column_off(col_index, num_leds=3):
        if col_index not in {0, 1}:
            raise ValueError("Invalid LED column index: ", col_index)

        for i in range(num_leds):
            LEDMatrix.LEDS[i][col_index].value = 0

    @staticmethod
    def turn_left_column_off(num_leds=3):
        LEDMatrix.turn_column_off(LEDMatrix.LEFT, num_leds)

    @staticmethod
    def turn_right_column_off(num_leds=3):
        LEDMatrix.turn_column_off(LEDMatrix.RIGHT, num_leds)
