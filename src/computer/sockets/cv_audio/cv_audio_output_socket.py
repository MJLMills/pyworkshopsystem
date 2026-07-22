import machine
import micropython
from micropython import const
from computer.base.analog_output import AnalogOutput
import uctypes


class CVAudioOutputSocket(AnalogOutput):

    REG_GPIO_OUT_SET = const(0xd0000014)
    """Memory address of the hardware register used to atomically set specific GPIO output pins high."""

    REG_GPIO_OUT_CLR = const(0xd0000018)
    """Memory address of the hardware register used to atomically clear specific GPIO output pins low."""

    PIN_21_MASK = const(1 << 21)
    """Bitmask used to target and control GPIO Pin 21."""

    # SPI0 Status register masks
    SPI_SR_TNF_MASK = const(1 << 1)
    """Bitmask constant used to check Transmit FIFO Not Full status."""

    SPI_SR_BSY_MASK = const(1 << 4)  # SPI Busy Flag
    """Bitmask constant used to check Busy status."""

    HARDWARE_MIN = const(0)
    HARDWARE_MAX = const(4095)
    BAUD_RATE_HZ = const(20_000_000)

    def __init__(self):
        super().__init__()
        self.chip_select_pin = machine.Pin(21, mode=machine.Pin.OUT, value=1)
        self.spi = machine.SPI(
            id=0,
            baudrate=self.BAUD_RATE_HZ,
            polarity=0,
            phase=0,
            bits=8,
            firstbit=machine.SPI.MSB,
            sck=machine.Pin(18),
            mosi=machine.Pin(19),
        )
        self.spi_buffer = bytearray(2)
        self.buf_addr = uctypes.addressof(self.spi_buffer)

    @property
    def hardware_min(self) -> int:
        return self.HARDWARE_MIN

    @property
    def hardware_max(self) -> int:
        return self.HARDWARE_MAX

    def write(self, value: int):
        # Extract primitive values out of structures before entering viper
        self._write_viper(
            value,
            self.DAC_HIGH_BYTE,
            self.buf_addr,
            self.PIN_21_MASK,
            self.SPI_SR_TNF_MASK,
            self.SPI_SR_BSY_MASK
        )

    @staticmethod
    @micropython.viper
    def _write_viper(value: int,
                     dac_high_byte: int,
                     buf_ptr: ptr8,
                     cs_mask: int,
                     tnf_mask: int,
                     bsy_mask: int):
        # 1. Process value
        inverted_val = (~value) & 0xFFF

        # 2. Write to buffer pointer
        buf_ptr[0] = dac_high_byte | (inverted_val >> 8)
        buf_ptr[1] = inverted_val & 0xFF

        # 3. Create pointer structures
        sio_regs = ptr32(0xd0000000)  # SIO Base
        spi_regs = ptr32(0x4003c000)  # SPI0 Base

        # 4. Pull CS Low (Clear register at 0xd0000018 -> index 6)
        sio_regs[6] = cs_mask

        # 5. Push Byte 0 (Wait for TX FIFO space)
        while not (spi_regs[3] & tnf_mask):
            pass
        spi_regs[2] = int(buf_ptr[0])

        # 6. Push Byte 1 (Wait for TX FIFO space)
        while not (spi_regs[3] & tnf_mask):
            pass
        spi_regs[2] = int(buf_ptr[1])

        # 7. Wait completely until all bits are shifted out
        while spi_regs[3] & bsy_mask:
            pass

        # 8. Pull CS High (Set register at 0xd0000014 -> index 5)
        sio_regs[5] = cs_mask

    def __str__(self):
        return f"{self.__class__.__name__}: (min = {self.hardware_min}, max = {self.hardware_max})"


class CVAudioOutputSocketOne(CVAudioOutputSocket):
    DAC_HIGH_BYTE = const(0x30)


class CVAudioOutputSocketTwo(CVAudioOutputSocket):
    DAC_HIGH_BYTE = const(0xB0)
