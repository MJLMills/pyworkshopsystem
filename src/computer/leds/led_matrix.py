from micropython import const
from computer.leds.led import LED


class LEDMatrix(object):
    """The 3x2 LED matrix on the module.

    Abstracts the six LEDs on the panel as a 3x2 (row-major) matrix.
    """
    # row indices
    TOP: int = const(0)
    MIDDLE: int = const(1)
    BOTTOM: int = const(2)

    # column indices
    LEFT: int = const(0)
    RIGHT: int = const(1)

    _INDEX_MAP = (
        None,
        (0, 0), (0, 1),
        (1, 0), (1, 1),
        (2, 0), (2, 1)
    )
    """Fast conversion from running index (1-6) to matrix subscripts."""

    def __init__(self, start_value=0, table_size=512):
        if start_value not in {0, 1}:
            start_value = 0

        self.flat_leds = (
            LED(led_index=1, table_size=table_size),
            LED(led_index=2, table_size=table_size),  # Top row
            LED(led_index=3, table_size=table_size),
            LED(led_index=4, table_size=table_size),  # Middle row
            LED(led_index=5, table_size=table_size),
            LED(led_index=6, table_size=table_size)  # Bottom row
        )

        self.use_digital_mode()

        # Zero-overhead internal iteration
        for led in self.flat_leds:
            if start_value:
                led.turn_on()
            else:
                led.turn_off()

    def use_digital_mode(self) -> None:
        """Pivots all 6 LEDs into Digital Mode simultaneously with zero loop nesting."""
        for led in self.flat_leds:
            led.use_digital_mode()

    def use_pwm_mode(self) -> None:
        """Pivots all 6 LEDs into PWM Mode simultaneously with zero loop nesting."""
        for led in self.flat_leds:
            led.use_pwm_mode()

    def set_matrix_brightness(self, value: int) -> None:
        """Sets the perceived brightness of the entire panel uniformly (0 to 65535).

        Parameters
        ----------
        value : int
            A value between 0 (minimum) and 65535 (maximum) for the matrix brightness.
        """
        for led in self.flat_leds:
            led.set_brightness(value)

    def toggle(self) -> None:
        """Toggle the value of all digital outputs across the matrix."""
        for led in self.flat_leds:
            led.toggle()

    def turn_on(self, index: int = None) -> None:
        """Turn the specified digital output on, or the entire matrix if no index provided."""
        if index:
            # Mathematical conversion: 1D index mapping directly
            # LED 1-6 maps to array offset 0-5
            self.flat_leds[index - 1].turn_on()
        else:
            for led in self.flat_leds:
                led.turn_on()

    def turn_off(self, index: int = None) -> None:
        """Turn the specified digital output off, or the entire matrix if no index provided."""
        if index:
            self.flat_leds[index - 1].turn_off()
        else:
            for led in self.flat_leds:
                led.turn_off()

    def get(self, row_index: int, col_index: int) -> LED:
        """Retrieve the LED instance at the specific row and column subscripts.

        Preserves the legacy 2D matrix API interface seamlessly.
        """
        # Linear offset formula: (row * row_width) + col
        return self.flat_leds[(row_index * 2) + col_index]

    def get_by_index(self, index: int) -> LED:
        """Retrieve the LED instance using its physical running index (1 to 6)."""
        return self.flat_leds[index - 1]

    def turn_row_on(self, row_index: int, num_leds: int = 2) -> None:
        if row_index not in {0, 1, 2}:
            raise ValueError("Invalid LED row index: ", row_index)

        # Calculate the direct flat index slice boundary for the requested row
        start_idx = row_index * 2
        for i in range(num_leds):
            self.flat_leds[start_idx + i].turn_on()

    def turn_top_row_on(self, num_leds: int = 2) -> None:
        self.turn_row_on(self.TOP, num_leds)

    def turn_middle_row_on(self, num_leds: int = 2) -> None:
        self.turn_row_on(self.MIDDLE, num_leds)

    def turn_bottom_row_on(self, num_leds: int = 2) -> None:
        self.turn_row_on(self.BOTTOM, num_leds)

    def turn_row_off(self, row_index: int, num_leds: int = 2) -> None:
        if row_index not in {0, 1, 2}:
            raise ValueError("Invalid LED row index: ", row_index)

        start_idx = row_index * 2
        for i in range(num_leds):
            self.flat_leds[start_idx + i].turn_off()

    def turn_top_row_off(self, num_leds: int = 2) -> None:
        self.turn_row_off(self.TOP, num_leds)

    def turn_middle_row_off(self, num_leds: int = 2) -> None:
        self.turn_row_off(self.MIDDLE, num_leds)

    def turn_bottom_row_off(self, num_leds: int = 2) -> None:
        self.turn_row_off(self.BOTTOM, num_leds)

    def turn_column_on(self, col_index: int, num_leds: int = 3) -> None:
        if col_index not in {0, 1}:
            raise ValueError("Invalid LED column index: ", col_index)

        for i in range(num_leds):
            # Column elements are offset by 2 spaces vertically in a flat array
            self.flat_leds[(i * 2) + col_index].turn_on()

    def turn_left_column_on(self, num_leds: int = 3) -> None:
        self.turn_column_on(self.LEFT, num_leds)

    def turn_right_column_on(self, num_leds: int = 3) -> None:
        self.turn_column_on(self.RIGHT, num_leds)

    def turn_column_off(self, col_index: int, num_leds: int = 3) -> None:
        if col_index not in {0, 1}:
            raise ValueError("Invalid LED column index: ", col_index)

        for i in range(num_leds):
            self.flat_leds[(i * 2) + col_index].turn_off()

    def turn_left_column_off(self, num_leds: int = 3) -> None:
        self.turn_column_off(self.LEFT, num_leds)

    def turn_right_column_off(self, num_leds: int = 3) -> None:
        self.turn_column_off(self.RIGHT, num_leds)
