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
