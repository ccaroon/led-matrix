import time

from info_panel.panel import Panel
from lib.colors.season import Season as SeasonColors

class BinaryClock(Panel):
    UPDATE_INTERVAL = 1

    # As X,Y tuples
    HOUR_PIXELS = [
        (
            (4,6),
            (4,7),
            (4,8),
            (4,9)
        ),
        (
            (5,6),
            (5,7),
            (5,8),
            (5,9)
        )
    ]

    # As X,Y tuples
    MINUTE_PIXELS = [
        (
            (7,6),
            (7,7),
            (7,8),
            (7,9)
        ),
        (
            (8,6),
            (8,7),
            (8,8),
            (8,9)
        )
    ]

    # As X,Y tuples
    SECOND_PIXELS = [
        (
            (10,6),
            (10,7),
            (10,8),
            (10,9)
        ),
        (
            (11,6),
            (11,7),
            (11,8),
            (11,9)
        )
    ]

    def __init__(self, x, y):
        super().__init__(x, y, SeasonColors.palette())

        self.__color_set = SeasonColors.get("current")
        self._border(self.__color_set[3])

        self.__curr_hour = None
        self.__curr_min  = None

    def __set_number(self, number, pixel_set, on_color):
        # 1. split into digits
        d0 = int(number / 10)
        d1 = number % 10

        # 2. convert digit to binary string, zero-padded to 4 places
        d0_bin = "{:04b}".format(d0)
        d1_bin = "{:04b}".format(d1)

        # 3. display on matrix
        for digit, bin_str in enumerate((d0_bin, d1_bin)):
            for idx, bin_value in enumerate(bin_str):
                color = None
                if int(bin_value) == 0:
                    color = SeasonColors.BLACK
                else:
                    color = on_color

                x = pixel_set[digit][idx][0]
                y = pixel_set[digit][idx][1]
                self._bitmap[x,y] = self._palette.from_color(color)

    def _update_display(self):
        now = time.localtime()

        if now.tm_hour != self.__curr_hour:
            self.__curr_hour = now.tm_hour
            self.__set_number(now.tm_hour, self.HOUR_PIXELS,   self.__color_set[0])

        if now.tm_min != self.__curr_min:
            self.__curr_min = now.tm_min
            self.__set_number(now.tm_min,  self.MINUTE_PIXELS, self.__color_set[1])

        # Always update the seconds since UPDATE_INTERVAL is 1 sec anyway
        self.__set_number(now.tm_sec,  self.SECOND_PIXELS, self.__color_set[2])











#
