import displayio
import random

from lib.colors.season import Season as SeasonColors

import game_of_life.patterns as patterns

class GameOfLife:
    DEAD  = 0
    ALIVE = 1

    # NEIGHBOR_OFFSETS = (
    #     (-1,-1),(+0,-1),(+1,-1),
    #     (-1,+0),        (+1,+0),
    #     (-1,+1),(+0,+1),(+1,+1)
    # )

    def __init__(self, display):
        self.__display = display

        self.__width = display.width
        self.__height = display.height

        self.__board1 = displayio.Bitmap(self.__width, self.__height, 2)
        self.__board2 = displayio.Bitmap(self.__width, self.__height, 2)

        palette = displayio.Palette(2)
        palette[self.DEAD] = 0x000000
        palette[self.ALIVE] = 0x000000
        self.__palette = palette

        # TileGrid & Group1
        grid1 = displayio.TileGrid(self.__board1, pixel_shader=palette)
        self.__group1 = displayio.Group()
        self.__group1.append(grid1)

        # TileGrid & Group2
        grid2 = displayio.TileGrid(self.__board2, pixel_shader=palette)
        self.__group2 = displayio.Group()
        self.__group2.append(grid2)

        self.__groups = {
            "live": self.__group1,
            "standby": self.__group2
        }

        self.__generation = 0

    def __seed_from_pattern(self, board, pattern, offset:tuple=(0,0), center=False):
        pat_width = pattern["width"]
        pat_height = pattern["height"]

        if pat_width > self.__width or pat_height > self.__height:
            raise ValueError(f"Board size to small for pattern. Min Size: ({pat_width}x{pat_height})")

        # Compute offset to center pattern on board
        if center:
            off_x = (self.__width // 2) - (pat_width // 2)
            off_y = (self.__height // 2) - (pat_height // 2)
        else:
            off_x = offset[0]
            off_y = offset[1]

        bitmap = pattern["bitmap"]
        for (idx, state) in enumerate(bitmap):
            x = idx % pat_width
            y = idx // pat_width
            board[x+off_x, y+off_y] = self.ALIVE if state else self.DEAD

    def __seed_randomly(self, board, percent=50):
        width = self.__width
        height = self.__height
        count = int(width * height * (percent/100))
        for _ in range(count):
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)
            board[x,y] = self.ALIVE

    # TODO: This code is too slow.
    # Needs to be optimized
    # def __count_live_neighbors(self, board, cell:tuple):
    #     x = cell[0]
    #     y = cell[1]
    #     width = self.__width
    #     height = self.__height
    #     count = 0

    #     for offset in self.NEIGHBOR_OFFSETS:
    #         nx = x + offset[0]
    #         ny = y + offset[1]

    #         if (nx >= 0 and nx < width) and (ny >= 0 and ny < height):
    #             count += 1 if board[nx,ny] == self.ALIVE else 0

    #     return count

    # TODO: This code is too slow.
    # Needs to be optimized
    # def __set_cell(self, board, cell:tuple, state, count):
    #     x = cell[0]
    #     y = cell[1]

    #     if state == self.ALIVE:
    #         # Any live cell with fewer than two live neighbours dies
    #         if count < 2:
    #             board[x,y] = self.DEAD
    #         # Any live cell with two or three live neighbours lives
    #         elif count == 2 or count == 3:
    #             board[x,y] = self.ALIVE
    #         # Any live cell with more than three live neighbours dies
    #         elif count > 3:
    #             board[x,y] = self.DEAD
    #     elif state == self.DEAD:
    #         # Any dead cell with exactly three live neighbours becomes a live cell
    #         if count == 3:
    #             board[x,y] = self.ALIVE
    #         else:
    #             board[x,y] = self.DEAD

    # Random primary color
    def __random_primary_color(self):
        color = (
        (0x0000ff if random.random() > .33 else 0) |
        (0x00ff00 if random.random() > .33 else 0) |
        (0xff0000 if random.random() > .33 else 0)) or 0xffffff

        return color

    def __random_color(self):
        color_set = SeasonColors.get("current")
        color = random.choice(color_set)

        return color.value

    # Algorithm - 2020 Jeff Epler for Adafruit Industries
    # https://learn.adafruit.com/rgb-led-matrices-matrix-panels-with-circuitpython/example-conways-game-of-life
    # --------------------------------------------------------------------------
    # The complicated way that the "m1" (minus 1) and "p1" (plus one) offsets are
    # calculated is due to the way the grid "wraps around", with the left and right
    # sides being connected, as well as the top and bottom sides being connected.
    #
    # This function has been somewhat optimized, so that when it indexes the bitmap
    # a single number [x + width * y] is used instead of indexing with [x, y].
    # This makes the animation run faster with some loss of clarity. More
    # optimizations are probably possible.
    # --------------------------------------------------------------------------
    def __apply_rules(self, old, new):
        for y in range(self.__height):
            yyy = y * self.__width
            ym1 = ((y + self.__height - 1) % self.__height) * self.__width
            yp1 = ((y + 1) % self.__height) * self.__width
            xm1 = self.__width - 1
            for x in range(self.__width):
                xp1 = (x + 1) % self.__width
                # Assumes DEAD == 0 and ALIVE == 1
                neighbors = (
                    old[xm1 + ym1] + old[xm1 + yyy] + old[xm1 + yp1] +
                    old[x   + ym1] +                  old[x   + yp1] +
                    old[xp1 + ym1] + old[xp1 + yyy] + old[xp1 + yp1])
                new[x+yyy] = neighbors == 3 or (neighbors == 2 and old[x+yyy])
                xm1 = x

    def __update_groups(self):
        if self.__generation % 2 == 0:
            self.__groups["live"] = self.__group1
            self.__groups["standby"] = self.__group2
        else:
            self.__groups["live"] = self.__group2
            self.__groups["standby"] = self.__group1

    def seed_board(self):
        self.__generation = 0

        # clear the board
        for i in range(self.__width * self.__height):
            self.__board1[i] = self.DEAD

        self.__palette[self.ALIVE] = self.__random_color()

        if random.choice((False, True)):
            pattern_name = random.choice(list(patterns.PATTERNS.keys()))
            pattern = patterns.PATTERNS[pattern_name]
            self.__seed_from_pattern(self.__board1, pattern, center=True)
            print(f"Seeding with '{pattern_name}' pattern.")
        else:
            print("Seeding randomly.")
            self.__seed_randomly(self.__board1, percent=33)

    def compute_generation(self):
        old_board = self.__groups["live"][0].bitmap
        new_board = self.__groups["standby"][0].bitmap
        self.__apply_rules(old_board, new_board)
        # -----------------------------------------
        # This code (my code) is too slow
        # -----------------------------------------
        # width = self.__width
        # height = self.__height
        # for y in range(height):
        #     for x in range(width):
        #         count = self.__count_live_neighbors(old_board, (x,y))
        #         self.__set_cell(new_board, (x,y), old_board[x,y], count)
        # -----------------------------------------

        self.__generation += 1
        # print(self.__generation)

    def update_display(self):
        self.__update_groups()
        self.__display.root_group = self.__groups["live"]
