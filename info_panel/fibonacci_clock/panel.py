import time
import random

from info_panel.panel import Panel
from lib.colors.holiday import Holiday as HolidayColors
from lib.colors.season import Season as SeasonColors


class FibonacciClock(Panel):
    UPDATE_INTERVAL = 60

    OFF = None
    ONE = "one"
    ONE_PRIME = "one-prime"
    TWO = "two"
    THREE = "three"
    FIVE = "five"

    # Location of the top-left corner of the clock
    LOCATION = (4, 5)

    # For each box...
    # ...the box size (size X size)
    # ...the offset from the top-left corner of clock
    BOX_INFO = {
        ONE: {
            "size": 1,
            "offset": (2, 0)
        },
        ONE_PRIME: {
            "size": 1,
            "offset": (2, 1)
        },
        TWO: {
            "size": 2,
            "offset": (0, 0)
        },
        THREE: {
            "size": 3,
            "offset": (0, 2)
        },
        FIVE: {
            "size": 5,
            "offset": (3, 0)
        }
    }

    NUMBER_MAP = (
        # ZERO => All lights off
        (
            (OFF, OFF, OFF, OFF, OFF),
        ),

        # ONE =>  1 | 1`
        (
            (ONE,       OFF, OFF, OFF, OFF),
            (ONE_PRIME, OFF, OFF, OFF, OFF),
        ),

        # TWO => 1,1` | 2
        (
            (ONE, ONE_PRIME, OFF, OFF, OFF),
            (TWO, OFF, OFF, OFF, OFF),
        ),

        # THREE => 1,2 | 1`,2 | 3
        (
            (ONE, TWO, OFF, OFF, OFF),
            (ONE_PRIME, TWO, OFF, OFF, OFF),
            (THREE, OFF, OFF, OFF, OFF),
        ),

        # FOUR => 1,3 | 1`,3 | 1,1`,2
        (
            (ONE, THREE, OFF, OFF, OFF),
            (ONE_PRIME, THREE, OFF, OFF, OFF),
            (ONE, ONE_PRIME, TWO, OFF, OFF),
        ),

        # FIVE => 1,1`,3 | 2,3 | 5
        (
            (ONE, ONE_PRIME, THREE, OFF, OFF),
            (TWO, THREE, OFF, OFF, OFF),
            (FIVE, OFF, OFF, OFF, OFF),
        ),

        # SIX =>  1,5 | 1`,5 | 1,2,3 | 1`,2,3
        (
            (ONE, FIVE, OFF, OFF, OFF),
            (ONE_PRIME, FIVE, OFF, OFF, OFF),
            (ONE, TWO, THREE, OFF, OFF),
            (ONE_PRIME, TWO, THREE, OFF, OFF),
        ),

        # SEVEN => 2,5 | 1,1`,2,3
        (
            (TWO, FIVE,      OFF, OFF,   OFF),
            (ONE, ONE_PRIME, TWO, THREE, OFF),
        ),

        # EIGHT => 3,5 | 1,2,5 | 1`,2,5
        (
            (THREE, FIVE, OFF, OFF, OFF),
            (ONE, TWO, FIVE, OFF, OFF),
            (ONE_PRIME, TWO, FIVE, OFF, OFF),
        ),

        # NINE => 1,1`,2,5 | 1,3,5 | 1`,3,5
        (
            (ONE, ONE_PRIME, TWO, FIVE, OFF),
            (ONE, THREE, FIVE, OFF, OFF),
            (ONE_PRIME, THREE, FIVE, OFF, OFF),
        ),

        # TEN => 2,3,5 | 1,1`,3,5
        (
            (TWO, THREE, FIVE, OFF, OFF),
            (ONE, ONE_PRIME, THREE, FIVE, OFF),
        ),

        # ELEVEN => 1,2,3,5 | 1`,2,3,5
        (
            (ONE, TWO, THREE, FIVE, OFF),
            (ONE_PRIME, TWO, THREE, FIVE, OFF),
        ),

        # TWELVE => 1,1`,2,3,5
        (
            (ONE, ONE_PRIME, TWO, THREE, FIVE),
        )
    )

    BLACK = SeasonColors.BLACK

    # What color to use from the chosen color_set for each part of the time
    COLOR_HOURS = 1
    COLOR_MINUTES = 2

    def __init__(self, x, y):
        palette = HolidayColors.palette()
        palette.add_colors(SeasonColors.colors())
        super().__init__(x, y, palette)

    def __number_to_boxes(self, number):
        choices = self.NUMBER_MAP[number]
        return random.choice(choices)

    def __draw_box(self, name, color):
        box = self.BOX_INFO[name]

        size = box["size"]
        offset = box["offset"]
        color_idx = self._palette.from_color(color)

        for col in range(size):
            for row in range(size):
                loc_x = self.LOCATION[0] + offset[0] + col
                loc_y = self.LOCATION[1] + offset[1] + row
                self._bitmap[loc_x, loc_y] = color_idx

    def _update_display(self):
        now = time.localtime()

        color_set = HolidayColors.get("current")
        if not color_set:
            color_set = SeasonColors.get("current")

        self._border(color_set[0])

        hour = now.tm_hour - 12 if now.tm_hour > 12 else now.tm_hour
        minutes = now.tm_min // 5

        # print(f"{hour:02}:{now.tm_min:02}")

        # Which boxes to turn on
        hour_boxes = self.__number_to_boxes(hour)
        min_boxes = self.__number_to_boxes(minutes)

        # What color each box should be:
        # 0 => OFF
        # 1 => hour color
        # 2 => min color
        # 3 => combo color
        box_colors = {
            self.ONE: 0,
            self.ONE_PRIME: 0,
            self.TWO: 0,
            self.THREE: 0,
            self.FIVE: 0
        }

        # Set box colors for hours
        for box in hour_boxes:
            if box is not self.OFF:
                box_colors[box] += self.COLOR_HOURS

        # Set/update box colors for minutes
        for box in min_boxes:
            if box is not self.OFF:
                box_colors[box] += self.COLOR_MINUTES

        for box_name, cs_idx in box_colors.items():
            color = self.BLACK if cs_idx == 0 else color_set[cs_idx]
            self.__draw_box(box_name, color)
