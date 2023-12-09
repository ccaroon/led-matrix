import info_panel.glyphs.alpha as alpha
import info_panel.glyphs.digit as digit
import info_panel.glyphs.fancy_digit as fancy_digit

class Glyph:
    # data == [{"x", "y", "on"}]
    def __init__(self, data, width, height):
        self.__data = data
        self.width = width
        self.height = height

    def __iter__(self):
        return iter(self.__data)

    @classmethod
    def get(cls, name, set_hint=None):
        glyph_set = None
        glyph_name = str(name)

        # TODO: this is a hack...make it better
        if set_hint:
            if set_hint == "fancy_digit":
                glyph_set = fancy_digit
        else:
            if glyph_name in alpha.DATA.keys():
                glyph_set = alpha
            elif glyph_name in digit.DATA.keys():
                glyph_set = digit
            elif glyph_name in fancy_digit.DATA.keys():
                glyph_set = fancy_digit
            else:
                raise ValueError(f"Unknown Glyph Set: {name}")

        glyph_data = cls.__get_data(
            glyph_set.TEMPLATE,
            glyph_set.DATA.get(glyph_name)
        )
        glyph = Glyph(glyph_data, width=glyph_set.WIDTH, height=glyph_set.HEIGHT)

        return glyph

    @classmethod
    def __get_data(cls, template, pixels):
        data = []
        for idx, loc in enumerate(template):
            px_data = {
                "x": loc[1],
                "y": loc[0],
                "on":  True if pixels[idx] == 1 else False
            }

            data.append(px_data)

        return data
