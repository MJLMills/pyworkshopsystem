import time

led_matrix = LEDMatrix()
sleep_length_s = 0.1

while True:
    led_matrix.turn_on()
    time.sleep(sleep_length_s)

    led_matrix.turn_off()
    time.sleep(sleep_length_s)

    led_matrix.turn_left_column_on()
    time.sleep(sleep_length_s)
    led_matrix.turn_left_column_off()
    time.sleep(sleep_length_s)

    led_matrix.turn_right_column_on()
    time.sleep(sleep_length_s)
    led_matrix.turn_right_column_off()
    time.sleep(sleep_length_s)

    led_matrix.turn_top_row_on()
    time.sleep(sleep_length_s)
    led_matrix.turn_top_row_off()
    time.sleep(sleep_length_s)

    led_matrix.turn_middle_row_on()
    time.sleep(sleep_length_s)
    led_matrix.turn_middle_row_off()
    time.sleep(sleep_length_s)

    led_matrix.turn_bottom_row_on()
    time.sleep(sleep_length_s)
    led_matrix.turn_bottom_row_off()
    time.sleep(sleep_length_s)