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
from .eeprom import Eeprom


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
    KNOWN_BOARD_VERSION_NAMES = {
        (False, False, False): "Proto 1.2",
        (True, False, False): "Proto 2.0, 2.0.1, Rev1"
    }
    """Known versions of the Computer board."""

    PIN_IDS = {
        "UART0_TX": 0,
        "UART0_RX": 1,
        "NORMALIZATION_PROBE": 4,
    }
    """GPIO Pin IDs not assigned to Computer classes.

    NB: GPIO pin 20 is not connected.

    UART0_TX, UART0_RX
        From unpopulated headers next to LEDs.
        There are two UARTS on the RP2040, UART0 and UART1.
        In this case, UART0 has been mapped to GPIO pins 0/1.
    NORMALIZATION_PROBE
        Connected to the switch inputs on all the inputs via a BAT45 protection
        diode. Toggle this pin to identify which input (CV/Audio, CV and pulse)
        sockets have plugs in them.
        The normalization probe high reads ~2600.
    """
    def __init__(self):

        self._board_version = None
        self._board_version_name = None
        self._eeprom = None
        self._uart0 = None

        self._main_knob = None
        self._knob_x = None
        self._knob_y = None
        self._switch_z = None

        self._cv_audio_input_socket_one = None
        self._cv_audio_input_socket_two = None
        self._cv_audio_output_socket_one = None
        self._cv_audio_output_socket_two = None

        self._cv_input_socket_one = None
        self._cv_input_socket_two = None
        self._cv_output_socket_one = None
        self._cv_output_socket_two = None

        self._pulses_input_socket_one = None
        self._pulses_input_socket_two = None
        self._pulses_output_socket_one = None
        self._pulses_output_socket_two = None

        self._led_matrix = None

    @property
    def eeprom(self):
        if self._eeprom is None:
            self._eeprom = Eeprom()

        return self._eeprom

    @property
    def uart(self):
        if self._uart0 is None:
            self._uart0 = machine.UART(
                0,
                baudrate=9600,  # check value
                tx=machine.Pin(Computer.PIN_IDS["UART0_TX"]),
                rx=machine.Pin(Computer.PIN_IDS["UART0_RX"])
            )

        return self._uart0

    @property
    def main_knob(self):
        if self._main_knob is None:
            self._main_knob = MainKnob()

        return self._main_knob

    @property
    def knob_x(self):
        if self._knob_x is None:
            self._knob_x = KnobX()

        return self._knob_x

    @property
    def knob_y(self):
        if self._knob_y is None:
            self._knob_y = KnobY()

        return self._knob_y

    @property
    def switch_z(self):
        if self._switch_z is None:
            self._switch_z = SwitchZ()

        return self._switch_z

    @property
    def cv_input_socket_one(self):
        if self._cv_input_socket_one is None:
            self._cv_input_socket_one = CVInputSocketOne()

        return self._cv_input_socket_one

    @property
    def cv_input_socket_two(self):
        if self._cv_input_socket_two is None:
            self._cv_input_socket_two = CVInputSocketTwo()

        return self._cv_input_socket_one

    @property
    def cv_output_socket_one(self):
        if self._cv_output_socket_one is None:
            self._cv_output_socket_one = CVOutputSocketOne()

        return self._cv_output_socket_one

    @property
    def cv_output_socket_two(self):
        if self._cv_output_socket_two is None:
            self._cv_output_socket_two = CVOutputSocketTwo()

        return self._cv_output_socket_two

    @property
    def cv_audio_input_socket_one(self):
        """The left CV/Audio input socket on the Computer."""
        if self._cv_audio_input_socket_one is None:
            self._cv_audio_input_socket_one = CVAudioInputSocketOne()

        return self._cv_audio_input_socket_one

    @property
    def cv_audio_input_socket_two(self):
        """The right CV/Audio input socket on the Computer."""
        if self._cv_audio_input_socket_two is None:
            self._cv_audio_input_socket_two = CVAudioInputSocketTwo()

        return self._cv_audio_input_socket_two

    @property
    def cv_audio_output_socket_one(self):
        if self._cv_audio_output_socket_one is None:
            self._cv_audio_output_socket_one = CVAudioOutputSocketOne()

        return self._cv_audio_output_socket_one

    @property
    def cv_audio_output_socket_two(self):
        if self._cv_audio_output_socket_two is None:
            self._cv_audio_output_socket_two = CVAudioOutputSocketTwo()

        return self._cv_audio_output_socket_two

    @property
    def pulses_input_socket_one(self):
        if self._pulses_input_socket_one is None:
            self._pulses_input_socket_one = PulseInputSocketOne()

        return self._pulses_input_socket_one

    @property
    def pulses_input_socket_two(self):
        if self._pulses_input_socket_two is None:
            self._pulses_input_socket_two = PulseInputSocketTwo()

        return self._pulses_input_socket_two

    @property
    def pulses_output_socket_one(self):
        if self._pulses_output_socket_one is None:
            self._pulses_output_socket_one = PulseOutputSocketOne()

        return self._pulses_output_socket_one

    @property
    def pulses_output_socket_two(self):
        if self._pulses_output_socket_two is None:
            self._pulses_output_socket_two = PulseOutputSocketTwo()

        return self._pulses_output_socket_two

    @property
    def led_matrix(self):
        if self._led_matrix is None:
            self._led_matrix = LEDMatrix()

        return self._led_matrix

    #@timed_function
    def update_analog_inputs(self):  # may be able to speed this up by setting multiplexer pins here
        # each update of the two multiplexer pins takes ~0.15 ms and we're doing it 8 times each time this is called (should be 4 max)
        """Update the current raw values of all of the analog inputs."""
        if self._main_knob is not None:
            self._main_knob.update_latest_value()

        if self._cv_input_socket_one is not None:
            self._cv_input_socket_one.update_latest_value()

        if self._knob_x is not None:
            self._knob_x.update_latest_value()

        if self._knob_y is not None:
            self._knob_y.update_latest_value()

        if self._switch_z is not None:
            self._switch_z.update_latest_value()

        if self._cv_input_socket_two is not None:
            self._cv_input_socket_two.update_latest_value()

        if self._cv_audio_input_socket_one is not None:
            self._cv_audio_input_socket_one.update_latest_value()

        if self._cv_audio_input_socket_two is not None:
            self._cv_audio_input_socket_two.update_latest_value()

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
