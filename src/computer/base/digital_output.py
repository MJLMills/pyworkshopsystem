import machine
from computer.base.hardware_component import HardwareComponent


class DigitalOutput(HardwareComponent):
    """A hardware digital output.

    Subclasses must implement two constants: ON_VALUE and OFF_VALUE.

    See Also
    --------
    PulseOutputSocket
        An output socket of the computer, sending pulses.
    LED
        A light emitting diode on the module.
    """
    ON_VALUE = None
    OFF_VALUE = None

    def __init__(self):
        super().__init__()
        self._pin = machine.Pin(self.IO_PIN_ID,
                                machine.Pin.OUT)

        self._timer = machine.Timer(-1)

    @property
    def on_value(self) -> int:
        """The value used to represent "on" for this digital output."""
        raise NotImplementedError(
            self.__class__.__name__ + " does not implement on_value."
        )

    @property
    def off_value(self) -> int:
        """The value used to represent "off" for this digital output."""
        raise NotImplementedError(
            self.__class__.__name__ + " does not implement off_value."
        )

    def turn_on(self, timer=None) -> None:
        """Turn this digital output on."""
        self._pin.value(self.ON_VALUE)

    def turn_off(self, timer=None) -> None:
        """Turn this digital output off."""
        self._pin.value(self.OFF_VALUE)

    def is_on(self) -> bool:
        """Determine whether this digital output is turned on."""
        return self._pin.value() == self.ON_VALUE

    def is_off(self) -> bool:
        """Determine whether this digital output is turned off."""
        return self._pin.value() == self.OFF_VALUE

    def toggle(self) -> None:
        """Toggle the value of this digital output."""
        if self._pin.value == self.ON_VALUE:
            self.turn_off()
        elif self._pin.value == self.OFF_VALUE:
            self.turn_on()

    def pulse(self) -> None:
        """Turn this digital output on for a period, then off."""
        self.turn_on()

        self._timer.init(mode=machine.Timer.ONE_SHOT,
                         period=100,
                         callback=self.turn_off)
