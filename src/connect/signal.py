class Signal(object):
    """A signal emitted by an object instance."""
    def __init__(self):
        self._slots = []

    def connect(self, *slots):
        """Connect the specified slots to this signal.

        Parameters
        ----------
        slots : list of callable
            The callable slots to connect to this signal.
        """
        for slot in slots:
            if slot not in self._slots:
                self._slots.append(slot)

    def disconnect(self, *slots):
        """Disconnect the specified slots from this signal.

        Parameters
        ----------
        slots : list of callable
            The callable slots to disconnect from this signal.
        """
        for slot in slots:
            if slot in self._slots:
                self._slots.pop(self._slots.index(slot))

    def emit(self, **kwargs) -> None:
        """Call each slot connected to this signal."""
        for slot in self._slots:
            slot(**kwargs)

    def __str__(self) -> str:
        """Create a human-readable representation of this object."""
        str_rep = self.__class__.__name__ + ", slots = ["
        for slot in self._slots:
            str_rep += str(slot) + ", "

        return str_rep[:-2]
