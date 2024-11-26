import machine


class KnobX(object):

    MUX_LOGIC_A_PIN_VALUE = 0
    MUX_LOGIC_B_PIN_VALUE = 1

    PIN_ID = 28

    def __init__(self, multiplexer):
        self.__multiplexer = multiplexer

    def read(self):
        self.__multiplexer.set_logic_pin_values(self.MUX_LOGIC_A_PIN_VALUE,
                                                self.MUX_LOGIC_B_PIN_VALUE)

        return machine.ADC(self.__multiplexer.MUX_IO_PIN_ONE_ID).read_u16()
