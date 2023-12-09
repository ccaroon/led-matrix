# import random
from lib.colors.color import Color

class ColorFactory:
    COLORS = {
        # b&w
        "black": Color((0,0,0), name="black"),
        "white": Color((255,255,255), name="white"),

        # rainbow
        "red": Color((255,0,0), name="red"),
        "orange": Color((255,128,0), name="orange"),
        "yellow": Color((255,255,0), name="yellow"),
        "green": Color((0,255,0), name="green"),
        "blue": Color((0,0,255), name="blue"),
        "indigo": Color((75,0,255), name="indigo"),
        "violet": Color((128,0,255), name="violet"),

        # other
        "cyan": Color((0,255,128), name="cyan"),
        "purple": Color((255,0,255), name="purple"),
        "pink": Color((255,1,80), name="pink")
    }

    @classmethod
    def get(cls, name):
        color = cls.COLORS.get(name)
        if color is None:
            raise ValueError("Unknown Color: '%s'" % name)

        return color

    # @classmethod
    # def random(cls, count=1):
    #     color_set = []
    #     for _ in range(count):
    #         red = random.randint(0,255)
    #         green = random.randint(0,255)
    #         blue = random.randint(0,255)

    #         color_set.append(Color(red, green, blue))

    #     return color_set[0] if len(color_set) == 1 else color_set
