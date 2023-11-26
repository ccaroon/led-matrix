import displayio

class BinaryClock(displayio.Group):
    def __init__(self, x, y):
        super().__init__(x=x, y=y)

        self.__bitmap = displayio.Bitmap(16, 16, 2)
        palette = displayio.Palette(2)
        palette[0] = 0x000000
        palette[1] = 0x00ff00

        grid = displayio.TileGrid(self.__bitmap, pixel_shader=palette)

        self.append(grid)

    def update(self):
        if self.__bitmap[8,8] == 0:
            self.__bitmap[8,8] = 1
        else:
            self.__bitmap[8,8] = 0
