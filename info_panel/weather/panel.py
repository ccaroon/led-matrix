import os

from lib.colors.weather import Weather as WeatherColors
from info_panel.panel import Panel

from my_wifi import MyWiFi
from aio import AdafruitIO

# TODO:
# * [x] old data
# * [ ] data retrieval error
# * [x] humidity
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
class WeatherPanel(Panel):
    # Update interval
    UPDATE_INTERVAL = 5 * 60  # 5 mins
    OLD_INTERVAL    = 10 * 60 # 10 mins
    # 200 degrees -> "really_hot" => RED
    ERROR_COLOR     = WeatherColors.from_temp(200)

    def __init__(self, x, y):
        super().__init__(x, y, WeatherColors.palette())

        self.__aio = AdafruitIO(
            MyWiFi.REQUESTS,
            "weather-station",
            { "username": os.getenv("aio.username"), "key": os.getenv("aio.key")}
        )

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

    def __draw_humidity(self, value):
        color = WeatherColors.from_humidity(value)
        # print(f"{value}% => ({color})")

        # Compute line length
        # 7 levels = 100/7 == 14.286 * 2 lights / level
        line_len =  ((value // 14.286) + 1) * 2
        # print(f"line_len: [{line_len}]")

        # Get color
        black_idx = self._palette.from_name("black")
        color_idx = self._palette.from_color(color)

        # Draw line centered on y=7
        start_x = int((self._bitmap.width // 2) - (line_len // 2))
        end_x = start_x + int(line_len)
        line = range(start_x, end_x)
        for x in range(1, self._bitmap.width-1):
            # print(f"[x,y] = [{x},7]")
            if x in line:
                self._bitmap[x,7] = color_idx
            else:
                self._bitmap[x,7] = black_idx

    def _update_display(self):
        # Current Temperature
        reading = self.__get_data("temperature")
        color = WeatherColors.from_temp(reading.value)
        # print(f"{reading.value} - {reading.age} > {self.OLD_INTERVAL} ({color})")

        # 6 == number width (both digits)
        # center it on x
        x = (self._bitmap.width // 2) - (6 // 2)
        self._draw_number2(x, 1, reading.value, color)

        # Border - Color based on current temperature
        # ...or ERROR_COLOR if data is "old"
        # TODO: don't updated the border **EVERY** time. Only if change.
        border_color = self.ERROR_COLOR if reading.age >= self.OLD_INTERVAL else color
        self._border(border_color)

        # Low Temperature
        reading = self.__get_data("temperature-low")
        color = WeatherColors.from_temp(reading.value)
        self._draw_number2(1, 9, reading.value, color)

        # High Temperature
        reading = self.__get_data("temperature-high")
        color = WeatherColors.from_temp(reading.value)
        self._draw_number2(15-6, 9, reading.value, color)

        # Humidity
        reading = self.__get_data("humidity")
        self.__draw_humidity(reading.value)











#
