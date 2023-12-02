from machine import RTC

from lib.colors.color import Color
from lib.colors.color_factory import ColorFactory

class Season:
    __RTC = RTC()

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
            ColorFactory.hex("0x00FF19"), # green
            ColorFactory.hex("0xFF0096"), # pink
            ColorFactory.hex("0x2800FF"), # blue
            ColorFactory.get("white")
        ),
        "summer": (
            ColorFactory.get("yellow"),
            ColorFactory.hex("0x3232FF"), # blue
            ColorFactory.get("green"),
            ColorFactory.get("indigo")
        ),
        "fall": (
            ColorFactory.get("red"),
            ColorFactory.hex("0xF0FF00"), # yellow
            ColorFactory.hex("0xFF6400"), # orange
            ColorFactory.hex("0x3d3202"), # dirty-yellow-orange'ish
        ),
        "winter": (
            ColorFactory.get("white"),
            ColorFactory.hex("0x0080FF"), # blue'ish
            ColorFactory.get("cyan"),
            ColorFactory.hex("0x7f74ff") # grey'ish
        )
    }

    @classmethod
    def get(cls, name, brightness=Color.DEFAULT_BRIGHTNESS):
        if name == "current":
            colors = cls.get_current(brightness)
        else:
            colors = cls.SEASONS.get(name)

        if colors is None:
            raise ValueError("Unknown Season: '%d'" % name)

        for color in colors:
            color.brightness = brightness

        return colors

    @classmethod
    def get_current(cls, brightness=Color.DEFAULT_BRIGHTNESS):
        # date == year, month, day, weekday, hour, minute, second, microsecond
        now = cls.__RTC.datetime()
        month = now[1]
        day = now[2]
        date_code = (month * 100) + day

        color_set = None
        # Pick Color for Season
        if date_code >= cls.START_OF_SPRING and date_code < cls.START_OF_SUMMER:
            color_set = cls.get("spring", brightness)
        elif date_code >= cls.START_OF_SUMMER and date_code < cls.START_OF_FALL:
            color_set = cls.get("summer", brightness)
        elif date_code >= cls.START_OF_FALL and date_code < cls.START_OF_WINTER:
            color_set = cls.get("fall", brightness)
        elif date_code >= cls.START_OF_WINTER or date_code < cls.START_OF_SPRING:
            color_set = cls.get("winter", brightness)

        return color_set
