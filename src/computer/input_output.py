class IO(object):
    """An object with an associated GPIO pin.

    All hardware objects have a single associated GPIO pin,
    regardless of whether they use that pin directly or through
    the multiplexer (in which case the GPIO pin may be shared).
    """
    @property
    def pin_id(self):
        raise NotImplementedError