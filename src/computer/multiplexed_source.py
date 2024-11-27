from abc import ABC, abstractmethod


class MultiplexedSource(ABC):

    def __init__(self, multiplexer):
        super().__init__()
        self.__multiplexer = multiplexer


    @property
    @abstractmethod
    def mux_logic_a_pin_value(self):
        pass

    @property
    @abstractmethod
    def mux_logic_b_pin_value(self):
        pass

    @property
    @abstractmethod
    def mux_io_pin_id(self):
        pass

    def read(self):
        self.__multiplexer.set_logic_pin_values(self.mux_logic_a_pin_value,
                                                self.mux_logic_b_pin_value)

        return self.__multiplexer.read(self.mux_io_pin_id)
