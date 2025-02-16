import machine


class Eeprom(object):
    """
    Connects to Zetta ZD24C08A EEPROM, clone of 24C0* chips.
    8k I2C eeprom on GPIO16 (SDA) and GPIO17 (SCL).
    Contains 8 kbits (1024 x 8).
    SDA & SCL lines have 2.2k pullups.
    Data is stored in 8 x 1024 pages addresses 0x50 to 0x5B.
    """
    EEPROM_STRUCTURE = {
        0: 2,   # magic number = 2001
                # if number is present, eeprom has been initialized
        2: 1,   # version number 0-255
        3: 1,   # padding
        4: 1,   # Channel 0 - Number of entries 0-9
        5: 40,  # 10 x 4 byte blocks:
                # 1 x 4-bit voltage + 4 bits space |
                # 1 x 24 bit setting = 32 bits = 4 bytes
        45: 1,  # Channel 1 - Number of entries 0-9
        46: 40, # 10 x 4-byte blocks:
                # 1x 4-bit voltage + 4 bits space |
                # 1 x 24 bit setting = 32 bits = 4 bytes
        86: 2   # CRC Check over previous data
    }
    """Memory map for 2 x precision PWM voltage outputs = Channels 0 and 1."""

    SDA_PIN_ID = 16
    SCL_PIN_ID = 17
    def __init__(self):
        self.i2c = machine.I2C(0,
                               scl=machine.Pin(Eeprom.SCL_PIN_ID,
                                               machine.Pin.OUT,
                                               machine.Pin.PULL_UP),
                               sda=machine.Pin(Eeprom.SDA_PIN_ID,
                                               machine.Pin.OUT,
                                               machine.Pin.PULL_UP),
                               )
