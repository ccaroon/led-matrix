import displayio

class DebugPanel(displayio.Group):
    def __init__(self, x, y):
        super().__init__(x=x, y=y)

        self.__bitmap = displayio.Bitmap(16, 16, 2)
        palette = displayio.Palette(2)
        palette[0] = 0x000000
        palette[1] = 0xffffff

        grid = displayio.TileGrid(self.__bitmap, pixel_shader=palette)

        self.append(grid)

    @property
    def bitmap(self):
        return self.__bitmap

    def draw_glyph(self, x, y, glyph):
        for data in glyph:
            palette_idx = 1 if data["on"] else 0
            self.__bitmap[data["x"]+x,data["y"]+y] = palette_idx

    def update(self):
        pass
