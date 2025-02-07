class HardwareComponent(object):
    """An abstract class for a hardware object with an associated GPIO pin."""

    @property
    def io_pin_id(self) -> int:
        """The unique identifier of the GPIO pin used by this class."""
        raise NotImplementedError(
            self.__class__.__name__ + " does not implement io_pin_id."
        )

    def __str__(self):
        return f"{self.__class__.__name__} on pin {self.io_pin_id}"
