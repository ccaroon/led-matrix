import os
import time

import displayio

import led_matrix

from chronos import Chronos
from my_wifi import MyWiFi

from lib.colors.color import Color
# **MUST** set the ORDER (iff not normal) before importing other Color classes
Color.ORDER = ("R", "B", "G")

from info_panel.binary_clock.panel import BinaryClock
from info_panel.digital_clock.panel import DigitalClock
from info_panel.debugger.panel import DebugPanel
from info_panel.fibonacci_clock.panel import FibonacciClock
from info_panel.iss.panel import ISSPanel
from info_panel.message.panel import MessagePanel
from info_panel.moon.panel import MoonPanel
from info_panel.weather.panel import WeatherPanel

MyWiFi.autoconnect()
# MyWiFi.test()

Chronos.sync(tz_offset=os.getenv("time.tz_offset"))
# Chronos.test()
# Chronos.is_dst()

display = led_matrix.init_64x32()

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
digi_clock = DigitalClock(pos[0], pos[1])

# Weather
pos = panel_pos(PANEL_LAYOUT["Weather"])
weather = WeatherPanel(pos[0], pos[1])

# Binary Clock
pos = panel_pos(PANEL_LAYOUT["BinaryClock"])
bin_clock = BinaryClock(pos[0], pos[1])

# Debugger
# pos = panel_pos(PANEL_LAYOUT["Debugger"])
# debug = DebugPanel(pos[0], pos[1])

# Fibonacci Clock
pos = panel_pos(PANEL_LAYOUT["FibonacciClock"])
fib_clock = FibonacciClock(pos[0], pos[1])

# ISS Tracker
pos = panel_pos(PANEL_LAYOUT["ISSTracker"])
iss = ISSPanel(pos[0], pos[1])

# Message Panel -- Takes up panels 4,5,6
pos = panel_pos(PANEL_LAYOUT["MessagePanel"])
# Shift X 1/2 a PANEL_WIDTH
# mp_x = pos[0] + (PANEL_WIDTH // 2)
message = MessagePanel(pos[0], pos[1])

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

while True:
    # print(f"--> tick:{count}")
    for panel in main_group:
        panel.update()

    time.sleep(1)
