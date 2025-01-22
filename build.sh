git clone https://github.com/micropython/micropython.git
cd micropython
make -C mpy-cross
cd ports/rp2/
make submodules
make clean
make
# make BOARD=MYBOARD FROZEN_MANIFEST=./manifest.py
ls build-RPI_PICO/firmware.uf2
