class HardwareComponent(object):
    pass

class SinglePinHardwareComponent(HardwareComponent):
    """An abstract class for a hardware object with an associated GPIO pin.

    All subclasses must implement the following constants:
    IO_PIN_ID:
        The ID of the GPIO pin connected to this hardware component.
    """
    IO_PIN_ID = None

    def __str__(self):
        return f"{self.__class__.__name__} on pin {self.IO_PIN_ID}"
