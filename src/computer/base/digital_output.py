import machine
from computer.base.hardware_component import SinglePinHardwareComponent


class DigitalOutput(SinglePinHardwareComponent):
    """A hardware digital output.

    Every subclass of this class must implement the following constants:

    IO_PIN_ID (from HardwareComponent):
        The ID of the GPIO pin connected to this digital output hardware component.
    ON_VALUE
        The value (0 or 1) corresponding to the "on" state.
    OFF_VALUE
        The value (0 or 1) corresponding to the "off" state.

    See Also
    --------
    PulseOutputSocket
        An output socket of the computer, sending pulses.
    LED
        A light emitting diode on the module.
    """
    ON_VALUE = None
    """The value (0 or 1) corresponding to the "on" state."""
    OFF_VALUE = None
    """The value (0 or 1) corresponding to the "off" state."""

    def __init__(self):
        super().__init__()
        self._pin = machine.Pin(self._resolve_pin_id(),
                                machine.Pin.OUT)

        self._timer = machine.Timer(-1)

    def _resolve_pin_id(self):
        return self.IO_PIN_ID

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
        self._pin.toggle()

    def pulse(self) -> None:
        """Turn this digital output on for a period, then off."""
        self.turn_on()

        self._timer.init(mode=machine.Timer.ONE_SHOT,
                         period=100,
                         callback=self.turn_off)
