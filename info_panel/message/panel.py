import math
import random

import info_panel.glyphs.alpha_num as alpha_num

from info_panel.panel import Panel
from lib.colors.holiday import Holiday as HolidayColors
from lib.colors.season import Season as SeasonColors
from lib.chronos import Chronos

class MessagePanel(Panel):
    UPDATE_INTERVAL = 15 * 60

    WIDTH = 48
    HEIGHT = 16
    GLYPH_W = alpha_num.WIDTH
    GLYPH_H = alpha_num.HEIGHT
    NUM_LINES = 2
    SPACING = 1
    # -2 -> 1 pixel on each side for the border
    MAX_LINE_LEN = WIDTH - 2

    def __init__(self, x, y):
        palette = HolidayColors.palette()
        palette.add_colors(SeasonColors.colors())
        super().__init__(
            x, y,
            palette,
            width=self.WIDTH, height=self.HEIGHT
        )

        self.__curr_msg = None

    def __truncate_line(self, line):
        new_line = line

        line_len = self._strlen(line, self.SPACING)
        if line_len > self.MAX_LINE_LEN:
            diff = (line_len - self.MAX_LINE_LEN) // (self.GLYPH_W + self.SPACING)
            # print(f"too long by: {diff}")
            diff = 2 if diff == 0 else diff
            new_line = line[0:-diff] + "•"

        return(new_line)

    def _update_display(self):
        color_set = HolidayColors.get("current")
        if not color_set:
            color_set = SeasonColors.get("current")

        msg = Chronos.motd()
        lines = []

        if msg != self.__curr_msg:
            self._clear(HolidayColors.BLACK)
            self.__curr_msg = msg

        clr_idx = random.randint(0,3)
        self._border(color_set[clr_idx])
        clr_idx += 1
        if clr_idx >= len(color_set):
            clr_idx = 0

        # Split onto multiple lines iff too long
        if self._strlen(msg, self.SPACING) > self.MAX_LINE_LEN:
            words = msg.split(" ")

            num_words = len(words)
            if num_words > 1:
                words_per_line = math.ceil(num_words / self.NUM_LINES)
                start_idx = 0
                end_idx = words_per_line
                for _ in range(self.NUM_LINES):
                    line = " ".join(words[start_idx:end_idx])
                    # print(f"Adding {line}")
                    lines.append(line)
                    start_idx = end_idx
                    end_idx += words_per_line
            else:
                lines.append(msg)
        else:
            lines.append(msg)

        # print(lines)

        for idx, line in enumerate(lines):
            msg_line = self.__truncate_line(line)
            msg_len = self._strlen(msg_line, self.SPACING)
            center = self._find_center(msg_len,0)
            x = center[0]
            y = 2 + (idx*self.GLYPH_H) + (idx*2)
            # print(f"msg_len: {msg_len}, x: {x}, y: {y}")
            self._draw_string(x, y, msg_line, color_set[clr_idx], spacing=self.SPACING)
            clr_idx += 1
            if clr_idx >= len(color_set):
                clr_idx = 0








#
