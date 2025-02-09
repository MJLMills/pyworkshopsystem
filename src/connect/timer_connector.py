import machine
import micropython


class TimerConnector:
    """Micropython timer for timed event loops."""
    def __init__(self,
                 looper,
                 freq: int,
                 computer=None):

        self._timer = machine.Timer(-1,
                                    freq=freq,
                                    callback=self.callback)
        self._looper = looper
        self._computer = computer

    def callback(self, _):
        """The callback to run on each timed execution."""
        micropython.schedule(self.update, 0)

    def update(self, _):
        """The update method to be scheduled by the callback."""
        self._looper.take_step()
