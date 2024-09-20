"""
MashUp of Boids & GameOfLife

Alternate between the Boids and the GameOfLife simulations
"""
import random
import time

from led_matrix import LEDMatrix
from boids.boids import BoidSimulation
from game_of_life.life import GameOfLife

matrix = LEDMatrix(64, 64, tile_across=1, tile_down=1, bit_depth=1)

BOIDS_MAX_ITER = 1000
boids = BoidSimulation(matrix.display)

GOL_MAX_GENS = 500
gol = GameOfLife(matrix.display)

active_sim = 0
SIMS = ["boids", "game_of_life"]

RUN_TIME = 60 * 5 # 5 minutes

start_time = time.time()
while True:
    curr_time = time.time()

    if curr_time - start_time > RUN_TIME:
        active_sim += 1
        if active_sim >= len(SIMS):
            active_sim = 0

        start_time = time.time()

    if SIMS[active_sim] == "boids":
        boids.init(count=random.randint(10, 16), iterations=BOIDS_MAX_ITER)
        boids.run()
        boids.clear()
    elif SIMS[active_sim] == "game_of_life":
        gol.seed_board()
        gol.update_display()
        for _ in range(GOL_MAX_GENS):
            gol.compute_generation()
            gol.update_display()
