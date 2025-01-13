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
        self._pin = machine.Pin(self.pin_id,
                                machine.Pin.OUT)

    @property
    def pin_id(self) -> int:
        """The unique identifier of the GPIO pin used by this class."""
        raise NotImplementedError
