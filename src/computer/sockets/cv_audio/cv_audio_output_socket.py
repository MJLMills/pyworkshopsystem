from machine import Pin, SPI
from multiplexed_input import IO


class CVAudioOutputSocket(IO):

    __SCK_PIN_ID = 18
    """Clock signal from the RP2040 to the DAC."""

    SDI_MOSI_PIN_ID = 19
    """serial data from RP2040, most-significant bit first."""

    CS_PIN_ID = 21
    """Active-low chip select signal from RP2040 to enable communication with the DAC.
    
    CS (Chip Select), to select a particular device on a bus with which communication takes place. Management of a CS signal should happen in user code (via machine.Pin class)."""

    def __init__(self):

        self.__spi = SPI(
            id=0,
            baudrate=80_000_000,  # in Hz, how should these be set? This is the SCK clock rate.
            polarity=0,
            phase=0,
            bits=16,
            firstbit=SPI.MSB,
            sck=self.__SCK_PIN_ID,
            mosi=self.SDI_MOSI_PIN_ID,
            miso=None
        )

    def write(self, value: bytes):
        """
        Writes to the DAC are 16-bit words.
        """
        self.__spi.write(bytes)  # write input bytes on MOSI (to output)


class CVAudioOutputSocketOne(CVAudioOutputSocket):

    DAC_SELECTION_BIT = b'1'

    @property
    def pin_id(self):
        return None


class CVAudioOutputSocketTwo(CVAudioOutputSocket):

    DAC_SELECTION_BIT = b'0'

    @property
    def pin_id(self):
        return None
