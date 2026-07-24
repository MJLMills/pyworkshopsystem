from micropython import const
from computer.base.digital_output import DigitalOutput


class LED(DigitalOutput):
    """A light emitting diode on the module.

    If the pin value is set to 1 (i.e. True), the LED is illuminated.
    The LED pins start at 10 and end at 15. Boundary checks and pin ID
    calculations use hardcoded values.

    Parameters
    ----------
    led_index: int
        The index (1 to 6) of the LED.

    """
    ON_VALUE = const(1)
    OFF_VALUE = const(0)

    def __init__(self, led_index):
        if not 1 <= led_index <= 6:
            raise ValueError(f"Invalid LED index: {led_index}")

        self.__io_pin_id = 9 + led_index
        super().__init__()

    def _resolve_pin_id(self) -> int:
        return self.__io_pin_id