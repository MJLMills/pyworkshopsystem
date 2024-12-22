import machine
from .knobs import MainKnob, KnobX, KnobY
from .switches import SwitchZ
from .sockets import CVAudioInputSocketOne
from .sockets import CVAudioInputSocketTwo
from .sockets import CVAudioInputSockets
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


# NB: if you instantiate the Computer, it currently creates all the controls when
# you may only want a subset. One way around this is to only instantiate the
# bits you want. A better option would be "lazy loading" the hardware classes.


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
    EEPROM_STRUCTURE = {
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

    KNOWN_BOARD_VERSIONS = {
        (0, 0, 0): "Proto 1.2",
        (1, 0, 0): "Proto 2.0, 2.0.1, Rev1"
    }
    """Known versions of the Computer board."""

    PIN_IDS = {
        "UART0_TX": 0,
        "UART0_RX": 1,
        "NORMALIZATION_PROBE": 4,
        "BOARD_IDENTIFICATION_A": 5,
        "BOARD_IDENTIFICATION_B": 6,
        "BOARD_IDENTIFICATION_C": 7,
        "EEPROM_SDA": 16,
        "EEPROM_SCL": 17,
    }
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
    """

    def __init__(self):

        self.main_knob = MainKnob()
        self.knob_x = KnobX()
        self.knob_y = KnobY()
        self.switch_z = SwitchZ()

        self.cv_audio_input_socket_one = CVAudioInputSocketOne()
        self.cv_audio_input_socket_two = CVAudioInputSocketTwo()
        self.cv_audio_input_sockets = CVAudioInputSockets()
        self.cv_audio_output_socket_one = CVAudioOutputSocketOne()
        self.cv_audio_output_socket_two = CVAudioOutputSocketTwo()

        self.cv_input_socket_one = CVInputSocketOne()
        self.cv_input_socket_two = CVInputSocketTwo()
        self.cv_output_socket_one = CVOutputSocketOne()
        self.cv_output_socket_two = CVOutputSocketTwo()

        self.pulses_input_socket_one = PulseInputSocketOne()
        self.pulses_input_socket_two = PulseInputSocketTwo()
        self.pulses_output_socket_one = PulseOutputSocketOne()
        self.pulses_output_socket_two = PulseOutputSocketTwo()

        self.led_matrix = LEDMatrix()

    @staticmethod
    def board_version():
        """Get the board version encoded in the values of GPIO pins 5, 6 and 7.

        (0, 0, 0) = Proto1.2
        (1, 0, 0) = Proto 2.0, 2.0.1, Rev1.
        """
        pin_a = machine.Pin(Computer.PinId.BOARD_IDENTIFICATION_A, machine.Pin.IN, machine.Pin.PULL_UP)
        pin_b = machine.Pin(Computer.PinId.BOARD_IDENTIFICATION_B, machine.Pin.IN, machine.Pin.PULL_UP)
        pin_c = machine.Pin(Computer.PinId.BOARD_IDENTIFICATION_C, machine.Pin.IN, machine.Pin.PULL_UP)

        pin_values = (pin_a.value(), pin_b.value(), pin_c.value())

        try:
            return Computer.KNOWN_BOARD_VERSIONS[pin_values]
        except KeyError:
            return "Unknown board version with pin values: ", pin_values
