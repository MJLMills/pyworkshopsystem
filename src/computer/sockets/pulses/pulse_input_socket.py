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
    __ON_VALUE = 0
    __OFF_VALUE = 1

    def __init__(self):

        self._pin = machine.Pin(self.io_pin_id,
                                machine.Pin.IN,
                                machine.Pin.PULL_UP)

        self.pulse_started = Signal()

        self.jack_inserted = Signal()
        self.jack_removed = Signal()
        self._has_jack = False

        self.irq = self._pin.irq(handler=self.__emit_pulse_started,
                                 trigger=machine.Pin.IRQ_FALLING)

    @property
    def has_jack(self) -> bool:
        return self._has_jack

    @has_jack.setter
    def has_jack(self, has_jack: bool) -> None:
        """Set whether this socket has a jack inserted."""
        had_jack = self._has_jack
        self._has_jack = has_jack

        if has_jack == had_jack:
            return
        elif has_jack and (not had_jack):
            self.jack_inserted.emit()
        elif (not has_jack) and had_jack:
            self.jack_removed.emit()

    def __emit_pulse_started(self, _):
        self.pulse_started.emit()

    def set_irq(self, handler):
        self._pin.irq(handler=handler, trigger=machine.Pin.IRQ_FALLING)

    def read(self):
        return self._pin.value()

    def read_norm_probe(self):
        return self.read()

    def is_high(self):
        return self.read() == self.__ON_VALUE

    def is_low(self):
        return self.read() == self.__OFF_VALUE


class PulseInputSocketOne(PulseInputSocket):
    """The first (leftmost) pulse input socket."""
    __IO_PIN_ID = 2

    @property
    def io_pin_id(self):
        """The unique identifier of the GPIO pin used by this class."""
        return self.__IO_PIN_ID


class PulseInputSocketTwo(PulseInputSocket):
    """The second (rightmost) pulse input socket."""
    __IO_PIN_ID = 3

    @property
    def io_pin_id(self):
        """The unique identifier of the GPIO pin used by this class."""
        return self.__IO_PIN_ID
