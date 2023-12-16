from lib.dates import Dates
from lib.colors.color import Color
from lib.colors.color_factory import ColorFactory
from lib.colors.palette import Palette

class Holiday:
    BLACK = Color(0x000000, name="black")

    PIPER_BDAY = 126
    CRAIG_BDAY = 219
    CATE_BDAY = 823
    NATE_BDAY = 818
    PICASSO_BDAY = 1025

    CNC_ANNIV = 316

    NEWYEAR = 101
    VALENTINES = 214
    STPATTY = 317
    INDYPENDY = 704
    HALLOWEEN = 1031
    # Not *exactly* the correct day, but close enough :)
    THANKSGIVING = 1125
    CHRISTMAS_EVE = 1224
    CHRISTMAS = 1225

    HOLIDAYS = {
        "just_another_day": (
            ColorFactory.get("green"),
            ColorFactory.get("blue"),
            ColorFactory.get("yellow"),
            ColorFactory.get("white")
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
            Color(0xAF00FF, name="ny_purple"),
            Color(0x0096C8, name="ny_blue")
        ),
        "valentines": (
            ColorFactory.get("red"),
            ColorFactory.get("white"),
            Color(0xFF4545, name="vd_pink"),
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
            Color(0x28FF28, name="sp_green"),
            ColorFactory.get("white"),
            Color(0x5ecc09, name="sp_4")
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
            Color(0x4B96FF, name="cmas_blue")
        ),
    }

    HOLIDAY_MAP = {
        CRAIG_BDAY: "birthday",
        CATE_BDAY: "birthday",
        NATE_BDAY: "birthday",
        PIPER_BDAY: "birthday",
        PICASSO_BDAY: "picasso_bday",
        CNC_ANNIV: "birthday",
        NEWYEAR: "new_years",
        VALENTINES: "valentines",
        STPATTY: "st_patricks",
        INDYPENDY: "independence",
        HALLOWEEN: "halloween",
        THANKSGIVING: "thanksgiving",
        CHRISTMAS_EVE: "christmas",
        CHRISTMAS: "christmas",
    }

    @classmethod
    def palette(cls):
        colors = [cls.BLACK]

        for color_set in cls.HOLIDAYS.values():
            colors.extend([clr for clr in color_set])

        return Palette(colors)

    @classmethod
    def get(cls, name):
        if name == "current":
            colors = cls.get_current()
        else:
            colors = cls.HOLIDAYS.get(name)

        if colors is None:
            raise ValueError(f"Unknown Holiday: '{name}'")

        return colors

    @classmethod
    def get_current(cls):
        date_code = Dates.date_code()
        color_set = None

        name = cls.HOLIDAY_MAP.get(date_code, "just_another_day")
        if name is not None:
            color_set = cls.get(name)

        return color_set
