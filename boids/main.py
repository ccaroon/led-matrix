import led_matrix

from boids.boids import BoidSimulation

MAX_ITERATIONS = 1000

display = led_matrix.init_64x64(bit_depth=1)
simulation = BoidSimulation(display)
while True:
    simulation.init(count=20, iterations=MAX_ITERATIONS)
    simulation.run()
    simulation.clear()
