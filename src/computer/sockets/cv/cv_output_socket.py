from src.computer.sockets import OutputSocket

class CVOutputSocket(OutputSocket):
    """
    Inverted PWM output.
    Two-pole active filtered. Use 11-bit PWM at 60 kHz.
    2047 = -6V
    1024 = 0V
    0 = +6V
    Requires firmware calibration for precise values.
    """
    ...


class CVOutputSocketOne(OutputSocket):
    PIN_ID = 22
    ...


class CVOutputSocketTwo(OutputSocket):
    PIN_ID = 23
    ...
