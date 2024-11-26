"""
These are bipolar DC-coupled inputs and outputs, both approximately -6V to +6V.
Inputs are read through a 4052 multiplexer into the internal ADC on the RP2040,
so are theoretically 12-bit but really more like 8-10 bits. The maximum read frequency has not been tested.
Outputs are 11-bit PWM signals at 60 kHz, filtered with two-pole active multifeedback filters, so they
should be reasonably clean and fast settling.
They'll be used to control oscillators, filters, envelope speeds, and can also double as extra gates,
LFOs or maybe even audio inputs.
It is also possible to calibrate the outputs to reasonable accuracy using ~15-bit Delta Sigma PWM.
"""