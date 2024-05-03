# Adafruit MatrixPortal S3 with ESP32S3
LED Matrix Driver Board

## Links
* Board: https://www.adafruit.com/product/5778
* Tutorial: https://learn.adafruit.com/adafruit-matrixportal-s3
* Bootloader Repair: https://learn.adafruit.com/adafruit-matrixportal-s3/factory-reset#factory-reset-and-bootloader-repair-3107941
* Python: https://circuitpython.org/board/adafruit_matrixportal_s3/

## Info
* Port: /dev/ttyACM0

## Hardware
* ESP32-S3 with 3.3v logic/power.
  - It has 8MB of Flash and 2MB of RAM.
* LIS3DH Triple-Axis Accelerometer
  - The accelerometer is connected via the I2C bus.
  - Please note the address of the accelerometer is 0x19 not 0x18 which is the default in our libraries
* RGB status NeoPixel labeled "STATUS". It is connected to `board.NEOPIXEL` or Arduino 4
* D13 LED. This is attached to `board.LED` and Arduino 13.
* UP button is attached to `board.BUTTON_UP` and Arduino 6.
* Down button is attached to `board.BUTTON_DOWN` and Arduino 7.
* NOTE: buttons do not have any pull-up resistors connect; pressing either of them pulls the input low.

## Init Board
### Enter ROM bootloader mode
Entering the ROM bootloader is easy. Complete the following steps.

Before you start, make sure your ESP32-S2/S3 is plugged into USB port to your computer using a data/sync cable. Charge-only cables will not work!

1. Press and hold the BOOT/DFU button down. Don't let go of it yet!
2. Press and release the Reset button. You should still have the BOOT/DFU button pressed while you do this.
3. Now you can release the BOOT/DFU button.

No USB drive will appear when you've entered the ROM bootloader. This is normal!

### Repair UF2 Bootloader
1. Test:  `esptool.py --port /dev/PORT chip_id`
2. Erase: `esptool.py --port /dev/PORT erase_flash`
3. Flash: `esptool.py --port /dev/PORT write_flash 0x0 firmware/MatrixPortal_S3_FactoryReset.bin`
4. Reset: Push the reset button

### Install CircuitPython
1. UF2 Mode:
  - Click the Reset button on your board.
  - When you see the NeoPixel RGB LED turn purple, press it again.
  - At that point, the NeoPixel should turn green. If it turns red, check the USB cable, try another USB port, etc.
  - A Drive named "MATRXS3BOOT" should appear.
2. Drag the UF2 installer file onto the "MATRXS3BOOT" drive
3. The LED will flash for a bit & the "MATRXS3BOOT" drive will disappear
4. A drive named "CIRCUITPYTHON" should appear.
5. Done.

## Development
* PortalBase: https://docs.circuitpython.org/projects/portalbase/en/latest/index.html
* MatrixPortal: https://docs.circuitpython.org/projects/matrixportal/en/latest/
* DisplayIO:
  - https://docs.circuitpython.org/en/latest/shared-bindings/displayio/
  - https://learn.adafruit.com/circuitpython-display-support-using-displayio
* Matrices with CPy: https://learn.adafruit.com/rgb-led-matrices-matrix-panels-with-circuitpython
* Chaining: https://learn.adafruit.com/rgb-led-matrices-matrix-panels-with-circuitpython/advanced-multiple-panels









.
