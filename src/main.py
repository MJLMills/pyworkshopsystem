from computer import Computer

computer = Computer()

while True:
    computer.read_analog_inputs()
    print(computer.main_knob.ranged_variable.value >> 6)