git clone --depth 1 --branch v1.24.1 https://github.com/micropython/micropython
cd micropython
git submodule update --init lib/pico-sdk lib/tinyusb lib/mbedtls lib/micropython-lib
