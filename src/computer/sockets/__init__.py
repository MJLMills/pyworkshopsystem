from src.computer.sockets.audio.audio_input_socket import AudioInputSocketOne
from src.computer.sockets.audio.audio_input_socket import AudioInputSocketTwo
from src.computer.sockets.cv_audio.cv_audio_output_socket import CVAudioOutputSocketOne
from src.computer.sockets.cv_audio.cv_audio_output_socket import CVAudioOutputSocketTwo
from src.computer.sockets.cv.cv_input_socket import CVInputSocketOne
from src.computer.sockets.cv.cv_input_socket import CVInputSocketTwo
from src.computer.sockets.pulses.pulse_input_socket import PulseInputSocketOne
from src.computer.sockets.pulses.pulse_input_socket import PulseInputSocketTwo


class Socket(object):
    ...

class InputSocket(Socket):
    """An input socket of the Computer."""
    ...

class OutputSocket(Socket):
    """An output socket of the Computer."""
    ...
