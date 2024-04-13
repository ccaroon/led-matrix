import random

import led_matrix

from boids.boids import BoidSimulation

MAX_ITERATIONS = 1000

# display = led_matrix.init_64x64(bit_depth=1)
display = led_matrix.init64_XxX(128, 64, bit_depth=1)
simulation = BoidSimulation(display)
while True:
    simulation.init(count=random.randint(10, 21), iterations=MAX_ITERATIONS)
    simulation.run()
    simulation.clear()
