import time
import led_matrix

from game_of_life.life import GameOfLife

MAX_GENS = 250

display = led_matrix.init_64x64(bit_depth=1)
game = GameOfLife(display)
while True:
    game.seed_board()
    game.update_display()

    for _ in range(MAX_GENS):
        game.compute_generation()
        game.update_display()
        # time.sleep(.75)
