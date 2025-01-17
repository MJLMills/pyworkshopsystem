import machine
from base.hardware_component import HardwareComponent
from src.connect.ranged_variable import RangedVariable
from src.connect.signal import Signal


class AnalogInput(HardwareComponent):
    """An abstract class for an analog input hardware object.

    There are eight analog inputs on the Computer. The main, X and Y knobs,
    the Z-switch and two pairs of CV and CV/Audio inputs. Excepting the
    CV/Audio inputs, all reach the RP2040 via a multiplexer, so there are in
    total four unique micropython ADC objects attached to GPIO pins with IDs
    26, 27, 28 and 29. The GPIO pins with IDs 28 and 29 are connected to the
    multiplexer to provide values from the 6 selectable inputs. The GPIO pins
    with IDs 26 and 27 are directly connected to the CV/Audio inputs. This is
    abstracted away in the two subclasses of AnalogInput; MultiplexedInput and
    CVAudioInputSocket.

    See Also
    --------
    MultiplexedInput
        A multiplexed analog input source.
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
    def __init__(self):

        self.ranged_variable = RangedVariable(
            value=self.min_value,
            minimum=self.min_value,
            maximum=self.max_value
        )
        self.value_changed = Signal()

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
        value = self.ranged_variable.value
        self.ranged_variable.value = self.adc.read_u16()

        if abs(self.ranged_variable.value - value) > 32:
            self.value_changed.emit(ranged_variable=self.ranged_variable)
