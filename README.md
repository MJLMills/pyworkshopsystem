# pyworkshopsystem

### A micropython object model for the Music Thing Modular Workshop System Computer module.

This repo contains an initial attempt at an object model for the
Music Thing Modular Workshop System's Computer module. In abstracting 
away much of the micropython specifics, it aims to allow a user to 
interact directly with the components of the module (knobs, sockets, 
switches and LEDs) in software.

This is a first attempt based on the supplied documentation without the benefit
of access to a working system for testing and mainly contains the beginnings of
various class definitions, along with some functionality inspired by the [rwmodular
computer repo](https://github.com/rwmodular/computer/tree/main). When this repo was started, the author had not seen the existing
code in the [Hello_Computer repo](https://github.com/TomWhitwell/Hello_Computer/tree/main/Demonstrations%2BHelloWorlds/Micropython)
working towards similar ends.


## Helpful Links

[Micropython documentation](https://docs.micropython.org/en/latest/index.html)

[Micropython functionality specific to the RP2040](https://docs.micropython.org/en/latest/library/rp2.html)

[RP2040 python datasheet](https://datasheets.raspberrypi.com/pico/raspberry-pi-pico-python-sdk.pdf)

[pio examples](https://github.com/raspberrypi/pico-micropython-examples/tree/master/pio)

