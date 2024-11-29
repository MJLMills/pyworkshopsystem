from abc import ABC, abstractmethod


class IO(ABC):
    """An object with an associated GPIO pin."""
    @property
    @abstractmethod
    def pin_id(self):
        pass