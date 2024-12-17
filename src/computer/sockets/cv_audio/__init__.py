"""
The CV/Audio input and outputs are bipolar and DC-coupled, ranging ~-6 to ~+6 V.
The audio ins and outs might be used for effects, or as oscillators, or as extra
CV inputs and outputs. Digital oscillators will be particularly useful for polyphony
and pitch precision or microtuning.


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

2) How do you read from the inputs?

The CV/Audio inputs are bipolar (inverted) and DC-coupled.
They require calibration for precise readings.
The left input is normalled to the right input, so if only one
socket is plugged in, both channels receive the same input.


The input signals are scaled (presumably in hardware) and then go to channels
0 and 1 of an internal analog to digital converter (Note that the multiplexer
makes use of channels 3 and 4 to read the CV inputs, knobs and switch). From
there they appear to go to two assigned GPIO pins (26 and 27) on the Pi,
from which they should be readable as analog inputs, as for the CV outputs, with ranges as follows:

Inverted bipolar analog input,into 12(?) bit internal ADC
+6v = 0
0v = 2048
-6v = 4095

If this works, should be no issue reading in, same as CV inputs?

"""