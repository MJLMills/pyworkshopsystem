from base.hardware_component import HardwareComponent


class DigitalOutput(HardwareComponent):
    """A hardware digital output.

    See Also
    --------
    PulseOutputSocket
    LED
    """
    def __init__(self):
        super().__init__()
        self._pin = machine.Pin(self.io_pin_id,
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

    def turn_on(self, timer=None):
        self._pin.value(self.on_value)

    def turn_off(self, timer=None):
        self._pin.value(self.off_value)  # may be able to get rid if this can be used as the callback

    def is_on(self):
        return self._pin.value() == self.on_value

    def is_off(self):
        return self._pin.value() == self.off_value

    def toggle(self):
        if self._pin.value == self.ON_VALUE:
            self.turn_off()
        elif self._pin.value == self.OFF_VALUE:
            self.turn_on()

    def pulse(self):
        self.turn_on()

        self._timer.init(mode=machine.Timer.ONE_SHOT,
                         period=500,
                         callback=self.turn_off)
