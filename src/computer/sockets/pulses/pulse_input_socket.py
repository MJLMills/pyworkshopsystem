import machine
from base.hardware_component import HardwareComponent
from src.connect.signal import Signal


class PulseInputSocket(HardwareComponent):
    """
    Inverted digital input: Low input = High reading.
    For example, use a falling edge to track the start of a pulse.
    NB: Input pin must have the pull-up enabled, this powers the transistor.

    The gates are about 5-6v
    """
    def __init__(self):

        self._pin = machine.Pin(self.io_pin_id,
                                machine.Pin.IN,
                                machine.Pin.PULL_UP)

        self.pulse_started = Signal()

        self.irq = self._pin.irq(handler=self.__emit_pulse_started,
                                 trigger=machine.Pin.IRQ_FALLING)

    def __emit_pulse_started(self, _):
        self.pulse_started.emit()

    @property
    def pin(self):
        return self._pin

    def set_irq(self, handler):
        self._pin.irq(handler=handler, trigger=machine.Pin.IRQ_FALLING)

    def read(self):
        return self._pin.value()

    def is_high(self):
        return self.read() == 0

    def is_low(self):
        return self.read() == 1


class PulseInputSocketOne(PulseInputSocket):
    """The first (leftmost) pulse input socket."""

    @property
    def io_pin_id(self):
        """The unique identifier of the GPIO pin used by this class."""
        return 2


class PulseInputSocketTwo(PulseInputSocket):
    """The second (rightmost) pulse input socket."""

    @property
    def io_pin_id(self):
        """The unique identifier of the GPIO pin used by this class."""
        return 3
