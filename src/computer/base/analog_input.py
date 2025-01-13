from base.hardware_component import HardwareComponent
from src.connect.ranged_variable import RangedVariable


class AnalogInput(HardwareComponent):
    """An abstract class for an analog input hardware object.

    There are eight analog inputs on the Computer. The main, X and Y knobs,
    the Z-switch and two pairs of CV and CV/Audio inputs. Excepting the
    CV/Audio inputs, all reach the Computer via a multiplexer, so there are in
    total four unique micropython ADC objects attached to GPIO pins with IDs
    26, 27, 28 and 29. The GPIO pins with IDs 28 and 29 are connected to the
    multiplexer to provide values from the 6 selectable inputs. The GPIO pins
    with IDs 26 and 27 are directly connected to the CV/Audio inputs.

    See Also
    --------
    MainKnob
        The main (big) knob on the Computer module.
    KnobX
        The knob marked X.
    KnobY
        The knob marked Y.
    SwitchZ
        The Z-switch.
    CVInputSocket
        The CV input sockets of the Computer.
    CVAudioInputSocket
        The CV/Audio input sockets of the computer.
    """
    def __init__(self):  # input_value property should be a ranged variable instance - this may be true of every IO object?
        self._latest_value = None
        self.ranged_variable = RangedVariable(
            value=self.min_value,
            minimum=self.min_value,
            maximum=self.max_value
        )
        # self.value_changed = Signal()

    @property
    def adc(self) -> machine.ADC:
        raise NotImplementedError(
            self.__class__.__name__ + " does not implement adc."
        )

    @property
    def min_value(self) -> int:
        raise NotImplementedError(
            self.__class__.__name__ + " does not implement min_value."
        )

    @property
    def max_value(self) -> int:
        raise NotImplementedError(
            self.__class__.__name__ + " does not implement max_value."
        )

    def read(self) -> None:
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
        Neither of these seems strictly necessary on read since the mappings take
        care of converting to the right ranges, and either way python is storing these
        as integers, 12-bit or 16-bit it doesn't care.
        """
        self.ranged_variable.value = self.adc.read_u16()

    # TODO - get rid of this? duplicates value of ranged variable
    def update_latest_value(self):
        """Update the latest value of this analog input."""
        self._latest_value = self.read()
        # for signals and slots, this will emit a signal if the value changes
        # containing the new value and range allowing mapping to outputs
        # value = self.read()
        # if value != self._latest_value:
        #    self._latest_value = value
        #    self.value_changed.emit(self._latest_value)

    @property
    def latest_value(self) -> int:
        """The pot value in the range 0, 4095."""
        return self.ranged_variable.value
