import time

from lib.colors.color_factory import ColorFactory
from info_panel.panel import Panel

import info_panel.moon.astro as astro

class MoonPanel(Panel):
    UPDATE_INTERVAL = 60 * 60

    def __init__(self, x, y, scale=1):
        self.__palette = ColorFactory.basic_palette()
        super().__init__(x, y, self.__palette, scale=scale)

        self._clear(ColorFactory.get("black"))
        self._border(ColorFactory.get("green"))

    def _update_display(self):
        now = time.localtime()
        moon_illum = astro.moon_illum(
            now.tm_year,
            now.tm_mon,
            now.tm_mday,
            now.tm_hour
        )
        print(f"[{moon_illum:.2f}] - {now.tm_year}/{now.tm_mon}/{now.tm_mday} @ {now.tm_hour}")
        self._draw_string(2, 5, f"{moon_illum:.1f}%", ColorFactory.get("white"))









#
