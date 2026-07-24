import time
from computer import Computer

computer = Computer()
led_matrix = computer.led_matrix
led_matrix.turn_off()

led_one = led_matrix.get_by_index(1)
led_two = led_matrix.get_by_index(2)
led_three = led_matrix.get_by_index(3)
led_four = led_matrix.get_by_index(4)
led_five = led_matrix.get_by_index(5)
led_six = led_matrix.get_by_index(6)

sleep_time_seconds = 0.2
sleep = time.sleep

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
