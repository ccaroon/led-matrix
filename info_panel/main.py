import os
import time

import displayio

import led_matrix

from chronos import Chronos
from my_wifi import MyWiFi

from info_panel.glyph import Glyph
from info_panel.binary_clock.panel import BinaryClock
from info_panel.debugger.panel import DebugPanel
from info_panel.weather.panel import WeatherPanel

MyWiFi.autoconnect()
# MyWiFi.test()

Chronos.sync(tz_offset=os.getenv("time.tz_offset"))
# Chronos.test()
# Chronos.is_dst()

display = led_matrix.init_64x32()

# Weather
weather = WeatherPanel(0,0)

# Binary Clock
bin_clock = BinaryClock(16,0)

# Debugger
debug = DebugPanel(0,16)
# debug.bitmap[0,0] = 1

digit = Glyph.get("8")
debug.draw_glyph(digit)

main_group = displayio.Group()
main_group.append(weather)
main_group.append(bin_clock)
main_group.append(debug)
display.root_group = main_group

count = 0
while True:
    # print(f"--> tick:{count}")
    for panel in main_group:
        panel.update()

    count += 1
    time.sleep(1)
