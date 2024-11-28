"""
# A lot of this should be the purview of the PulsesOutputSocket class, i.e. a `pulse` method with settable rate and duty cycle
# look at some examples os square wave classes. Probably better if the parameters are in Hz.
"""
import time
from computer import Computer

pulse_length = 10  # ms
max_interval = 3277  # ms

computer = Computer()
pulses_output_socket_one = computer.pulses_output_socket_one
main_knob = computer.main_knob
main_knob.max_value = max_interval

time_to_turn_pulse_on = 0
"""The next time at which the pulse should be turned on."""

time_to_turn_pulse_off = None
"""The next time at which the pulse should be turned off."""

def pulse_should_begin(time_to_turn_pulse_on):
    return time.ticks_diff(time.ticks_ms, time_to_turn_pulse_on) > 0

def pulse_should_end(time_to_turn_pulse_off):
    return time.ticks_diff(now, time_to_turn_pulse_off) > 0

while True:

    if pulse_should_begin(time_to_turn_pulse_on) > 0:

        pulses_output_socket_one.turn_on()

        pulse_gap = main_knob.read()
        now = time.ticks_ms()
        time_to_turn_pulse_on = time.ticks_add(now, pulse_gap)
        time_to_turn_pulse_off = time.ticks_add(now, pulse_length)

    elif pulses_output_socket_one.is_on() and pulse_should_end(time_to_turn_pulse_off):
        pulses_output_socket_one.turn_off()
