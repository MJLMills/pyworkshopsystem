## Analog Inputs

The following analog inputs are present on the Music Thing Modular Workshop System Computer:

* CV/Audio Input 1
* CV/Audio Input 2
* Main Knob
* X Knob
* Y Knob
* Z Switch
* CV/Input 1
* CV/Input 2

The RP2040 microprocessor has an integrated 12-bit analog-to-digital (ADC) converter with four 
channels (indexed 0 to 3) routed to GPIO pins 26, 27, 28, and 29. In the Computer, the first two ADC 
channels (0 and 1, GPIO pins 26 and 27) are each connected directly to a CV/Audio input. This avoids the 
multiplexer overhead described below, allowing the fastest possible read speeds for audio input.

The remaining six inputs are connected to ADC channels 2 and 3 via a 4052 2 x 4 multiplexer.
GPIO pins 28 (ADC channel 2) and 29 (ADC channel 3) are connected to each of the multiplexer's outputs.
In addition, two digital output pins (GPIO 24 and 25) are connected to the multiplexer, and their values are set in order to select
which of the four inputs are connected to each output according to the following table.

| GPIO Pin | Digital Output A (GPIO 24) | Digital Output B (GPIO 25) | Analog Input |
|----------|----------------------------|----------------------------|--------------|
| 28       | 0                          | 0                          | Main Knob    |
|          | 0                          | 1                          | X Knob       |
|          | 1                          | 0                          | Y Knob       |
|          | 1                          | 1                          | Z Switch     |
| 29       | 0                          | 0                          | CV Input 1   |
|          | 0                          | 1                          | CV Input 2   |
|          | 1                          | 0                          | CV Input 1   |
|          | 1                          | 1                          | CV Input 2   |

The use of the multiplexer allows more inputs to be connected to the four channels of the RP2040's onboard ADC, with the
added cost of switching digital pins in order to read the values of those inputs. Managing these pins efficiently 
requires careful implementation.

A `micropython` ADC object must be created for each pin of the ADC in order to 
read values from the analog inputs via the `read_u16` method.


The following is suggested code for speeding up scaling the inputs
between the measured min and max values of a potentiometer.

```python

from machine import ADC, Pin

pot = ADC(Pin(26))
read_adc = pot.read_u16

MIN_RAW = 224
INPUT_SPAN = 65535 - MIN_RAW  # 65311

# Pre-calculate the exact scaling multiplier shifted by 16 bits
# (65535 << 16) // 65311 = 65759
SCALE_U16 = (65535 << 16) // INPUT_SPAN

@micropython.native
def get_clean_u16() -> int:
    raw = read_adc()
    
    if raw <= MIN_RAW:
        return 0
        
    # Subtract offset and scale up to stretch the range back to exactly 65535
    val = ((raw - MIN_RAW) * SCALE_U16) >> 16
    
    # Cap any slight noise overflow at the true 16-bit ceiling
    if val > 65535:
        return 65535
    return val

# Execution loop
while True:
    clean_value = get_clean_u16()  # This sits perfectly at 0 to 65535
```

Here's fast, branchless software window for accepting a specified 
voltage range at the CV inputs:

```python
from machine import ADC, Pin

# Setup hardware
cv_input = ADC(Pin(26))
read_adc = cv_input.read_u16

# 1. Base hardware calibration bounds (Your -5V to +5V scale)
HW_MIN = 224
HW_MAX = 65535

# 2. Define your desired software acceptance window
# Example: Only accept CV inputs from -2.0V to +3.5V
# Map your desired physical voltages proportionally to the 0-65535 scale:
WINDOW_MIN = 15000  # Corresponds to your desired minimum voltage cutoff
WINDOW_MAX = 55000  # Corresponds to your desired maximum voltage cutoff

# 3. Pre-calculate fixed-point span multipliers
WINDOW_SPAN = WINDOW_MAX - WINDOW_MIN
SCALE_U16 = (65535 << 16) // WINDOW_SPAN

@micropython.native
def get_windowed_cv() -> int:
    raw = read_adc()
    
    # Fast clamping to your specified minimum and maximum windows
    if raw <= WINDOW_MIN:
        return 0
    elif raw >= WINDOW_MAX:
        return 65535
        
    # Rescale the remaining window data into a full 16-bit application sweep
    return ((raw - WINDOW_MIN) * SCALE_U16) >> 16

# Execution loop
while True:
    cv_value = get_windowed_cv()  # Sweeps 0 to 65535 strictly within your window

```