import machine


class IO(object):
    """A hardware object with an associated GPIO pin.

    All hardware objects (other than the CV/Audio output sockets) have a single
    associated GPIO pin, regardless of whether they use that pin directly or
    through the multiplexer (in which case the GPIO pin may be shared). This
    pin has a unique integer identifier.
    """
    @property
    def pin_id(self) -> int:
        """The unique identifier of the GPIO pin used by this class."""
        raise NotImplementedError(
            self.__class__.__name__ + " does not implement pin_id."
        )

class AnalogInput(IO):
    """An analog input hardware object.

    There are eight analog inputs on the Computer. The main, X and Y knobs,
    the Z-switch and two pairs of CV and CV/Audio inputs. Excepting the
    CV/Audio inputs, all reach the Computer via a multiplexer, so there are in
    total four unique micropython ADC objects attached to GPIO pins with IDs
    26, 27, 28 and 29.
    """
    @property
    def adc(self) -> machine.ADC:
        raise NotImplementedError(
            self.__class__.__name__ + " does not implement adc."
        )

    def read(self) -> int:
        """Read the value of this analog input."""
        return self.adc.read_u16()
