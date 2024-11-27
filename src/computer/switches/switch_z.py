import machine
from multiplexed_source import MultiplexedSource


class SwitchZ(MultiplexedSource):

    def __init__(self, multiplexer):
        self.__multiplexer = multiplexer
        self.__adc = machine.ADC(self.__multiplexer.MUX_IO_PIN_ONE_ID)

    def read(self):
        self.__multiplexer.set_logic_pin_values(self.mux_logic_a_pin_value,
                                                self.mux_logic_b_pin_value)

        return self.__adc.read_u16()

    def is_on(self):
        return self.read() == 1

    def is_off(self):
        return not self.is_on()

    @property
    def mux_logic_a_pin_value(self):
        return 1

    @property
    def mux_logic_b_pin_value(self):
        return 1

    @property
    def mux_io_pin_id(self):
        return 28