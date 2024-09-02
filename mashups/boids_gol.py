"""
MashUp of Boids & GameOfLife

Alternate between the Boids and the GameOfLife simulations
"""
import random

from led_matrix import LEDMatrix
from boids.boids import BoidSimulation
from game_of_life.life import GameOfLife

matrix = LEDMatrix(64, 64, tile_across=1, tile_down=1, bit_depth=1)

BOIDS_MAX_ITER = 1000
simulation = BoidSimulation(matrix.display)

GOL_MAX_GENS = 500
game = GameOfLife(matrix.display)

while True:
    # Boids
    simulation.init(count=random.randint(10, 16), iterations=BOIDS_MAX_ITER)
    simulation.run()
    simulation.clear()

    # Game Of Life
    game.seed_board()
    game.update_display()
    for _ in range(GOL_MAX_GENS):
        game.compute_generation()
        game.update_display()
