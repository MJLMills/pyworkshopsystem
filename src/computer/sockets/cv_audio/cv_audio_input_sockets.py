import array
from computer.sockets.cv_audio.cv_audio_input_socket import CVAudioInputSocketOne
from computer.sockets.cv_audio.cv_audio_input_socket import CVAudioInputSocketTwo


class CVAudioInputSockets(object):
    """The pair of audio input sockets."""

    def __init__(self):
        self.socket_one = CVAudioInputSocketOne()
        self.socket_two = CVAudioInputSocketTwo()

    def read(self):
        return (self.socket_one.read_u16(),
                self.socket_two.read_u16())

    def read_range(self, num_samples=1):

        left_values = array.array(typecode="I") * num_samples
        right_values = array.array(typecode="I") * num_samples

        for i in range(0, num_samples):
            left_values[i] = self.socket_one.read_u16()
            right_values[i] = self.socket_two.read_u16()

        return (max(left_values) - min(left_values),
                max(right_values) - min(right_values))

