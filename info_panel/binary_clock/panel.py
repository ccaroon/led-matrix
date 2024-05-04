import time

from info_panel.panel import Panel
from lib.colors.holiday import Holiday as HolidayColors
from lib.colors.season import Season as SeasonColors

class BinaryClock(Panel):
    UPDATE_INTERVAL = 1

    # Pixel Locations - as X,Y tuples
    # Each X,Y represents the top-left corner of a 2x2 pixel
    # ...with 1 pixel width between each 2x2 block
    HOUR_PIXELS = [
        (
            (1,2),
            (1,5),
            (1,8),
            (1,11)
        ),
        (
            (3,2),
            (3,5),
            (3,8),
            (3,11)
        )
    ]

    MINUTE_PIXELS = [
        (
            (6,2),
            (6,5),
            (6,8),
            (6,11)
        ),
        (
            (8,2),
            (8,5),
            (8,8),
            (8,11)
        )
    ]

    SECOND_PIXELS = [
        (
            (11,2),
            (11,5),
            (11,8),
            (11,11)
        ),
        (
            (13,2),
            (13,5),
            (13,8),
            (13,11)
        )
    ]

    def __init__(self, x, y, scale=1):
        palette = HolidayColors.palette()
        palette.add_colors(SeasonColors.colors())
        super().__init__(x, y, palette, scale=scale)

        self.__curr_day  = None
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

                # Each "pixel" is a 2x2 set of pixels
                x = pixel_set[digit][idx][0]
                y = pixel_set[digit][idx][1]
                color_idx = self._palette.from_color(color)

                self._bitmap[x,   y]   = color_idx
                self._bitmap[x+1, y]   = color_idx
                self._bitmap[x,   y+1] = color_idx
                self._bitmap[x+1, y+1] = color_idx

    def _update_display(self):
        now = time.localtime()

        color_set = HolidayColors.get("current")
        if not color_set:
            color_set = SeasonColors.get("current")

        # Draw the border once a day in case the season changes
        # and it's color needs to be updated.
        if now.tm_mday != self.__curr_day:
            self.__curr_day = now.tm_mday
            self._border(color_set[3])

        if now.tm_hour != self.__curr_hour:
            self.__curr_hour = now.tm_hour
            self.__set_number(now.tm_hour, self.HOUR_PIXELS, color_set[0])

        if now.tm_min != self.__curr_min:
            self.__curr_min = now.tm_min
            self.__set_number(now.tm_min,  self.MINUTE_PIXELS, color_set[1])

        # Always update the seconds since UPDATE_INTERVAL is 1 sec anyway
        self.__set_number(now.tm_sec,  self.SECOND_PIXELS, color_set[2])











#
