import led_matrix

from boids.boids import Boids

MAX_GENS = 500

display = led_matrix.init_64x64(bit_depth=1)
simulation = Boids(display)
while True:
    for _ in range(MAX_GENS):
        simulation.tick()
        simulation.display()
        # time.sleep(.75)
