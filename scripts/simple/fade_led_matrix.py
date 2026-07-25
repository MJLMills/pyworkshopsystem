import time
from computer.leds.led_matrix import LEDMatrix


def main():
    matrix = LEDMatrix()
    matrix.use_pwm_mode()

    try:
        while True:
            for b in range(0, 65536, 256):
                matrix.set_matrix_brightness(b)
                time.sleep_ms(3)
            for b in range(65535, -1, -256):
                matrix.set_matrix_brightness(b)
                time.sleep_ms(3)
    except KeyboardInterrupt:
        matrix.set_matrix_brightness(0)
        matrix.use_digital_mode()


if __name__ == "__main__":
    main()
