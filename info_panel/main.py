import os
import time

import displayio

from led_matrix import LEDMatrix

from chronos import Chronos
from my_wifi import MyWiFi

from lib.colors.color import Color
# **MUST** set the ORDER (iff not normal) before importing other Color classes

MATRICES = {
    "small": {
        "width": 64,
        "height": 32,
        "scale": 1,
        "tile_across": 1
    },
    "large": {
        "width": 64,
        "height": 64,
        "scale": 2,
        "tile_across": 2
    }
}
MATRIX = MATRICES["large"]

if MATRIX["height"] == 32:
    Color.ORDER = ("R", "B", "G")

from info_panel.binary_clock.panel import BinaryClock
from info_panel.digital_clock.panel import DigitalClock
from info_panel.debugger.panel import DebugPanel
from info_panel.fibonacci_clock.panel import FibonacciClock
from info_panel.iss.panel import ISSPanel
from info_panel.message.panel import MessagePanel
# from info_panel.moon.panel import MoonPanel
from info_panel.weather.panel import WeatherPanel

MyWiFi.autoconnect()
# MyWiFi.test()

Chronos.sync(tz_offset=os.getenv("time.tz_offset"))
# Chronos.test()
# Chronos.is_dst()

matrix = LEDMatrix(
    MATRIX["width"], MATRIX["height"],
    tile_across=MATRIX["tile_across"],
    tile_down=1,
    bit_depth=4
)
display = matrix.display

PANEL_ROWS = 2
PANEL_COLS = 4
PANEL_WIDTH = display.width // PANEL_COLS
PANEL_HEIGHT = display.height // PANEL_ROWS


def panel_pos(idx):
    row = idx // PANEL_COLS
    col = idx % PANEL_COLS

    if row >= PANEL_ROWS or col >= PANEL_COLS:
        raise ValueError(f"Invalid Panel Position: [{idx}]")

    x = (display.width // PANEL_COLS) * col
    y = (display.height // PANEL_ROWS) * row

    return x, y


PANEL_LAYOUT = {
    "MessagePanel": 0,  # 0,1,2 ALL taken up
    "DigitalClock": 4,
    "Weather": 5,
    "BinaryClock": 3,
    # "Debugger": 6,
    "FibonacciClock": 6,
    # "MoonPhase": 6,
    "ISSTracker": 7
}

# Digital Clock
pos = panel_pos(PANEL_LAYOUT["DigitalClock"])
digi_clock = DigitalClock(pos[0], pos[1], scale=MATRIX["scale"])

# Weather
pos = panel_pos(PANEL_LAYOUT["Weather"])
weather = WeatherPanel(pos[0], pos[1], scale=MATRIX["scale"])

# Binary Clock
pos = panel_pos(PANEL_LAYOUT["BinaryClock"])
bin_clock = BinaryClock(pos[0], pos[1], scale=MATRIX["scale"])

# Debugger
# pos = panel_pos(PANEL_LAYOUT["Debugger"])
# debug = DebugPanel(pos[0], pos[1])

# Fibonacci Clock
pos = panel_pos(PANEL_LAYOUT["FibonacciClock"])
fib_clock = FibonacciClock(pos[0], pos[1], scale=MATRIX["scale"])

# ISS Tracker
pos = panel_pos(PANEL_LAYOUT["ISSTracker"])
iss = ISSPanel(pos[0], pos[1], scale=MATRIX["scale"])

# Message Panel -- Takes up panels 4,5,6
pos = panel_pos(PANEL_LAYOUT["MessagePanel"])
# Shift X 1/2 a PANEL_WIDTH
# mp_x = pos[0] + (PANEL_WIDTH // 2)
message = MessagePanel(pos[0], pos[1], scale=MATRIX["scale"])

# Moon Phase
# pos = panel_pos(PANEL_LAYOUT["MoonPhase"])
# moon = MoonPanel(pos[0], pos[1)

# Add Panels to main Display Group
# Listed in Update Priority Order
main_group = displayio.Group()
main_group.append(digi_clock)
main_group.append(bin_clock)
main_group.append(iss)
main_group.append(weather)
main_group.append(fib_clock)
main_group.append(message)
# main_group.append(moon)
# main_group.append(debug)

display.root_group = main_group

# TODO: Move / clean-up this code
ON_TIME = 900
OFF_TIME = 2359
IS_ON = True

def in_on_window(time_code):
    return time_code >= ON_TIME and time_code < OFF_TIME

def time_code():
    now = time.localtime()
    return (now.tm_hour * 100) + now.tm_min

display.auto_refresh = False
while True:
    now = time_code()
    if not IS_ON and in_on_window(now):
        IS_ON = True
        display.brightness = 1.0
        display.refresh()
    elif IS_ON and not in_on_window(now):
        IS_ON = False
        display.brightness = 0.0
        display.refresh()

    if IS_ON:
        for panel in main_group:
            panel.update()
            display.refresh()

    time.sleep(1)
