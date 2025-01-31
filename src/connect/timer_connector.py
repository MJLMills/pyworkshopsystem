import machine
import micropython


class TimerConnector:

    def __init__(self,
                 looper,
                 freq,
                 computer=None):
        self._timer = machine.Timer(-1,
                                    freq=freq,
                                    callback=self.callback)
        self._looper = looper
        self._computer = computer

    def callback(self, _):
        # computer.cv_audio_input_socket_one.read()
        # computer.cv_audio_input_socket_two.read()

        micropython.schedule(self.update, 0)

    def update(self, _):
        self._looper.take_step()