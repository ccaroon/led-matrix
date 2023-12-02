import random
from lib.colors.color import Color

class ColorFactory:
    COLORS = {
        # b&w
        "black": Color(0,0,0),
        "white": Color(255,255,255),
        "white_rgbw": Color(0,0,0,255),

        # rainbow
        "red": Color(255,0,0),
        "orange": Color(255,128,0),
        "yellow": Color(255,255,0),
        "green": Color(0,255,0),
        "blue": Color(0,0,255),
        "indigo": Color(75,0,255),
        "violet": Color(128,0,255),

        # other
        "cyan": Color(0,255,128),
        "purple": Color(255,0,255),
        "pink": Color(255,1,80)
    }

    SETS = {
        "rgb": (
            COLORS["red"],
            COLORS["green"],
            COLORS["blue"],
            COLORS["black"]
        ),
        "Y+B=G": (
            COLORS["yellow"],
            COLORS["blue"],
            COLORS["green"],
            COLORS["black"]
        )
    }

    @classmethod
    def get(cls, name):

        if name.startswith("0x"):
            color = cls.hex(name)
        else:
            color = cls.COLORS.get(name)

        if color is None:
            raise ValueError("Unknown Color: '%s'" % name)

        return color

    @classmethod
    def random(cls, count=1):
        color_set = []
        for _ in range(count):
            red = random.randint(0,255)
            green = random.randint(0,255)
            blue = random.randint(0,255)

            color_set.append(Color(red, green, blue))

        return color_set[0] if len(color_set) == 1 else color_set

    @classmethod
    def get_set(cls, name):
        color_set = cls.SETS.get(name)
        if color_set is None:
            raise ValueError("Unknown Color Set: '%d'" % name)

        return color_set

    # @classmethod
    # def hex(self, hex_str):
    #     if hex_str.startswith("0x"):
    #         red = int(hex_str[2:4], 16)
    #         green = int(hex_str[4:6], 16)
    #         blue= int(hex_str[6:8], 16)
    #     else:
    #         raise ValueError("'%s' does not appear to be a HEX number")

    #     return Color(red, green, blue)






















#
