import machine
from multiplexed_source import MultiplexedSource


class KnobX(MultiplexedSource):

    def __init__(self, multiplexer):
        self.__multiplexer = multiplexer

    def read(self):
        self.__multiplexer.set_logic_pin_values(self.mux_logic_a_pin_value,
                                                self.mux_logic_b_pin_value)

        return machine.ADC(self.__multiplexer.MUX_IO_PIN_ONE_ID).read_u16()

    @property
    def mux_logic_a_pin_value(self):
        return 0

    @property
    def mux_logic_b_pin_value(self):
        return 1

    @property
    def mux_io_pin_id(self):
        return 28
