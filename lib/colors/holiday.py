from machine import RTC

from lib.colors.color import Color
from lib.colors.color_factory import ColorFactory

class Holiday:
    __RTC = RTC()

    TODAY = 0

    PIPER_BDAY = 126
    CRAIG_BDAY = 219
    CATE_BDAY = 823
    NATE_BDAY = 818
    PICASSO_BDAY = 1025

    NEWYEAR = 101
    VALENTINES = 214
    STPATTY = 317
    INDYPENDY = 704
    HALLOWEEN = 1031
    # Not *exactly* the correct day, but close enough :)
    THANKSGIVING = 1125
    CHRISTMAS = 1225

    HOLIDAYS = {
        # For Testing Purposes
        "test_set": (
            ColorFactory.hex("0xFF0000"),
            ColorFactory.hex("0x00FF00"),
            ColorFactory.hex("0x0000FF"),
            ColorFactory.hex("0xFFFFFF")
        ),
        "picasso_bday": (
            ColorFactory.get("red"),
            ColorFactory.get("blue"),
            ColorFactory.get("yellow"),
            ColorFactory.get("white")
        ),
        "new_years": (
            ColorFactory.get("white"),
            ColorFactory.get("yellow"),
            ColorFactory.hex("0xAF00FF"), # purple
            ColorFactory.hex("0x0096C8")  # blue
        ),
        "valentines": (
            ColorFactory.get("red"),
            ColorFactory.get("white"),
            ColorFactory.hex("0xFF4545"), # pink
            ColorFactory.get("black")
        ),
        "birthday": (
            ColorFactory.get("green"),
            ColorFactory.get("violet"),
            ColorFactory.get("yellow"),
            ColorFactory.get("blue")
        ),
        "st_patricks": (
            ColorFactory.get("green"),
            ColorFactory.hex("0x28FF28"), # light-green
            ColorFactory.get("white"),
            ColorFactory.hex("0x5ecc09")
        ),
        "independence": (
            ColorFactory.get("red"),
            ColorFactory.get("white"),
            ColorFactory.get("blue"),
            ColorFactory.get("black")
        ),
        "halloween": (
            ColorFactory.get("orange"),
            ColorFactory.get("violet"),
            ColorFactory.get("green"),
            ColorFactory.get("white")
        ),
        "thanksgiving": (
            ColorFactory.get("red"),
            ColorFactory.get("yellow"),
            ColorFactory.get("orange"),
            ColorFactory.get("white")
        ),
        "christmas": (
            ColorFactory.get("white"),
            ColorFactory.get("green"),
            ColorFactory.get("red"),
            ColorFactory.hex("0x4B96FF")  # light-blue
        ),
    }

    HOLIDAY_MAP = {
        TODAY: "test_set",
        CRAIG_BDAY: "birthday",
        CATE_BDAY: "birthday",
        NATE_BDAY: "birthday",
        PIPER_BDAY: "birthday",
        PICASSO_BDAY: "picasso_bday",
        NEWYEAR: "new_years",
        VALENTINES: "valentines",
        STPATTY: "st_patricks",
        INDYPENDY: "independence",
        HALLOWEEN: "halloween",
        THANKSGIVING: "thanksgiving",
        CHRISTMAS: "christmas"
    }

    @classmethod
    def get(cls, name, brightness=Color.DEFAULT_BRIGHTNESS):
        if name == "current":
            colors = cls.get_current(brightness)
        else:
            colors = cls.HOLIDAYS.get(name)
            if colors is None:
                raise ValueError("Unknown Holiday: '%s'" % name)

        if colors is not None:
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

        name = cls.HOLIDAY_MAP.get(date_code, None)
        if name is not None:
            color_set = cls.get(name, brightness)

        return color_set
