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