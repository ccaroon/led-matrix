import time
import displayio
import os

from lib.colors.color import Color
# **MUST** set the ORDER (iff not normal) before importing other Color classes
Color.ORDER = ("R", "B", "G")
from lib.colors.weather import Weather
from info_panel.glyph import Glyph

from my_wifi import MyWiFi
from aio import AdafruitIO

# TODO:
# * [ ] old data
# * [ ] data retrieval error
# * [ ] humidity
# * [ ] combine color sets and Palette? I.e. color set subclasses of Palette?
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
    UPDATE_INTERVAL = 5 * 60  # 5 mins
    OLD_INTERVAL    = 10 * 60 # 10 mins
    # 200 degrees -> "really_hot" => RED
    ERROR_COLOR     = Weather.from_temp(200)

    def __init__(self, x, y):
        super().__init__(x=x, y=y)

        self.__palette = Weather.palette()
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
        reading = None
        if resp["success"]:
            reading = Reading(
                name,
                int(resp["results"][0]["value"]),
                resp["age"]
            )
        return reading

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

    def __draw_humidity(self, value):
        color = Weather.from_humidity(value)
        # print(f"{value}% => ({color})")

        # Compute line length
        # 7 levels = 100/7 == 14.286 * 2 lights / level
        line_len =  ((value // 14.286) + 1) * 2

        # Get color
        color_idx = self.__palette.from_color(color)

        # Draw line centered on y=7
        start_x = (self.__bitmap.width // 2) - (line_len // 2)
        for x in range(int(start_x), int(line_len)+1):
            self.__bitmap[x,7] = color_idx

    def __display(self):
        # Current Temperature
        reading = self.__get_data("temperature")
        color = Weather.from_temp(reading.value)
        # print(f"{reading.value} - {reading.age} > {self.OLD_INTERVAL} ({color})")

        # 6 == number width (both digits)
        # center it on x
        x = (self.__bitmap.width // 2) - (6 // 2)
        self.__display_number2(x, 1, reading.value, color)

        # Border - Color based on current temperature
        # ...or ERROR_COLOR if data is "old"
        border_color = self.ERROR_COLOR if reading.age >= self.OLD_INTERVAL else color
        self.__border(border_color)

        # Low Temperature
        reading = self.__get_data("temperature-low")
        color = Weather.from_temp(reading.value)
        self.__display_number2(1, 9, reading.value, color)

        # High Temperature
        reading = self.__get_data("temperature-high")
        color = Weather.from_temp(reading.value)
        self.__display_number2(15-6, 9, reading.value, color)

        # Humidity
        reading = self.__get_data("humidity")
        self.__draw_humidity(reading.value)


    def update(self):
        now = time.time()
        if now - self.__last_update > self.UPDATE_INTERVAL:
            self.__last_update = now
            self.__display()

    # def update(self):
    #     self.__display_number(0, 0, self.__count)
    #     self.__count += 1










#
