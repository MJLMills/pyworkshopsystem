class HardwareComponent(object):
    """An abstract class for a hardware object with an associated GPIO pin."""
    IO_PIN_ID = None

    def __str__(self):
        return f"{self.__class__.__name__} on pin {self.IO_PIN_ID}"
