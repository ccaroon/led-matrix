import time
import displayio
import os

from info_panel.glyph import Glyph

from my_wifi import MyWiFi
from aio import AdafruitIO

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
    INTERVAL = 1 * 60

    def __init__(self, x, y):
        super().__init__(x=x, y=y)

        self.__bitmap = displayio.Bitmap(16, 16, 2)
        palette = displayio.Palette(2)
        palette[0] = 0x000000
        palette[1] = 0x0000ff

        grid = displayio.TileGrid(self.__bitmap, pixel_shader=palette)

        self.append(grid)

        self.__last_update = 0
        self.__aio = AdafruitIO(
            MyWiFi.REQUESTS,
            "weather-station",
            { "username": os.getenv("aio.username"), "key": os.getenv("aio.key")}
        )

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

    # TODO: implement me
    def __display_number(self, x, y, number):
        dwidth = 3
        d0 = number // 100
        d1 = number // 10
        d2 = number % 10

        if d0 > 0:
            digit = Glyph.get(d0)
            self.__draw_digit(0*dwidth,0,digit)

        if d1 > 0:
            digit = Glyph.get(d1)
            self.__draw_digit(1*dwidth,0,digit)

        if d2 > 0:
            digit = Glyph.get(d2)
            self.__draw_digit(2*dwidth,0,digit)

    def __draw_digit(self, x, y, glyph):
        for data in glyph:
            self.__bitmap[data["col"]+x, data["row"]+y] = data["color"]

    def __display(self):
        reading = self.__get_data("temperature")
        print(reading)
        self.__display_number(0,0, reading.value)

    def update(self):
        now = time.time()
        if now - self.__last_update > self.INTERVAL:
            self.__last_update = now
            self.__display()










#
