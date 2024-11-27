import array
from .cv_audio_input_socket import CVAudioInputSocketOne
from .cv_audio_input_socket import CVAudioInputSocketTwo


class CVAudioInputSockets(object):
    """The pair of audio input sockets."""

    def __init__(self):
        self.socket_one = CVAudioInputSocketOne()
        self.socket_two = CVAudioInputSocketTwo()

    def read(self):
        return (self.socket_one.read(),
                self.socket_two.read())

    def read_range(self, n=1):

        left_values = array.array(typecode="I") * n
        right_values = array.array(typecode="I") * n

        for i in range(0, n):
            left_values[i] = self.socket_one.read()
            right_values[i] = self.socket_two.read()

        return (max(left_values) - min(left_values),
                max(right_values) - min(right_values))

