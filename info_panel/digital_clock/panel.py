import time
from info_panel.panel import Panel

from info_panel.glyph import Glyph
from lib.colors.season import Season as SeasonColors

class DigitalClock(Panel):
    UPDATE_INTERVAL = 1

    def __init__(self, x, y):
        super().__init__(x, y, SeasonColors.palette())

        # TODO: Better way to get Glyph W & H
        number_w = 3 * 2

        self.__curr_hour = None
        self.__curr_min  = None
        self.__curr_ampm = None

        start_x = 0
        self.__pos = {
            "hour_x": start_x,
            "hour_y": 5,

            "min_x": start_x + number_w + 3,
            "min_y": 5,

            "sep_x": start_x + number_w + 1,
            "sep_y1": 5 + 1,
            "sep_y2": 5 + 3,
        }

    # TODO: optimize -> only change pixels that need to be changed
    def __border_seconds(self, secs, color_on, color_off):
        self._border(color_off)

        count = 0
        color_off_idx = self._palette.from_color(color_off)
        color_on_idx = self._palette.from_color(color_on)

        # Top | x = 0 -> 15
        for x in range(0, self._bitmap.width):
            self._bitmap[x,0] = color_on_idx if count <= secs else color_off_idx
            count += 1

        # Right | y = 1 -> 15
        for y in range(1, self._bitmap.height):
            self._bitmap[self._bitmap.width-1, y] = color_on_idx if count <= secs else color_off_idx
            count += 1

        # Bottom | x = 14 -> 0
        for x in range(self._bitmap.width-2, -1, -1):
            self._bitmap[x, self._bitmap.height-1] = color_on_idx if count <= secs else color_off_idx
            count += 1

        # Left | y = 14 -> 1
        for y in range(self._bitmap.height-2, 0, -1):
            self._bitmap[0, y] = color_on_idx if count <= secs else color_off_idx
            count += 1

    def __draw_am_pm(self, hour, color):
        if hour >= 12:
            self._draw_alpha_num(5, 10, Glyph.get("P"), color)
        else:
            self._draw_alpha_num(5, 10, Glyph.get("A"), color)

        self._draw_alpha_num(9, 10, Glyph.get("M"), color)

    def _update_display(self):
        now = time.localtime()
        color_set = SeasonColors.get_current()

        # Hour
        if now.tm_hour != self.__curr_hour:
            self.__curr_hour = now.tm_hour
            hour = now.tm_hour - 12 if now.tm_hour > 12 else now.tm_hour
            self._draw_number2(
                self.__pos["hour_x"], self.__pos["hour_y"],
                hour, color_set[0],
            )

        # Colon Separater - Blink on/off with seconds
        # 0 == Black
        color_idx = 0
        if now.tm_sec % 2 == 0:
            color_idx = self._palette.from_color(color_set[2])

        self._bitmap[self.__pos["sep_x"], self.__pos["sep_y1"]] = color_idx
        self._bitmap[self.__pos["sep_x"], self.__pos["sep_y2"]] = color_idx

        # Minutes
        if now.tm_min != self.__curr_min:
            self.__curr_min = now.tm_min
            self._draw_number2(
                self.__pos["min_x"], self.__pos["min_y"],
                now.tm_min, color_set[1],
                leading_zero=True
            )

        # Seconds (around border)
        self.__border_seconds(now.tm_sec, color_set[2], color_set[3])

        # AM/PM
        meridiem = "pm" if now.tm_hour >= 12 else "am"
        if meridiem != self.__curr_ampm:
            self.__curr_ampm = meridiem
            self.__draw_am_pm(now.tm_hour, color_set[3])









#
