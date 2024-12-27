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


# NB: if you instantiate the Computer, it currently creates all the controls when
# you may only want a subset. One way around this is to only instantiate the
# bits you want. A better option would be "lazy loading" the hardware classes.
# TODO - this lazy loading to minimize startup time.

class Computer(object):
    """Music Thing Modular Workshop System Computer Module.

    This class abstracts the Computer module in order to make interacting with
    its controls as direct as possible. The package uses micropython for
    interaction with the hardware.
    The module provides the following set of controls (top-to-bottom,
    left-to-right):

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
    hiding the complexity of the hardware, while providing access to the
    micropython objects for use where specific functionality is not yet
     implemented.
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

    KNOWN_BOARD_VERSION_NAMES = {
        (False, False, False): "Proto 1.2",
        (True, False, False): "Proto 2.0, 2.0.1, Rev1"
    }
    """Known versions of the Computer board."""

    PIN_IDS = {
        "UART0_TX": 0,
        "UART0_RX": 1,
        "NORMALIZATION_PROBE": 4,
        "EEPROM_SDA": 16,
        "EEPROM_SCL": 17,
    }
    """GPIO Pin IDs not assigned to Computer classes.

    NB: GPIO pin 20 is not connected.

    UART0_TX, UART0_RX
        From unpopulated headers next to LEDs.
    NORMALIZATION_PROBE
        Connected to the switch inputs on all the inputs via a BAT45 protection
        diode. Toggle this pin to identify which sockets have plugs in them.
        The normalization probe high reads ~2600.
    EEPROM_SDA, EEPROM_SCL
        Connects to Zetta ZD24C08A EEPROM, clone of 24C0* chips.
        Contains 8 kbits (1024 x 8).
        SDA & SCL lines have 2.2k pullups.
        Data is stored in 8 x 1024 pages addresses 0x50 to 0x5B.
    """

    def __init__(self):

        self._board_version = None
        self._board_version_name = None

        self.main_knob = MainKnob()
        self.knob_x = KnobX()
        self.knob_y = KnobY()
        self.switch_z = SwitchZ()

        self.cv_audio_input_socket_one = CVAudioInputSocketOne()
        self.cv_audio_input_socket_two = CVAudioInputSocketTwo()
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

    @property
    def board_version(self) -> tuple:
        """The version of the Computer board.

        Returns
        -------
        tuple of bool
            The three Boolean values identifying the board version."""
        if self._board_version is None:
            self._board_version = self.__read_board_version()

        return self._board_version

    @property
    def board_version_name(self) -> str:
        """The name of this board version."""

        try:
            return Computer.KNOWN_BOARD_VERSION_NAMES[self.board_version]
        except KeyError:
            raise ValueError(
                "Unknown board version with pin values: ", self.board_version
            )

    @staticmethod
    def __read_board_version() -> tuple:
        """Read the board version ID.

        The board version is stored in three bits that are read from GPIO
        digital input pins with IDs 5, 6 and 7. The following table shows the
        mapping between board version IDs and names provided in the Computer
        documentation:

        (False, False, False) = Proto1.2
        (True, False, False) = Proto 2.0, 2.0.1, Rev1.

        Note that this method (and any code that relies on the board version
        being Proto1.2) is untested due to lack of access to the appropriate
        physical board. Proto 2.0.1 and Rev1 are identical.

        See Also
        --------
        For information on the changes across different board types, see the
        Computer documentation.

        Returns
        -------
        tuple of bool
            The three Boolean values identifying the board version.
        """
        pin_a = machine.Pin(5,
                            machine.Pin.IN,
                            machine.Pin.PULL_UP)

        pin_b = machine.Pin(6,
                            machine.Pin.IN,
                            machine.Pin.PULL_UP)

        pin_c = machine.Pin(7,
                            machine.Pin.IN,
                            machine.Pin.PULL_UP)

        return (bool(pin_a.value()),
                bool(pin_b.value()),
                bool(pin_c.value()))
