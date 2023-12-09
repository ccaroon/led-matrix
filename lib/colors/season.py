import time

from lib.colors.color import Color
from lib.colors.color_factory import ColorFactory
from lib.colors.palette import Palette

class Season:
    BLACK = Color(0x000000, name="black")
    # Spring: 3-20  to 6-20   => 320 to 620
    # Summer: 6-21  to 9-21   => 621 to 921
    # Fall:   9-22  to 12-20  => 922 to 1220
    # Winter: 12-21 to 3-19   => 1221 to 319
    START_OF_SPRING =  320
    START_OF_SUMMER =  621
    START_OF_FALL   =  922
    START_OF_WINTER =  1221

    SEASONS = {
        "spring": (
            Color(0x00FF19, name="spring1"), # green
            Color(0xFF0096, name="spring2"), # pink
            Color(0x2800FF, name="spring3"), # blue
            Color(0x555555, name="spring4"), # dim white
        ),
        "summer": (
            ColorFactory.get("yellow"),
            Color(0x3232FF, name="summer2"), # blue
            ColorFactory.get("green"),
            ColorFactory.get("indigo")
        ),
        "fall": (
            ColorFactory.get("red"),
            Color(0xF0FF00, name="fall2"), # yellow
            Color(0xFF6400, name="fall3"), # orange
            # Color(0x3d3202, name="fall4"), # dirty-yellow-orange'ish
            Color(0x555555, name="fall4"), # dirty-yellow-orange'ish
        ),
        "winter": (
            ColorFactory.get("white"),
            Color(0x0080FF, name="winter2"), # blue'ish
            ColorFactory.get("cyan"),
            Color(0x7f74ff, name="winter4") # grey'ish
        )
    }

    @classmethod
    def palette(cls):
        colors = [cls.BLACK]
        colors.extend([clr for clr in cls.SEASONS["spring"]])
        colors.extend([clr for clr in cls.SEASONS["summer"]])
        colors.extend([clr for clr in cls.SEASONS["fall"]])
        colors.extend([clr for clr in cls.SEASONS["winter"]])
        return Palette(colors)

    @classmethod
    def get(cls, name):
        if name == "current":
            colors = cls.get_current()
        else:
            colors = cls.SEASONS.get(name)

        if colors is None:
            raise ValueError("Unknown Season: '%d'" % name)

        return colors

    @classmethod
    def get_current(cls):
        now = time.localtime()
        month = now.tm_mon
        day = now.tm_mday
        date_code = (month * 100) + day

        color_set = None
        # Pick Color for Season
        if date_code >= cls.START_OF_SPRING and date_code < cls.START_OF_SUMMER:
            color_set = cls.get("spring")
        elif date_code >= cls.START_OF_SUMMER and date_code < cls.START_OF_FALL:
            color_set = cls.get("summer")
        elif date_code >= cls.START_OF_FALL and date_code < cls.START_OF_WINTER:
            color_set = cls.get("fall")
        elif date_code >= cls.START_OF_WINTER or date_code < cls.START_OF_SPRING:
            color_set = cls.get("winter")

        return color_set
