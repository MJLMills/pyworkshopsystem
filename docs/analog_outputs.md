## Analog Outputs

There are four analog outputs on the Music Thing Modular Workshop System Computer,
all of which are sockets.

* CV/Audio Output One
* CV/Audio Output Two
* CV Output One
* CV Output Two

### Control Voltage Outputs
The CV output sockets are written to using pulse width modulation (PWM) at 60 kHz, generating pseudo-analog signals.
The output is filtered with external circuitry with an active two-pole (second order) low-pass filter
to remove the high-frequency PWM switching noise, reducing ripple voltage on the analog outputs.

### Control Voltage/Audio Outputs

These outputs are connected directly to an MCP4822 DAC as the RP2040 itself has no native analog output channels.
The DAC enables true analog sound output, and is a dual-channel, 12-bit DAC that communicates via the Serial Peripheral Interface (SPI) protocol. 
The SPI communication enables audio-rate updates and precise control over CV at speeds up to 20 MHz.

The SPI requires connection of three pins of the MCP4822 DAC to the RP2040:

* SCK (Serial Clock, GPIO 18)
  * The RP2040 generates this signal to sync data transmission.
* MOSI or TX (Main out Target In, GPIO 19)
  * Used by the RP2040 to send data to the MCP4822.
* CS (Chip Select, GPIO 21)
  * Controlled by the RP2040 to activate a specific target chip.

Note that two-way SPI communication also requires a MISO (also called RX) (Main in Target Out)
For the Computer module, this connection is not needed as the MCP4822 only _receives_ data from the RP2040.

Micropython provides the `machine.SPI` class to abstract the SPI connection.
The clock is sent continuously to the DAC from the RP2040 at the maximum 20 MHz.
Writing to the TX pin is achieved by sending 16-bit bytestrings to the DAC.