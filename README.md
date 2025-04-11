# pyworkshopsystem

### A micropython object model for the Music Thing Modular Workshop System Computer module.

This repo contains an object model for the Music Thing Modular Workshop 
System's Computer module. In abstracting away much of the micropython 
specifics, it aims to allow a user to interact directly with the components of 
the module (knobs, sockets, switches and LEDs) in software, and to connect 
them using a signals/slots API.

### Building the Package

The source code can be frozen into the micropython code within a .uf2 file, 
allowing for flashing of Computer modules with both micropython and
the extensions in the package. This process is not mature or well-tested,
so per-release, pre-built .uf2 files are provided in the release page of the 
git repo.

Building requires cmake and the appropriate GNU embedded toolchain. On MacOS
these can be installed using [homebrew](https://brew.sh/):

`brew install cmake`

and

`brew install gcc-arm-embedded`

The bash script `clone.sh` clones the micropython repo, and initializes the
submodules needed to build the rp2 port of micropython. The `build.sh` script
then builds the cross-compiler, the board/port submodules and finally the
`firmware.uf2` file, which is copied to the root dist directory. This file can
be copied to the RP2040 in the Computer module, with all Computer-specific
functionality then available via `import computer` in the `main.py` file running
on the RP2040.

## Helpful Links

[Micropython documentation](https://docs.micropython.org/en/latest/index.html)

[Micropython samples](https://github.com/peterhinch/micropython-samples/blob/master/encoders/encoder_portable.py)

[Micropython functionality specific to the RP2040](https://docs.micropython.org/en/latest/library/rp2.html)

[Micropython RP2xxx quick reference](https://docs.micropython.org/en/latest/rp2/quickref.html)

[RP2040 python datasheet](https://datasheets.raspberrypi.com/pico/raspberry-pi-pico-python-sdk.pdf)

[RP2040 Datasheet](https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf)

[pio examples](https://github.com/raspberrypi/pico-micropython-examples/tree/master/pio)

[Micropython SPI documentation](https://docs.micropython.org/en/latest/library/machine.SPI.html#machine-spi)