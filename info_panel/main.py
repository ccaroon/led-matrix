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
# from info_panel.debugger.panel import DebugPanel
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

rows = 2
cols = 4
panel_pos = []
for row in range(rows):
    for col in range(cols):
        panel_pos.append(
            {
                "x": (display.width // cols)  * col,
                "y": (display.height // rows) * row
            }
        )

# Digital Clock
digi_clock = DigitalClock(panel_pos[0]["x"], panel_pos[0]["y"])

# Weather
weather = WeatherPanel(panel_pos[1]["x"], panel_pos[1]["y"])

# Binary Clock
bin_clock = BinaryClock(panel_pos[2]["x"], panel_pos[2]["y"])

# Debugger
# debug = DebugPanel(panel_pos[2]["x"], panel_pos[2]["y"])

iss = ISSPanel(panel_pos[3]["x"], panel_pos[3]["y"])

# Message Panel -- Takes up panels 4,5,6
message = MessagePanel(panel_pos[4]["x"], panel_pos[4]["y"])

# moon = MoonPanel(panel_pos[7]["x"], panel_pos[5]["y"])

main_group = displayio.Group()
# Listed in Update Priority
main_group.append(digi_clock)
main_group.append(bin_clock)
main_group.append(iss)
main_group.append(weather)
main_group.append(message)
# main_group.append(moon)
# main_group.append(debug)

display.root_group = main_group

while True:
    # print(f"--> tick:{count}")
    for panel in main_group:
        panel.update()

    time.sleep(1)
