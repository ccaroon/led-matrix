import board
import displayio
import rgbmatrix
import framebufferio


class LEDMatrix:
    def __init__(self, base_width, base_height, tile_across=1, tile_down=1, bit_depth=6):
        self.__display = None

        width = base_width * tile_across
        height = base_height * tile_down

        self.__init_display(width, height, bit_depth, tile_down)

    def __init_display(self, width, height, bit_depth, tile_down):
        displayio.release_displays()

        addr_pins = [
            board.MTX_ADDRA,
            board.MTX_ADDRB,
            board.MTX_ADDRC,
            board.MTX_ADDRD
        ]

        if height // tile_down == 64:
            addr_pins.append(board.MTX_ADDRE)

        matrix = rgbmatrix.RGBMatrix(
            width=width, height=height, bit_depth=bit_depth,
            rgb_pins=[
                board.MTX_R1,
                board.MTX_G1,
                board.MTX_B1,
                board.MTX_R2,
                board.MTX_G2,
                board.MTX_B2
            ],
            addr_pins=addr_pins,
            clock_pin=board.MTX_CLK,
            latch_pin=board.MTX_LAT,
            output_enable_pin=board.MTX_OE,
            tile=tile_down
        )
        self.__display = framebufferio.FramebufferDisplay(matrix)

    @property
    def display(self):
        return self.__display

    @property
    def width(self):
        return self.__display.width

    @property
    def height(self):
        return self.__display.height
