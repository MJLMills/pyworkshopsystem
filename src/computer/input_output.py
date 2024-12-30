import machine


class IO(object):
    """An abstract class for a hardware object with an associated GPIO pin.

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
    """An abstract class for an analog input hardware object.

    There are eight analog inputs on the Computer. The main, X and Y knobs,
    the Z-switch and two pairs of CV and CV/Audio inputs. Excepting the
    CV/Audio inputs, all reach the Computer via a multiplexer, so there are in
    total four unique micropython ADC objects attached to GPIO pins with IDs
    26, 27, 28 and 29.
    """
    def __init__(self):
        self._latest_value = None

    @property
    def adc(self) -> machine.ADC:
        raise NotImplementedError(
            self.__class__.__name__ + " does not implement adc."
        )

    def read(self) -> int:
        """Read a 12-bit uint value from the RP2040's ADC.

        The micropython ADC class provides a single read method, which takes an
        analog reading and returns a 16-bit unsigned integer in the range
        0-65535. The return value represents the raw reading taken by the ADC,
        scaled such that the minimum value is 0 and the maximum value is 65535.

        The ADC on the RP2040 is 12-bit, meaning it can distinguish 4096 values
        at the pin. When reading the ADC with micropython, the 4 least
        significant bits of the u16 will not be meaningful.
        There are two alternatives for converting the 16-bit unsigned integers
        from the micropython ADC read_16 method to 12-bit unsigned integers.
        Either can scale (which uses floating point and rounding)
        u12 = int(u16 / 16)
        or shift bits 4 positions to the right, effectively discarding the four
        least significant bits.
        u12 = u16 >> 4
        """
        return self.adc.read_u16() >> 4
        # TODO - how do you calibrate this avoiding remapping with floats?

    def update_latest_value(self):
        """Update the latest value of this analog input."""
        self._latest_value = self.read()

    @property
    def latest_value(self) -> int:
        """The pot value in the range 0, 4095."""
        return self._latest_value
