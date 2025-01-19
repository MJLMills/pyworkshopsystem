import machine
import random


class NormalizationProbe(object):
    """The normalization probe.

    The normalization probe is a digital output connected to GPIO pin 4. When
    nothing is plugged into each input socket (pulse inputs one and two, CV
    inputs one and two, CV/Audio inputs one and two), they are connected to
    the normalization probe and will have the values written there. By writing
    a known pattern of digital values to the sockets and checking their read
    values, it is possible to determine whether each socket is connected to the
    normalization probe, and therefore whether a jack is plugged into its
    socket.
    A pseudorandom sequence of bits is generated on each instantiation. The
    length of this sequence is hard-coded; the longer the sequence the lower
    the possibility of coincidentally receiving it as a genuine input.
    """
    __IO_PIN_ID = 4
    __N_BITS = 4

    def __init__(self):
        self._pin = machine.Pin(self.__IO_PIN_ID,
                                machine.Pin.OUT)

        self.pattern = random.getrandbits(self.__N_BITS)
        self.index = 0
        self.n_bits = self.__N_BITS

    def write(self):
        """Write the next bit of the pattern to pin 4."""
        self._pin.value((self.pattern >> self.index) & 1)

        if self.index == self.__N_BITS - 1:
            self.index = 0
        else:
            self.index += 1

        return self._pin.value()

