import random

from led_matrix import LEDMatrix
from boids.boids import BoidSimulation

MAX_ITERATIONS = 1000

matrix = LEDMatrix(64, 64, tile_across=2, tile_down=1, bit_depth=1)
simulation = BoidSimulation(matrix.display)
while True:
    simulation.init(count=random.randint(10, 21), iterations=MAX_ITERATIONS)
    simulation.run()
    simulation.clear()
