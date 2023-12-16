import time

import displayio

# from lib.colors.color_factory import ColorFactory
from info_panel.glyph import Glyph

class Panel(displayio.Group):

    # Update interval
    UPDATE_INTERVAL = 5 * 60  # 5 mins

    def __init__(self, x, y, palette, width=16, height=16):
        super().__init__(x=x, y=y)

        self._palette = palette
        self._bitmap = displayio.Bitmap(width, height, self._palette.num_colors)
        grid = displayio.TileGrid(
            self._bitmap,
            pixel_shader=self._palette.dio_palette
        )
        self.append(grid)
        self.__last_update = 0

    def _border(self, color):
        color_idx = self._palette.from_color(color)
        # Top/Bottom
        for x in range(0, self._bitmap.width):
            self._bitmap[x,0] = color_idx
            self._bitmap[x, self._bitmap.height-1] = color_idx

        # Left/Right
        for y in range(0, self._bitmap.height):
            self._bitmap[0, y] = color_idx
            self._bitmap[self._bitmap.width-1, y] = color_idx

    # d1_color = color
    # if d1 == 0 and not kwargs.get("leading_zero", False):
    #     d1_color = ColorFactory.get("black")
    def _draw_string(self, x, y, msg, color, **kwargs):
        chars = list(str(msg))
        spacing = kwargs.get("spacing", 0)
        for idx, char in enumerate(chars):
            glyph = Glyph.get(char)
            # TODO: don't space a space
            if char is "-":
                dx = x + (idx * glyph.width)
            else:
                dx = x + (idx * glyph.width) + (spacing * idx)
            self._draw_glyph(dx, y, glyph, color)

    def _draw_glyph(self, x, y, glyph, color):
        color_idx = self._palette.from_color(color)
        for data in glyph:
            palette_idx = color_idx if data["on"] else 0
            self._bitmap[data["x"]+x, data["y"]+y] = palette_idx

    def _update_display(self):
        raise NotImplementedError("Subclasses Must Implement")

    def update(self):
        now = time.time()
        if now - self.__last_update >= self.UPDATE_INTERVAL:
            self.__last_update = now
            self._update_display()
