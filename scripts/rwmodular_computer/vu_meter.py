"""This example uses the LEDs as a VU meter for audio inputs 1 & 2.

This example implies the value of a reusable VU meter class.
"""
from computer import Computer


n_samples_per_iteration = 10
audio_limits = (2000, 8000, 20000)

def audio_value_to_num_leds(value):

    if value < audio_limits[0]:
        return 0
    elif value in range(audio_limits[0], audio_limits[1]):
        return 1
    elif value in range(audio_limits[1], audio_limits[2]):
        return 2
    elif value >= audio_limits[2]:
        return 3

computer = Computer()
cv_audio_input_sockets = computer.cv_audio_input_sockets
led_matrix = computer.led_matrix

while True:
    # read the range of values from the left and right CV/audio sockets over n samples
    left_audio_value, right_audio_value = cv_audio_input_sockets.read_n(n=n_samples_per_iteration)

    # turn off the matrix
    led_matrix.turn_off()
    # light the left column using left
    led_matrix.turn_left_column_on(num_leds=audio_value_to_num_leds(left_audio_value))
    # light the right column using right
    led_matrix.turn_right_column_on(num_leds=audio_value_to_num_leds(right_audio_value))
