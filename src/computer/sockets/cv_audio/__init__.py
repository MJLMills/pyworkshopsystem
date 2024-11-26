"""
These are also bipolar DC-coupled inputs and outputs, approximately -6V to +6V.
The inputs are scaled, then go directly to channels 0 and 1 of the ADC. As for
the CV sockets, theoretically 12 bits, probably fewer.
Both DC-coupled.
The left input is normalled to the right input so if only one socket is plugged in,
both channels see that input.
Outputs come through a MCP4822 DAC.
The audio ins and outs might be used for effects, or as oscillators, or as extra
CV inputs and outputs. Digital oscillators will be particularly useful for polyphony
and pitch precision or microtuning.
"""