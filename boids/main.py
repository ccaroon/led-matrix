import os
import random

from chronos import Chronos
from my_wifi import MyWiFi
from led_matrix import LEDMatrix

from boids.boids import BoidSimulation

MyWiFi.autoconnect()
# MyWiFi.test()

Chronos.sync(tz_offset=os.getenv("time.tz_offset"))

MAX_ITERATIONS = 1000

matrix = LEDMatrix(64, 64, tile_across=1, tile_down=1, bit_depth=4)
simulation = BoidSimulation(matrix.display)
while True:
    simulation.init(count=random.randint(10, 16), iterations=MAX_ITERATIONS)
    simulation.run()
    simulation.clear()
