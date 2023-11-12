import time
import led_matrix

from game_of_life.life import GameOfLife

display = led_matrix.init_64x64()
game = GameOfLife(display)
while True:
    # pass
    game.compute_generation()
    # time.sleep(.1)
