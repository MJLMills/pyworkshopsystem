import math
import machine
from micropython import const
from computer.base.digital_output import DigitalOutput


class LED(DigitalOutput):
    """A light emitting diode on the module with shared integer gamma correction.

    Parameters
    ----------
    led_index: int
        The index of the LED on the module (1 to 6).
    table_size: int
        The number of entries in the gamma-corrected brightness table.
        The choice of this value is a tradeoff between fidelity and RAM usage.
    init_pwm: bool
        Whether to initialize the pin in PWM mode for controllable brightness.
        By default the pin is initialized in digital mode.
    """
    ON_VALUE = const(1)
    OFF_VALUE = const(0)
    MIN_BRIGHTNESS = const(0)
    MAX_BRIGHTNESS = const(65535)

    _gamma_table = None
    _table_shift_bits = 0

    def __init__(self, led_index: int, table_size: int = 512, init_pwm: bool = False):
        if not 1 <= led_index <= 6:
            raise ValueError(f"Invalid LED index: {led_index}")

        if (table_size & (table_size - 1)) != 0 or table_size < 2:
            raise ValueError("table_size must be a power of 2 (e.g., 256, 512, 1024)")

        self.__io_pin_id = 9 + led_index
        super().__init__()  # Always defaults to digital first via parent class

        self.__pwm = None

        if LED._gamma_table is None:
            LED._initialize_shared_table(table_size)

        # If requested, instantly pivot the hardware into PWM mode at boot
        if init_pwm:
            self.use_pwm_mode()

    @classmethod
    def _initialize_shared_table(cls, table_size: int):
        """Generates the static integer gamma table shared by all LEDs.

        The gamma table contains values mapping 16-bit integers to gamma-corrected
        16-bit integers for setting LED brightness. The table shift bits stores
        the bit shift required to map the input values (0-65535) to the range (0, table_size-1).

        Parameters
        ----------
        table_size : int
            The number of entries in the gamma-corrected brightness table.
        """
        cls._gamma_table = [
            int(math.pow(i / (table_size - 1), 2.2) * 65535)
            for i in range(table_size)
        ]
        cls._table_shift_bits = 16 - int(math.log2(table_size))

    def _resolve_pin_id(self) -> int:
        return self.__io_pin_id

    def use_digital_mode(self) -> None:
        """Configures the pin back to standard digital. Safe to call repeatedly."""
        if self.__pwm is not None:
            self.__pwm.deinit()
            self.__pwm = None
            self._pin.init(mode=machine.Pin.OUT)

    def use_pwm_mode(self) -> None:
        """Configures the pin for PWM. Safe to call repeatedly."""
        if self.__pwm is None:
            self.__pwm = machine.PWM(self._pin, freq=1000)

    def set_brightness(self, value: int):
        """Set the perceived LED brightness from 0 (off) to 65535 (full on).

        Parameters
        ----------
        value : int
            A value between 0 (minimum) and 65535 (maximum) for the LED brightness.
            This value is clamped within the specified range and then downsampled
            to match the size of the precomputed gamma table.
        """
        # Removed the broken internal method call. If use_pwm_mode() was not called,
        # MicroPython natively raises an AttributeError here on self.__pwm.
        clamped = max(self.MIN_BRIGHTNESS, min(value, self.MAX_BRIGHTNESS))
        table_index = clamped >> self._table_shift_bits
        self.__pwm.duty_u16(self._gamma_table[table_index])
