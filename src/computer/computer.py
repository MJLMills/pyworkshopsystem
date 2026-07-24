import machine
from micropython import const
from .normalization_probe import NormalizationProbe


class Computer(object):
    """Music Thing Modular Workshop System Computer Module.

    This class abstracts the Computer module in order to make interacting with
    its controls as direct as possible. The package uses micropython for
    interaction with the hardware. The module provides the following set of controls (top-to-bottom,
    left-to-right):

    * A "main knob"
        A potentiometer with a large dial.
    * X and Y knobs
        Two trimmer potentiometers.
    * Z switch
        An (ON)-OFF-ON switch with momentary push down and latching push up.
    * Two separate CV/Audio inputs
        Labeled 1 and 2 herein, corresponding to physical left and right.
    * Two separate CV/Audio outputs
        Labeled 1 and 2 herein, corresponding to physical left and right.
    * Two separate CV inputs
        Labeled 1 and 2 herein, corresponding to physical left and right.
    * Two separate CV outputs
        Labeled 1 and 2 herein, corresponding to physical left and right.
    * Two separate pulse inputs
        Labeled 1 and 2 herein, corresponding to physical left and right.
    * Two separate pulse outputs
        Labeled 1 and 2 herein, corresponding to physical left and right.
    * Six LEDs
        Arranged in a 3x2 matrix.

    Each of these controls is abstracted as a dedicated class, minimizing redundancy and
    hiding the complexity of the hardware, while providing access to the
    micropython objects for use where specific functionality is not yet implemented.

    This class enforces a strict singleton pattern. Once instantiated, further attempts to instantiate
    will raise a RuntimeError. This is intended to fail fast so that the error can be quickly corrected.

    NB: GPIO pin 20 is not connected.

    Raises
    ------
    RuntimeError
        When a second instance of the class is instantiated.
    """
    KNOWN_BOARD_VERSION_NAMES = {
        (False, False, False): "Proto 1.2",
        (True, False, False): "Proto 2.0, 2.0.1, Rev1"
    }
    """Known versions of the Computer board."""

    UART_TX_PIN_ID = const(0)
    UART_RX_PIN_ID = const(1)
    """GPIO Pin IDs for UART connections."""

    _instance = None

    def __init__(self):

        if Computer._instance is not None:
            raise RuntimeError("Computer already initialized.")

        Computer._instance = self

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

        self._normalization_probe = NormalizationProbe()

        self.__input_sockets = [None] * 6
        self.__active_socket_count = 0

    # TODO - test this still works
    def update_input_socket_jack_status(self, fire_all_signals: bool = False) -> None:
        """Update whether sockets have jacks or not using the normalization probe.

        The update process is as follows: write each probe bit once, then read all undecided sockets for that bit.
        Remove sockets from the undecided set as soon as they're classified. Loop over bits, writing once per bit and
        testing only undecided sockets. Any remaining undecided sockets are treated as not connected.

        Parameters
        ----------
        fire_all_signals:bool
            Whether to emit jack inserted/removed signals.
        """
        self.__active_socket_count = 0

        if self._cv_audio_input_socket_one is not None:
            self.__input_sockets[self.__active_socket_count] = self._cv_audio_input_socket_one
            self.__active_socket_count += 1
        if self._cv_audio_input_socket_two is not None:
            self.__input_sockets[self.__active_socket_count] = self._cv_audio_input_socket_two
            self.__active_socket_count += 1
        if self._cv_input_socket_one is not None:
            self.__input_sockets[self.__active_socket_count] = self._cv_input_socket_one
            self.__active_socket_count += 1
        if self._cv_input_socket_two is not None:
            self.__input_sockets[self.__active_socket_count] = self._cv_input_socket_two
            self.__active_socket_count += 1
        if self._pulses_input_socket_one is not None:
            self.__input_sockets[self.__active_socket_count] = self._pulses_input_socket_one
            self.__active_socket_count += 1
        if self._pulses_input_socket_two is not None:
            self.__input_sockets[self.__active_socket_count] = self._pulses_input_socket_two
            self.__active_socket_count += 1

        if self.__active_socket_count == 0:
            return

        probe = self._normalization_probe
        n_bits = probe.n_bits

        for _ in range(n_bits):
            if self.__active_socket_count == 0:
                break

            written_value = probe.write()
            i = 0
            while i < self.__active_socket_count:
                socket = self.__input_sockets[i]
                read_value = socket.read_norm_probe()

                if read_value != written_value:
                    socket.has_jack = True
                    if fire_all_signals:
                        socket.jack_inserted.emit()

                    self.__active_socket_count -= 1
                    self.__input_sockets[i] = self.__input_sockets[self.__active_socket_count]
                else:
                    i += 1

        for i in range(self.__active_socket_count):
            self.__input_sockets[i].has_jack = False
            if fire_all_signals:
                self.__input_sockets[i].jack_removed.emit()

    @property
    def eeprom(self):
        if self._eeprom is None:
            from .eeprom import Eeprom
            self._eeprom = Eeprom()

        return self._eeprom

    @property
    def uart(self):
        """
        From unpopulated headers next to LEDs.
        There are two UARTS on the RP2040, UART0 and UART1.
        In this case, UART0 has been mapped to GPIO pins 0/1.
        """
        if self._uart0 is None:
            self._uart0 = machine.UART(
                0,
                baudrate=9600,  # check value
                tx=machine.Pin(Computer.UART_TX_PIN_ID),
                rx=machine.Pin(Computer.UART_RX_PIN_ID)
            )

        return self._uart0

    @property
    def main_knob(self):
        """The main knob on the computer."""
        if self._main_knob is None:
            from .knobs import MainKnob
            self._main_knob = MainKnob()

        return self._main_knob

    @property
    def knob_x(self):
        """The X knob on the computer."""
        if self._knob_x is None:
            from .knobs import KnobX
            self._knob_x = KnobX()

        return self._knob_x

    @property
    def knob_y(self):
        """The Y knob on the computer."""
        if self._knob_y is None:
            from .knobs import KnobY
            self._knob_y = KnobY()

        return self._knob_y

    @property
    def switch_z(self):
        """The Z switch on the computer."""
        if self._switch_z is None:
            from .switch import SwitchZ
            self._switch_z = SwitchZ()

        return self._switch_z

    @property
    def cv_input_socket_one(self):
        """The left CV input socket on the computer."""
        if self._cv_input_socket_one is None:
            from .sockets import CVInputSocketOne
            self._cv_input_socket_one = CVInputSocketOne()

        return self._cv_input_socket_one

    @property
    def cv_input_socket_two(self):
        """The right CV input socket on the computer."""
        if self._cv_input_socket_two is None:
            from .sockets import CVInputSocketTwo
            self._cv_input_socket_two = CVInputSocketTwo()

        return self._cv_input_socket_two

    @property
    def cv_output_socket_one(self):
        """The left CV output socket on the computer."""
        if self._cv_output_socket_one is None:
            from .sockets import CVOutputSocketOne
            self._cv_output_socket_one = CVOutputSocketOne()

        return self._cv_output_socket_one

    @property
    def cv_output_socket_two(self):
        """The right CV output socket on the computer."""
        if self._cv_output_socket_two is None:
            from .sockets import CVOutputSocketTwo
            self._cv_output_socket_two = CVOutputSocketTwo()

        return self._cv_output_socket_two

    @property
    def cv_audio_input_socket_one(self):
        """The left CV/Audio input socket on the Computer."""
        if self._cv_audio_input_socket_one is None:
            from .sockets import CVAudioInputSocketOne
            self._cv_audio_input_socket_one = CVAudioInputSocketOne()

        return self._cv_audio_input_socket_one

    @property
    def cv_audio_input_socket_two(self):
        """The right CV/Audio input socket on the Computer."""
        if self._cv_audio_input_socket_two is None:
            from .sockets import CVAudioInputSocketTwo
            self._cv_audio_input_socket_two = CVAudioInputSocketTwo()

        return self._cv_audio_input_socket_two

    @property
    def cv_audio_output_socket_one(self):
        """The left CV/Audio output socket on the Computer."""
        if self._cv_audio_output_socket_one is None:
            from .sockets import CVAudioOutputSocketOne
            self._cv_audio_output_socket_one = CVAudioOutputSocketOne()

        return self._cv_audio_output_socket_one

    @property
    def cv_audio_output_socket_two(self):
        """The right CV/Audio output socket on the Computer."""
        if self._cv_audio_output_socket_two is None:
            from .sockets import CVAudioOutputSocketTwo
            self._cv_audio_output_socket_two = CVAudioOutputSocketTwo()

        return self._cv_audio_output_socket_two

    @property
    def pulses_input_socket_one(self):
        """The left pulses input socket on the Computer."""
        if self._pulses_input_socket_one is None:
            from .sockets import PulseInputSocketOne
            self._pulses_input_socket_one = PulseInputSocketOne()

        return self._pulses_input_socket_one

    @property
    def pulses_input_socket_two(self):
        """The right pulses input socket on the Computer."""
        if self._pulses_input_socket_two is None:
            from .sockets import PulseInputSocketTwo
            self._pulses_input_socket_two = PulseInputSocketTwo()

        return self._pulses_input_socket_two

    @property
    def pulses_output_socket_one(self):
        """The left pulses output socket on the Computer."""
        if self._pulses_output_socket_one is None:
            from .sockets import PulseOutputSocketOne
            self._pulses_output_socket_one = PulseOutputSocketOne()

        return self._pulses_output_socket_one

    @property
    def pulses_output_socket_two(self):
        """The right pulses output socket on the Computer."""
        if self._pulses_output_socket_two is None:
            from .sockets import PulseOutputSocketTwo
            self._pulses_output_socket_two = PulseOutputSocketTwo()

        return self._pulses_output_socket_two

    @property
    def led_matrix(self):
        """The LED matrix on the Computer."""
        if self._led_matrix is None:
            from .leds import LEDMatrix
            self._led_matrix = LEDMatrix()

        return self._led_matrix

    def read_analog_inputs(self):
        # may be able to speed this up by setting multiplexer pins here
        # each update of the two multiplexer pins takes ~0.15 ms and we're doing it 8 times each time this is called (should be 4 max)
        """Update the current raw values of all the analog inputs."""
        if self._main_knob is not None:
            self._main_knob.read()

        if self._cv_input_socket_one is not None and self._cv_input_socket_one.has_jack:
            self._cv_input_socket_one.read()

        if self._knob_x is not None:
            self._knob_x.read()

        if self._knob_y is not None:
            self._knob_y.read()

        if self._switch_z is not None:
            self._switch_z.read()

        if self._cv_input_socket_two is not None and self._cv_input_socket_two.has_jack:
            self._cv_input_socket_two.read()

        if self._cv_audio_input_socket_one is not None and self._cv_audio_input_socket_one.has_jack:
            self._cv_audio_input_socket_one.read()

        if self._cv_audio_input_socket_two is not None and self._cv_audio_input_socket_two.has_jack:
            self._cv_audio_input_socket_two.read()

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