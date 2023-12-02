import time
import displayio
import os

from lib.colors.color import Color
# **MUST** set the ORDER (iff not normal) before importing other Color classes
Color.ORDER = ("R", "B", "G")
from lib.colors.temperature import Temperature
from info_panel.glyph import Glyph

from my_wifi import MyWiFi
from aio import AdafruitIO

# TODO:
# * [ ] old data
# * [ ] data retrieval error
# * [ ] humidity
# -----------------------------------------------------------------------------
class Reading:
    name = None
    value = None
    age = None
    def __init__(self, name, value, age):
        self.name = name
        self.value = value
        self.age = age

    def __repr__(self):
        return (self.name, self.value, self.age)

    def __str__(self):
        return f"{self.name}: {self.value} ({self.age} sec)"
# -----------------------------------------------------------------------------
class WeatherPanel(displayio.Group):

    # Update interval
    INTERVAL = 5 * 60

    def __init__(self, x, y):
        super().__init__(x=x, y=y)

        self.__palette = Temperature.palette()
        self.__bitmap = displayio.Bitmap(16, 16, self.__palette.num_colors)
        grid = displayio.TileGrid(
            self.__bitmap,
            pixel_shader=self.__palette.dio_palette
        )
        self.append(grid)

        self.__last_update = 0
        self.__aio = AdafruitIO(
            MyWiFi.REQUESTS,
            "weather-station",
            { "username": os.getenv("aio.username"), "key": os.getenv("aio.key")}
        )

    def __border(self, color):
        color_idx = self.__palette.from_color(color)
        # Top/Bottom
        for x in range(0, self.__bitmap.width):
            self.__bitmap[x,0] = color_idx
            self.__bitmap[x, self.__bitmap.height-1] = color_idx

        # Left/Right
        for y in range(0, self.__bitmap.height):
            self.__bitmap[0, y] = color_idx
            self.__bitmap[self.__bitmap.width-1, y] = color_idx

    def __get_data(self, name):
        resp = self.__aio.get_data(name)
        data = None
        if resp["success"]:
            data = Reading(
                name,
                int(resp["results"][0]["value"]),
                resp["age"]
            )
        return data

    def __display_number2(self, x, y, number, color):
        d1 = number // 10
        d2 = number % 10

        digit = Glyph.get(d1)
        self.__draw_digit((0*digit.width)+x, y, digit, color)

        digit = Glyph.get(d2)
        self.__draw_digit((1*digit.width)+x, y, digit, color)

    # def __display_number3(self, x, y, number, color):
    #     d0 = number // 100
    #     d1 = number // 10 if number < 100 else (number-100) // 10
    #     d2 = number % 10

    #     if number >= 100:
    #         digit = Glyph.get(d0)
    #         self.__draw_digit((0*digit.width)+x, y, digit, color)

    #     if number >= 10:
    #         digit = Glyph.get(d1)
    #         self.__draw_digit((1*digit.width)+x, y, digit, color)

    #     if number >= 0:
    #         digit = Glyph.get(d2)
    #         self.__draw_digit((2*digit.width)+x, y, digit, color)

    def __draw_digit(self, x, y, glyph, color):
        color_idx = self.__palette.from_color(color)
        for data in glyph:
            palette_idx = color_idx if data["on"] else 0
            self.__bitmap[data["x"]+x, data["y"]+y] = palette_idx

    def __display(self):
        # Current Temperature
        reading = self.__get_data("temperature")
        color = Temperature.from_temp(reading.value)
        print(f"{reading} ({color.name} => {color})")

        # 6 == number width (both digits)
        # center it on x
        x = (self.__bitmap.width // 2) - (6 // 2)

        self.__border(color)
        self.__display_number2(x,1, reading.value, color)

        # Low Temperature
        reading = self.__get_data("temperature-low")
        color = Temperature.from_temp(reading.value)
        self.__display_number2(1,9, reading.value, color)

        # High Temperature
        reading = self.__get_data("temperature-high")
        color = Temperature.from_temp(reading.value)
        self.__display_number2(15-6,9, reading.value, color)

    def update(self):
        now = time.time()
        if now - self.__last_update > self.INTERVAL:
            self.__last_update = now
            self.__display()

    # def update(self):
    #     self.__display_number(0, 0, self.__count)
    #     self.__count += 1










#
