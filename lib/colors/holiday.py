from lib.chronos import Chronos
from lib.colors.color import Color
from lib.colors.color_factory import ColorFactory
from lib.colors.palette import Palette

class Holiday:
    BLACK = Color(0x000000, name="black")

    PIPER_BDAY = 126
    CRAIG_BDAY = 219
    CATE_BDAY = 823
    NATE_BDAY = 818
    LINDA_BDAY = 111
    PICASSO_BDAY = 1025

    CNC_ANNIV = 316

    TEST_DAY = 000
    NEWYEAR = 101
    VALENTINES = 214
    STPATTY = 317
    INDYPENDY = 704
    HALLOWEEN = 1031
    # Not *exactly* the correct day, but close enough :)
    THANKSGIVING = 1125
    CHRISTMAS_EVE = 1224
    CHRISTMAS = 1225

    COLOR_SETS = {
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
            Color(0xFF69B4, name="vd_pink1"),
            Color(0xFF1493, name="vd_pink2"),
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
            Color(0x4682B4, name="steel_blue")
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
        TEST_DAY: "independence",
        CRAIG_BDAY: "birthday",
        CATE_BDAY: "birthday",
        NATE_BDAY: "birthday",
        PIPER_BDAY: "birthday",
        LINDA_BDAY: "birthday",
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
        return Palette(cls.colors())

    @classmethod
    def colors(cls):
        colors = [cls.BLACK]

        for color_set in cls.COLOR_SETS.values():
            colors.extend([clr for clr in color_set])

        return colors

    @classmethod
    def get(cls, name):
        """
        Get a color set by name.

        :param name: The name of the color set
        :return: Specified color set or None if it's not a known holiday.
        """
        if name == "current":
            colors = cls.get_current()
        else:
            colors = cls.COLOR_SETS.get(name)

        return colors

    @classmethod
    def get_current(cls):
        date_code = Chronos.date_code()
        color_set = None

        name = cls.HOLIDAY_MAP.get(date_code)
        if name is not None:
            color_set = cls.get(name)

        return color_set
