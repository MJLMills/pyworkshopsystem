import machine
from src.connect.ranged_variable import RangedVariable
from src.connect.signal import Signal


class HardwareComponent(object):
    """An abstract class for a hardware object with an associated GPIO pin.

    All hardware objects (other than the CV/Audio output sockets) have a single
    associated GPIO pin, regardless of whether they use that pin directly or
    through the multiplexer (in which case the GPIO pin may be shared). This
    pin has a unique integer identifier.

    # i'm fairly convinced there's no way to change the ranges on inputs
    # that's because the read will always return a value in the hardware range
    # that then can be mapped elsewhere. If you e.g. set the min to 1000, the read
    # method will still carry on reading whatever is at the pin. You would have to map
    # the hardware reads to another range, which you're going to be doing anyway so
    # it's a waste of time.
    # the min/max values then are a form of calibration if they might differ for
    # each specific workshop system.

    main knob - its ranged variable is the u16 read at the multiplexer, range is fixed by hardware constraints
    x knob - same
    y knob - same
    z switch - same (but really is mapped to one of three states at any given instant)

    CV input (1,2) - same
    CV/Audio input (1,2) - u16 read straight from pin

    # these you may want to control the range of, because to write a limited range you
    # literally have to change the range of the hardware output because the value is computed
    # by mapping whatever input to the output based on that range.
    CV output (1,2) - PWM output
    CV/Audio output (1,2) - SPI/DAC output
    """
    @property
    def pin_id(self) -> int:
        """The unique identifier of the GPIO pin used by this class."""
        raise NotImplementedError(
            self.__class__.__name__ + " does not implement pin_id."
        )

    @property
    def pin(self):
        raise NotImplementedError(
            self.__class__.__name__ + " does not implement pin."
        )

class AnalogOutput(HardwareComponent):
    """A hardware analog output.

    There are four analog outputs on the Computer, each of which is a socket.
    Two are dedicated to CV and are written to using PWM. The other two may be
    used for CV or audio, and are written to through the Computer's DAC.

    See Also
    --------
    CVAudioOutputSocket
        The CV/Audio output sockets of the Computer.
    CVOutputSocket
        The CV output sockets of the Computer.
    """
    def __init__(self):
        self.ranged_variable = RangedVariable(
            value=self.min_value,
            minimum=self.min_value,
            maximum=self.max_value
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

    @property
    def hardware_min(self) -> int:
        raise NotImplementedError(
            self.__class__.__name__ + " does not implement max_value."
        )

    @property
    def hardware_max(self) -> int:
        raise NotImplementedError(
            self.__class__.__name__ + " does not implement max_value."
        )

    def write(self, value):
        raise NotImplementedError(
            self.__class__.__name__ + " does not implement write."
        )


class AnalogInput(HardwareComponent):
    # TODO - is this a ranged variable, or does it have a ranged variable?
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
