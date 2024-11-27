from abc import ABC, abstractmethod


class MultiplexedSource(ABC):

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
