from enum import Enum
import machine
from .knobs import MainKnob, KnobX, KnobY
from .switches import SwitchZ
from .sockets import CVAudioInputSocketOne
from .sockets import CVAudioInputSocketTwo
from .sockets import CVAudioOutputSocketOne
from .sockets import CVAudioOutputSocketTwo
from .sockets import CVInputSocketOne
from .sockets import CVInputSocketTwo
from .sockets import CVOutputSocketOne
from .sockets import CVOutputSocketTwo
from .sockets import PulseInputSocketOne
from .sockets import PulseInputSocketTwo
from .sockets import PulseOutputSocketOne
from .sockets import PulseOutputSocketTwo
from .leds import LEDMatrix



class Computer(object):
    """Music Thing Modular Workshop System Computer Module.

    This class abstracts the Computer module in order to make interacting with
    its controls as direct as possible. The package uses micropython for interaction
    with the hardware.
    The module provides the following set of controls (top-to-bottom, left-to-right):

    A "main knob" - a potentiometer with a large dial.
    X and Y knobs - trimmer potentiometers.
    Z switch - (ON)-OFF-ON, momentary push down, normal pull up.
    Two CV/Audio inputs
    Two CV/Audio outputs
    Two CV inputs
    Two CV outputs
    Two pulse inputs
    Two pulse outputs
    Six LEDs (arranged in a 3x2 matrix)

    Each of these is modeled with a dedicated class, minimizing re-use and
    hiding the complexity of the hardware, while providing access to the micropython
    objects for use where specific functionality is not yet implemented.
    """
    eeprom_structure = {
        0: 2,  # magic number = 2001 - if number is present, eeprom has been initialized
        2: 1,  # version number 0-255
        3: 1,  # padding
        4: 1,  # Channel 0 - Number of entries 0-9
        5: 40,  # 10 x 4 byte blocks: 1 x 4-bit voltage + 4 bits space | 1 x 24 bit setting = 32 bits = 4 bytes
        45: 1,  # Channel 1 - Number of entries 0-9
        46: 40,  # 10 x 4-byte blocks: 1x 4-bit voltage + 4 bits space | 1 x 24 bit setting = 32 bits = 4 bytes
        86: 2  # CRC Check over previous data
    }
    """Memory map for 2 x precision PWM voltage outputs = Channels 0 and 1."""

    class PinId(Enum):
        """GPIO Pin IDs not assigned to Computer classes.

        NB: GPIO pin 20 is not connected.

        UART0_TX, UART0_RX
            From unpopulated headers next to LEDs.
        NORMALIZATION_PROBE
            Connected to the switch inputs on all the inputs via a BAT45 protection diode.
            Toggle this pin to identify which sockets have plugs in them.
            The normalization probe high reads ~2600.
        BOARD_IDENTIFICATION
            GPIO Pins 5, 6, 7 = binary bits
            0 0 0 = Proto1.2 (all pins floating)
            1 0 0 = Proto 2.0, 2.0.1, Rev1.
        EEPROM_SDA, EEPROM_SCL
            Connects to Zetta ZD24C08A EEPROM, clone of 24C0* chips.
            Contains 8 kbits (1024 x 8).
            SDA & SCL lines have 2.2k pullups.
            Data is stored in 8 x 1024 pages addresses 0x50 to 0x5B.
        DAC_SCK_SCK, DAC_SDI_MOSI, DAC_CS_CS
            MCP4822 Control.
        """
        UART0_TX = 0
        UART0_RX = 1
        NORMALIZATION_PROBE = 4
        BOARD_IDENTIFICATION_A = 5
        BOARD_IDENTIFICATION_B = 6
        BOARD_IDENTIFICATION_C = 7
        EEPROM_SDA = 16
        EEPROM_SCL = 17
        DAC_SCK_SCK = 18
        DAC_SDI_MOSI = 19
        DAC_CS_CS = 21

    class Multiplexer(object):
        """The multiplexer on the Computer.

        This is a 4052 multiplexer with 2x4 channels.
        The multiplexer has two output pins that are set to
        determine which analog input will be read via the ADC on
        the I/O pins. The uC I/O pins are connected to analog inputs
        2 and 3 from the multiplexer.

        Truth table is as follows:

        A | B | ADC Channel 2 GPIO 28 | ADC Channel 3 GPIO 29
        --|---|-----------------------|----------------------
        0 | 0 | Main Knob             | CV 1
        0 | 1 | X Knob                | CV 2
        1 | 0 | Y Knob                | CV 1
        1 | 1 | Z Switch              | CV 2
        """
        MUX_LOGIC_A_PIN_ID = 24
        """The ID of the first multiplexer output pin."""
        MUX_LOGIC_B_PIN_ID = 25
        """The ID of the second multiplexer output pin."""
        MUX_IO_PIN_ONE_ID = 28
        """The ID of the first multiplexer I/O pin."""
        MUX_IO_PIN_TWO_ID = 29
        """The ID of the second multiplexer I/O pin."""

        MUX_LOGIC_A_PIN = machine.Pin(MUX_LOGIC_A_PIN_ID,
                                      machine.Pin.OUT)

        MUX_LOGIC_B_PIN = machine.Pin(MUX_LOGIC_B_PIN_ID,
                                      machine.Pin.OUT)

        MUX_IO_ADC_ONE = machine.ADC(MUX_IO_PIN_ONE_ID)
        MUX_IO_ADC_TWO = machine.ADC(MUX_IO_PIN_TWO_ID)

        def __init__(self):
            self.mux_logic_pin_a_value = 0
            self.mux_logic_pin_b_value = 0

        @property
        def mux_logic_pin_a_value(self):
            return self.MUX_LOGIC_A_PIN.value()

        @mux_logic_pin_a_value.setter
        def mux_logic_pin_a_value(self, value):
            self.MUX_LOGIC_A_PIN.value(value)

        @property
        def mux_logic_pin_b_value(self):
            return self.MUX_LOGIC_B_PIN.value()

        @mux_logic_pin_b_value.setter
        def mux_logic_pin_b_value(self, value):
            self.MUX_LOGIC_B_PIN.value(value)

        def set_logic_pin_values(self, a, b):
            """Set the values of the logic pins."""
            self.mux_logic_pin_a_value = a
            self.mux_logic_pin_b_value = b

    __MULTIPLEXER = Multiplexer()
    """The multiplexer used to read hardware values."""

    def __init__(self):

        self.main_knob = MainKnob(multiplexer=self.__MULTIPLEXER)
        self.knob_x = KnobX(multiplexer=self.__MULTIPLEXER)
        self.knob_y = KnobY(multiplexer=self.__MULTIPLEXER)
        self.switch_z = SwitchZ(multiplexer=self.__MULTIPLEXER)

        self.cv_audio_input_socket_one = CVAudioInputSocketOne()
        self.cv_audio_input_socket_two = CVAudioInputSocketTwo()
        self.cv_audio_output_socket_one = CVAudioOutputSocketOne()
        self.cv_audio_output_socket_two = CVAudioOutputSocketTwo()

        self.cv_input_socket_one = CVInputSocketOne(multiplexer=self.__MULTIPLEXER)
        self.cv_input_socket_two = CVInputSocketTwo(multiplexer=self.__MULTIPLEXER)
        self.cv_output_socket_one = CVOutputSocketOne()
        self.cv_output_socket_two = CVOutputSocketTwo()

        self.pulses_input_socket_one = PulseInputSocketOne()
        self.pulses_input_socket_two = PulseInputSocketTwo()
        self.pulses_output_socket_one = PulseOutputSocketOne()
        self.pulses_output_socket_two = PulseOutputSocketTwo()

        self.led_matrix = LEDMatrix()

    def get_version(self):
        raise NotImplementedError()
