import random
from lib.colors.color import Color
from lib.colors.color_factory import ColorFactory
from lib.colors.palette import Palette

class Basic:
    COLORS = {
        "aqua": Color((0,255,255), name="aqua")
    }
    COLORS.update(ColorFactory.COLORS)

    @classmethod
    def palette(cls):
        return Palette(cls.colors())

    @classmethod
    def colors(cls):
        colors = [clr for clr in cls.COLORS.values()]
        colors.insert(0, ColorFactory.get("black"))
        return colors

    @classmethod
    def get(cls, name):
        if name == "random":
            color = random.choice(list(cls.COLORS.values()))
        else:
            color = cls.COLORS.get(name)

        if color is None:
            raise ValueError(f"Unknown Color: '{name}'")

        return color
