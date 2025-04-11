import os

from chronos import Chronos
from my_wifi import MyWiFi
from led_matrix import LEDMatrix

from game_of_life.life import GameOfLife

MyWiFi.autoconnect()
# MyWiFi.test()

Chronos.sync(tz_offset=os.getenv("time.tz_offset"))

MAX_GENS = 500

matrix = LEDMatrix(64, 64, tile_across=1, tile_down=1, bit_depth=4)
game = GameOfLife(matrix.display)
while True:
    game.seed_board()
    game.update_display()

    for _ in range(MAX_GENS):
        game.compute_generation()
        game.update_display()
