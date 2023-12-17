import random

from info_panel.panel import Panel
from lib.colors.basic import Basic as BasicColors

class ISSPanel(Panel):
    UPDATE_INTERVAL = 2

    def __init__(self, x, y):
        super().__init__(x, y, BasicColors.palette())

    def __seed_randomly(self, color, percent=50):
        width = self._bitmap.width
        height = self._bitmap.height
        color_idx = self._palette.from_color(color)

        count = int(width * height * (percent/100))
        for _ in range(count):
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)
            self._bitmap[x,y] = color_idx

    def _update_display(self):
        self._clear(BasicColors.get("black"))

        color = BasicColors.get("random")
        self.__seed_randomly(color)
