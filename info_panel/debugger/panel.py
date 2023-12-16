from info_panel.panel import Panel
# from info_panel.glyph import Glyph

from lib.colors.season import Season as SeasonColors

class DebugPanel(Panel):
    UPDATE_INTERVAL = 1

    def __init__(self, x, y):
        super().__init__(x, y, SeasonColors.palette())

        self.__colors = SeasonColors.get("current")
        self.__count = 0

        self._border(self.__colors[3])

    def _update_display(self):
        # print(f"Debugger -> {self.__count}")
        msg = self.__count % 9999
        self._draw_string(2, 5,
            f"{msg:04d}",
            self.__colors[0]
        )
        self.__count += 1
