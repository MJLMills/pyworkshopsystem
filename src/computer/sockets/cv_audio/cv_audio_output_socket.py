import machine


class CVAudioOutputSocket(object):
    """A CV/Audio output socket.

    https://docs.micropython.org/en/latest/library/machine.SPI.html#machine-spi
    """

    __SCK_PIN_ID = 18
    """Pin ID for clock signal from the RP2040 to the DAC."""

    __SDI_MOSI_PIN_ID = 19
    """Pin ID for serial data from RP2040 to the DAC, most-significant bit first."""

    __CS_PIN_ID = 21
    """Active-low chip select signal from RP2040 to enable communication with the DAC."""

    __BAUD_RATE_HZ = 20_000_000
    """The max SCK clock rate (in Hz) from the MCP4822 datasheet. Equal to 20 MHz"""

    __BITS = 16
    """The width in bits of each transfer."""

    def __init__(self):
        # create a chip select on the documented SPI CS pin
        self.__chip_select_pin = machine.Pin(self.__CS_PIN_ID, mode=machine.Pin.OUT, value=1)

        self.__chip_select_pin(0)  # select peripheral

        self.__spi = machine.SPI(
            id=0,
            baudrate=self.__BAUD_RATE_HZ,
            polarity=0,
            phase=0,
            bits=self.__BITS,
            firstbit=machine.SPI.MSB,
            sck=self.__SCK_PIN_ID,
            mosi=self.__SDI_MOSI_PIN_ID,
        )

    def write(self, value: int):
        """
        Writes to the DAC are 16-bit words.

        The bytes object (immutable) is 16-bits where:

        15 : DAC_SELECTION_BIT in {0, 1}
        14 : IGNORED
        13 : Output gain selection bit, probably hard-coded in {0, 1}
        12 : Output Shutdown Control bit in {0, 1}, hard-coded to 1
        11-0 : the data value to write to the DAC
        """
        value_u12 = int((value / 65535) * 4095)

        value_u12_bytes = value_u12.to_bytes(12, "big")
        # print(value_u12, int.from_bytes(value_u12_bytes, "little"), value_u12_bytes)

        # value_bytes = value_u12_bytes + b"\x01\x01\x01" + self.DAC_SELECTION_BIT
        value_bytes = self.DAC_SELECTION_BIT + b"\x00\x01\x01" + value_u12_bytes

        self.__spi.write(value_bytes)  # write input bytes on MOSI (to output)

    def __str__(self):
        print(self.__spi)


class CVAudioOutputSocketOne(CVAudioOutputSocket):
    DAC_SELECTION_BIT = b'\x00'


class CVAudioOutputSocketTwo(CVAudioOutputSocket):
    DAC_SELECTION_BIT = b'\x01'


