import displayio

# Tried to inherit from displayio.Palette, but kept getting error:
# FATAL: read zero bytes from port
# term_exitfunc: reset failed for dev UNKNOWN: Input/output error
#
# Instead wrapping displayio.Palette
class Palette():
    def __init__(self, colors:list):
        self.__num_colors = 0
        self.__all_colors = []
        self.__dio_palette = None
        self.__name_map = {}
        self.__value_map = {}

        self.add_colors(colors)

    @property
    def num_colors(self):
        return self.__num_colors

    @property
    def dio_palette(self):
        return self.__dio_palette

    def add_colors(self, colors):
        self.__all_colors.extend(colors)
        self.__num_colors = len(self.__all_colors)

        self.__dio_palette = displayio.Palette(self.__num_colors)

        self.__name_map = {}
        self.__value_map = {}
        for idx, color in enumerate(self.__all_colors):
            # Populate displayio.Pallete instance
            self.__dio_palette[idx] = color.value

            # "green" = 1
            self.__name_map[color.name] = idx

            # 0x00ff00 = 1
            self.__value_map[str(color)] = idx

    def from_name(self, name):
        return self.__name_map[name]

    def from_value(self, value):
        return self.__value_map[str(hex(value))]

    def from_color(self, color):
        # TODO: maybe by color.value instead?
        return self.__name_map[color.name]

    def __len__(self):
        return self.__num_colors
