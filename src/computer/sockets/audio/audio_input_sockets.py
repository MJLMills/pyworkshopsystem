import array
from .audio_input_socket import AudioInputSocketOne
from .audio_input_socket import AudioInputSocketTwo


class AudioInputSockets(object):
    """The pair of audio input sockets."""

    def __init__(self):
        self.socket_one = AudioInputSocketOne()
        self.socket_two = AudioInputSocketTwo()

    def read(self):
        return (self.socket_one.read(),
                self.socket_two.read())

    def read_n(self, n):

        left_values = array.array(typecode="I") * n
        right_values = array.array(typecode="I") * n

        for i in range(0, n):
            left_values[i] = self.socket_one.read()
            right_values[i] = self.socket_two.read()

        return (max(left_values) - min(left_values),
                max(right_values) - min(right_values))

