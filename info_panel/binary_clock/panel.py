from info_panel.panel import Panel
from lib.colors.season import Season as SeasonColors

class BinaryClock(Panel):
    UPDATE_INTERVAL = 1

    def __init__(self, x, y):
        super().__init__(x, y, SeasonColors.palette())

    def _update_display(self):
        if self._bitmap[8,8] == 0:
            self._bitmap[8,8] = 1
        else:
            self._bitmap[8,8] = 0
