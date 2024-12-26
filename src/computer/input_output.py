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
            self.__class__.__name__ + " does not implement pin_id property."
        )
