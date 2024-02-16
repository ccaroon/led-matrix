import random

from info_panel.panel import Panel
# from info_panel.glyph import Glyph

from lib.colors.season import Season as SeasonColors

class DebugPanel(Panel):
    UPDATE_INTERVAL = 2.5 * 60

    def __init__(self, x, y):
        super().__init__(x, y, SeasonColors.palette())

        self.__colors = SeasonColors.get("current")
        self.__count = 0

    def _update_display(self):
        # print(f"Debugger -> {self.__count}")
        # msg = self.__count % 9999
        # self._draw_string(2, 5,
        #     f"{msg:04d}",
        #     self.__colors[0]
        # )
        # self.__count += 1
        # -----
        msgs = ["42", "7", "CNC", "C8", "KRG", "PY", "8"]
        x_pos = {
            1: 7,
            2: 4,
            3: 3
        }
        color_set = set(self.__colors)

        color1 = random.choice(list(color_set))
        color_set.discard(color1)
        self._border(color1)

        color2 = random.choice(list(color_set))
        msg = random.choice(msgs)

        # Clear Msg area
        self._draw_string(3, 5, " "*4, SeasonColors.BLACK)

        x = x_pos.get(len(msg), 3)
        self._draw_string(x, 5, msg, color2, spacing=1)
