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
