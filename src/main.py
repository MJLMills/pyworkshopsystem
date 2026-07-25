import time
from computer.leds import LEDMatrix

sleep_time_seconds = 0.25
gamma_table_size = 1024
fade_step_length_ms = 10
sleep = time.sleep

led_matrix = LEDMatrix(start_value=0, table_size=gamma_table_size)

led_one = led_matrix.get_by_index(1)
led_two = led_matrix.get_by_index(2)
led_three = led_matrix.get_by_index(3)
led_four = led_matrix.get_by_index(4)
led_five = led_matrix.get_by_index(5)
led_six = led_matrix.get_by_index(6)

try:
    while True:
        led_matrix.toggle()
        sleep(sleep_time_seconds)
        led_matrix.toggle()
        sleep(sleep_time_seconds)
        led_one.toggle()
        sleep(sleep_time_seconds)
        led_two.toggle()
        sleep(sleep_time_seconds)
        led_three.toggle()
        sleep(sleep_time_seconds)
        led_four.toggle()
        sleep(sleep_time_seconds)
        led_five.toggle()
        sleep(sleep_time_seconds)
        led_six.toggle()
        sleep(sleep_time_seconds)

        led_matrix.turn_off()
        led_matrix.use_pwm_mode()
        for b in range(0, 65536, gamma_table_size):
            led_matrix.set_matrix_brightness(b)
            time.sleep_ms(fade_step_length_ms)
        for b in range(65535, -1, -gamma_table_size):
            led_matrix.set_matrix_brightness(b)
            time.sleep_ms(fade_step_length_ms)

        led_matrix.use_digital_mode()
        led_matrix.turn_off()

except KeyboardInterrupt:
    led_matrix.use_digital_mode()
    led_matrix.turn_off()