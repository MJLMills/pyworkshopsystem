# want to set an IRQ that turns the LED on when a pulse is received at the input
# this is the challenge, the handler gets attached to the pulse input socket
# but needs access to the LED pin
# see: https://docs.micropython.org/en/latest/reference/isr_rules.html#the-use-of-object-methods-as-callbacks

# the Computer class has references to all the hardware object instances so can construct these, but the callbacks
# would be Computer methods
# subclassing this guy seems to be the best option.
# the output does not have to be hardware - can be some object whose state is to change
class IRQConnector(object):
    """Connect an IRQ source to an output.

    For pins on which an IRQ can be set
    """

    def __init__(self, irq_source, outputs, trigger):
        self._outputs = outputs
        irq_source.pin.irq(handler=self.callback,
                           trigger=trigger)

    def callback(self, irq_source_pin):
        raise NotImplementedError("Connector subclasses must define a callback method.")


class LEDFlasher(IRQConnector):
    """Connect an IRQ source to an output."""

    def callback(self, irq_source_pin):
        """Turn the LED on and off."""
        if self._outputs[0].pin.value():
            self._outputs[0].pin.value(0)
        else:
            self._outputs[0].pin.value(1)

        # the IRQ gets set on the pin instance, need to provide a handler
        # the handler will need to turn the looper on, which implies needing a
        # ref to the looping class which we don't have here.

        # so maybe can provide the IRQ from outside and pass a class method instead?
        # this may be how stuff gets implemented in the actual Computer program in the end
        # if this can just set a bool to be consumed by something in a loop that might help.
        # but then why not just poll the value? - figure this out.
        # see set_irq below:



import machine
from looper import Looper

# TODO - these are technically signals and slots, the IRQ firing is a signal
# and the callback(s) it calls is a slot
# see if these can be made syntactically the same as signal/slots
# e.g. the callback could just emit a signal then the code can register slots
# to that signal
# this code can probably be housed in the DigitalInput classes (pulse inputs)
# since the IRQ is set on the pulse input pin.
# check if a pin can have multiple IRQs

class IRQConnector(object):
    """Connect an IRQ source to an output.

    For pins on which an IRQ can be set, this class can be used to add a
    callback that has access to the necessary program state without defining
    global variables.

    Parameters
    ----------
    irq_source
        The pin on which the IRQ is to be set.
    outputs
        The class instances providing access to program state.
    """
    def __init__(self,
                 irq_source: machine.Pin,
                 outputs: list,
                 trigger):

        self._outputs = outputs
        irq_source.pin.irq(handler=self.callback,
                           trigger=trigger)

    def callback(self, irq_source_pin):
        raise NotImplementedError(
            "Connector subclasses must define a callback method.")


class ToggleLooping(IRQConnector):
    """Connect a pulse input to toggle looping of the system.

    This class sets an IRQ on a provided digital input pin which toggles the
    provided looper on or off (depending on its current state) when the pin
    goes high.

    Parameters
    ----------
    pulse_input
        The pulse input that will toggle looping.
    looper
        The looper whose state will be toggled by the pulse input.
    """

    def __init__(self,
                 pulse_input: machine.Pin,
                 looper: Looper):
        super().__init__(pulse_input,
                         outputs=[looper],
                         trigger=machine.Pin.IRQ_RISING)

        self._looper = self._outputs[0]

    def callback(self, _):
        """Toggle looping when the pulse input goes high."""
        self._looper.toggle_looping()


# if the start point is pinged, tell the looper (set_initial_coordinates)
class SetStartPoint(IRQConnector):
    """Connect a pulse input one to set the start point of a looper.

    This class sets an IRQ on a provided digital input pin which sets the start
    point of the provided looper when the pin goes high.

    Parameters
    ----------
    pulse_input
        The pulse input that will set the start point.
    looper
        The looper whose start point will be set by the pulse input.
    """

    def __init__(self,
                 pulse_input: machine.Pin,
                 looper: Looper,
                 led: LED):
        super().__init__(pulse_input,
                         outputs=[looper, led],
                         trigger=machine.Pin.IRQ_RISING)

        self._looper = self._outputs[0]
        self._led = self._outputs[1]

    def callback(self, irq_source_pin):
        """Set the start point when the pin goes high."""
        self._looper.set_initial_coordinates()
        self._led.pulse(0.001)