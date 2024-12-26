# want to set an IRQ that turns the LED on when a pulse is received at the input
# this is the challenge, the handler gets attached to the pulse input socket
# but needs access to the LED pin
# see: https://docs.micropython.org/en/latest/reference/isr_rules.html#the-use-of-object-methods-as-callbacks

# the Computer class has references to all the hardware object instances so can construct these, but the callbacks
# would be Computer methods
# subclassing this guy seems to be the best option.
# the output does not have to be hardware - can be some object whose state is to change
class IRQConnector(object):
    """Connect an IRQ source to an output."""

    def __init__(self, irq_source, output, trigger):
        self.output = output
        irq_source.pin.irq(handler=self.callback,
                           trigger=trigger)

    def callback(self, irq_source_pin):
        raise NotImplementedError("Connector subclasses must define a callback method.")


class LEDFlasher(IRQConnector):
    """Connect an IRQ source to an output."""

    def callback(self, irq_source_pin):
        """Turn the LED on and off."""
        if self.output.pin.value():
            self.output.pin.value(0)
        else:
            self.output.pin.value(1)