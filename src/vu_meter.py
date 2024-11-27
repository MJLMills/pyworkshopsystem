"""A VU meter class using the LED matrix.

The rwmodular vu_meter example implies the value of a reusable VU meter class.
which could have log and lin mappings.
Essentially has to map from a variable with a known range of values to an
integer value from 0 to the max resolution.

Can monitor 2 values with 4-bit resolution or
3 values with 3-bit resolution or
6 values with 2-bit (on/off) resolution.
Combinations are also possible but who knows how readable.

Can be used for progress bars without much effort (just pass increasing values in)
"""