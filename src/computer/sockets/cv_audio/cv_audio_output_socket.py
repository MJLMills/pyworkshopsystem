import machine
from base.analog_output import AnalogOutput


class CVAudioOutputSocket(AnalogOutput):
    """The CV/Audio output sockets of the Computer.

    https://docs.micropython.org/en/latest/library/machine.SPI.html#machine-spi

    1) How do you write to the outputs?

    The CV/Audio outputs are bipolar (inverted) and DC-coupled.
    Outputs must go through a MCP4822 (2-input-channel) DAC to the sockets.

    "Communication with the device is accomplished via a simple serial interface using SPI protocols."

    Pins 18, 19 and 21 are specified for control of the MCP4822.
    Pin 18 is labeled DAC_SCK / SCK - clock signal from main
    Pin 19 is labeled DAC_SDI / MOSI - serial data from main, most-significant bit first
    Pin 21 is labeled DAC_CS / CS - active-low chip select signal from main to enable communication with a specific sub device.
    MISO is not included as the DAC (sub) does not output to main (the Pi)

    Looks like you setup a connection with the SPI class and write through it.
    There are two analog outputs on the DAC that are going to the sockets
    Each 16-bit word written to the DAC over SPI has a flag on byte 15 for which DAC you want to write to.
    The datasheet has the rest, but there are 12 bits for the value.
    """

    __SCK_PIN_ID = 18
    """Pin ID for clock signal from the RP2040 to the DAC."""

    __SDI_MOSI_PIN_ID = 19
    """Pin ID for serial data from RP2040 to the DAC, most-significant bit first."""

    __CS_PIN_ID = 21
    """Active-low chip select signal from RP2040 to enable communication with the DAC."""

    __BAUD_RATE_HZ = 20_000_000
    """The max SCK clock rate (in Hz) from the MCP4822 datasheet. Equal to 20 MHz"""

    __BITS = 8
    """The width in bits of each transfer."""

    def __init__(self):
        super().__init__()
        # create a chip select on the documented SPI CS pin
        self.__chip_select_pin = machine.Pin(self.__CS_PIN_ID,
                                             mode=machine.Pin.OUT, value=1)

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

        #self._ranged_min_value = RangedVariable(
        #    min_value=self.hardware_max / 2,
        #    max_value=0,
        #    value=0)

        #self._ranged_max_value = RangedVariable(
        #    min_value=self.hardware_max / 2,
        #    max_value=self.hardware_max,
        #    value=self.hardware_max)

    @property
    def hardware_min(self) -> int:
        return 0

    @property
    def hardware_max(self) -> int:
        return 4095

    @property
    def min_value(self) -> int:
        """The minimum value of the analog output."""
        return self.hardware_min
        #return self._ranged_min_value.value

    @min_value.setter
    def min_value(self, min_value: int) -> None:
        """Set the minimum value of the analog output."""
        self._ranged_min_value.value = int(min_value)

    @property
    def max_value(self) -> int:
        """The maximum value of the analog output."""
        return self.hardware_max
        #return self._ranged_max_value.value

    @max_value.setter
    def max_value(self, max_value: int) -> None:
        """Set the maximum value of the analog output."""
        self._ranged_max_value.value = int(max_value)

    def write(self, value: int):
        """Write the given value to the DAC.

        Parameters
        ----------
        value
            The 12-bit uint (a python int ranging 0 to 4095) to write.

        Writes to the DAC are 16-bit words.
        The value to write to the DAC is a 12-bit unsigned integer.

        The bytes object (immutable) is 16-bits where:

        15 : DAC_SELECTION_BIT in {0, 1}
        14 : IGNORED
        13 : Output gain selection bit, hard-coded to 1
        12 : Output Shutdown Control bit, hard-coded to 1
        11-0 : the data value to write to the DAC
        """

        # value = int((value / 65535) * 4095)

        dac_data = self.__DAC_STRING | (int(self.max_value - value) & 0xFFF)

        try:
            self.__chip_select_pin.value(0)
            self.__spi.write(bytes((dac_data >> 8, dac_data & 0xFF)))
        finally:
            self.__chip_select_pin.value(1)

    def __str__(self):
        return self.__class__.__name__ + ": (min = " + str(
            self.min_value) + ", max = " + str(self.max_value) + ")"


class CVAudioOutputSocketOne(CVAudioOutputSocket):
    __DAC_STRING = 0b0011000000000000


class CVAudioOutputSocketTwo(CVAudioOutputSocket):
    __DAC_STRING = 0b1011000000000000
