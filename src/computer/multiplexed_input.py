from abc import ABC, abstractmethod


class MultiplexedInput(ABC):
    """A multiplexed source of data.

    The set of inputs sharing the multiplexer are the main, x and y knobs,
    the Z switch and CV input sockets 1 and 2. By subclassing this class
    and defining the three abstract properties, these inputs can all share
    the same implementation of the read method.

    Methods
    -------
    read
        Read the value of this input from the multiplexer.
    """
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
