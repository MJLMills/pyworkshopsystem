import array
from computer.sockets.cv_audio.cv_audio_output_socket import CVAudioOutputSocketOne
from computer.sockets.cv_audio.cv_audio_output_socket import CVAudioOutputSocketTwo


class CVAudioOutputSockets(object):
    """The pair of audio output sockets."""

    def __init__(self):
        self.socket_one = CVAudioOutputSocketOne()
        self.socket_two = CVAudioOutputSocketTwo()
