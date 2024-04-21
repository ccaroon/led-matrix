from led_matrix import LEDMatrix
from game_of_life.life import GameOfLife

MAX_GENS = 500

matrix = LEDMatrix(64, 64, tile_across=2, tile_down=1, bit_depth=1)
game = GameOfLife(matrix.display)
while True:
    game.seed_board()
    game.update_display()

    for _ in range(MAX_GENS):
        game.compute_generation()
        game.update_display()
