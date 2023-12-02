from lib.colors.color import Color
from lib.colors.palette import Palette

class Temperature:
    RANGES = (
        { "color": Color(0x000000, name="black"),       "range": range(0,0)    },
        { "color": Color(0xffffff, name="freezing"),    "range": range(0,26)   },
        { "color": Color(0x2222ff, name="really_cold"), "range": range(26,33)  },
        { "color": Color(0x0077ff, name="cold"),        "range": range(33,56)  },
        { "color": Color(0x04fbe8, name="cool"),        "range": range(56,65)  },
        { "color": Color(0x33e108, name="comfortable"), "range": range(65,76)  },
        { "color": Color(0xf9f504, name="warm"),        "range": range(76,86)  },
        { "color": Color(0xf97304, name="hot"),         "range": range(86,96)  },
        { "color": Color(0xff0000, name="really_hot"),  "range": range(96,200) }
    )

    @classmethod
    def palette(self):
        colors = [item["color"] for item in self.RANGES]
        return Palette(colors)

    @classmethod
    def from_temp(cls, temp):
        color = Color(0xffffff)

        for temp_range in cls.RANGES:
            if temp in temp_range["range"]:
                color = temp_range["color"]
                break

        return color
