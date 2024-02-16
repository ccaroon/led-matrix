class Color:
    ORDER = ("R", "G", "B")
    def __init__(self, value, name=None):
        if isinstance(value, tuple):
            self.__tuple2rgb(value)
        elif isinstance(value, int):
            self.__int2rgb(value)
        else:
            raise TypeError(f"Unrecognized type for color data: {type(value)} ")

        self.__value = self.__red << 16 | self.__green << 8 | self.__blue
        self.name = str(hex(self.__value)) if name is None else name

    @property
    def value(self):
        return self.__value

    def __eq__(self, value):
        return self.__value == value

    def __str__(self) -> str:
        return str(hex(self.__value))

    def __hash__(self) -> int:
        return self.__value

    def __int2rgb(self, value):
        # 0xLLMMRR
        v_left = value >> 16
        v_mid = (value & 0x00ff00) >> 8
        v_rght = value & 0x0000ff

        rgb = {}
        rgb[self.ORDER[0]] = v_left
        rgb[self.ORDER[1]] = v_mid
        rgb[self.ORDER[2]] = v_rght

        self.__red = rgb["R"]
        self.__green = rgb["G"]
        self.__blue = rgb["B"]

    def __tuple2rgb(self, color):
        r_idx = self.ORDER.index("R")
        self.__red = color[r_idx]

        g_idx = self.ORDER.index("G")
        self.__green = color[g_idx]

        b_idx = self.ORDER.index("B")
        self.__blue = color[b_idx]
