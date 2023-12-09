import time

import displayio

from lib.colors.color_factory import ColorFactory
from info_panel.glyph import Glyph

class Panel(displayio.Group):

    # Update interval
    UPDATE_INTERVAL = 5 * 60  # 5 mins

    def __init__(self, x, y, palette):
        super().__init__(x=x, y=y)

        self._palette = palette
        self._bitmap = displayio.Bitmap(16, 16, self._palette.num_colors)
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

    def _draw_number2(self, x, y, number, color, **kwargs):
        d1 = number // 10
        d2 = number % 10

        d1_color = color
        if d1 == 0 and not kwargs.get("leading_zero", False):
            d1_color = ColorFactory.get("black")

        digit = Glyph.get(d1)
        self._draw_alpha_num((0*digit.width)+x, y, digit, d1_color)

        digit = Glyph.get(d2)
        self._draw_alpha_num((1*digit.width)+x, y, digit, color)

    def _draw_number3(self, x, y, number, color):
        d0 = number // 100
        d1 = number // 10 if number < 100 else (number-100) // 10
        d2 = number % 10

        digit = Glyph.get(d0)
        self._draw_alpha_num((0*digit.width)+x, y, digit, color)

        digit = Glyph.get(d1)
        self._draw_alpha_num((1*digit.width)+x, y, digit, color)

        digit = Glyph.get(d2)
        self._draw_alpha_num((2*digit.width)+x, y, digit, color)

    def _draw_alpha_num(self, x, y, glyph, color):
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
