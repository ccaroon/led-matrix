import displayio
import random

class GameOfLife:
    DEAD  = 0
    ALIVE = 1

    NEIGHBOR_OFFSETS = (
        (-1,-1),(+0,-1),(+1,-1),
        (-1,+0),        (+1,+0),
        (-1,+1),(+0,+1),(+1,+1)
    )

    def __init__(self, display):
        self.__display = display

        self.__board1 = displayio.Bitmap(display.width, display.height, 2)
        self.__board2 = displayio.Bitmap(display.width, display.height, 2)

        palette = displayio.Palette(2)
        palette[self.DEAD] = 0x000000
        palette[self.ALIVE] = 0x0000ff

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
        self.__seed_board(self.__board1)
        self.__show()

    def __seed_board(self, board, percent=50):
        width = board.width
        height = board.height
        count = int(width * height * (percent/100))
        for _ in range(count):
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)
            board[x,y] = self.ALIVE

    def __count_live_neighbors(self, board, cell:tuple):
        x = cell[0]
        y = cell[1]
        width = board.width
        height = board.height
        count = 0

        for offset in self.NEIGHBOR_OFFSETS:
            nx = x + offset[0]
            ny = y + offset[1]

            if (nx >= 0 and nx < width) and (ny >= 0 and ny < height):
                count += 1 if board[nx,ny] == self.ALIVE else 0
                # print(f"({x},{y}) - ({nx},{ny})...({board[nx][ny]})")

        # if count > 0:
        #     print(f"({x},{y})...{count}")

        return count

    def __set_cell(self, board, cell:tuple, state, count):
        x = cell[0]
        y = cell[1]

        if state == self.ALIVE:
            # Any live cell with fewer than two live neighbours dies
            if count < 2:
                board[x,y] = self.DEAD
                # print(f"{x},{y}: ALIVE --> DEAD")
            # Any live cell with two or three live neighbours lives
            elif count == 2 or count == 3:
                board[x,y] = self.ALIVE
                # print(f"{x},{y}: ALIVE --> ALIVE")
            # Any live cell with more than three live neighbours dies
            elif count > 3:
                board[x,y] = self.DEAD
                # print(f"{x},{y}: ALIVE --> DEAD")
            # else:
            #     print(f"{x},{y} - [{count}] ALIVE --> ?????")
        elif state == self.fDEAD:
            # Any dead cell with exactly three live neighbours becomes a live cell
            if count == 3:
                board[x,y] = self.ALIVE
                # print(f"{x},{y}: DEAD --> ALIVE")
            else:
                board[x,y] = self.DEAD
                # print(f"{x},{y} - [{count}] DEAD --> DEAD")
        # else:
        #     print(f"{x},{y}: ????? --> ?????")

    def __update_groups(self):
        if self.__generation % 2 == 0:
            self.__groups["live"] = self.__board1
            self.__groups["standby"] = self.__board2
        else:
            self.__groups["live"] = self.__board2
            self.__groups["standby"] = self.__board1

    def compute_generation(self):
        old_board = self.__groups["standby"][0].bitmap
        live_board = self.__groups["live"][0].bitmap
        width = old_board.width
        height = old_board.height
        for y in range(height):
            for x in range(width):
                count = self.__count_live_neighbors(old_board, (x,y))
                self.__set_cell(live_board, (x,y), old_board[x,y], count)

        self.__generation += 1

        self.__update_groups()
        self.__show()

    def __show(self):
        self.__display.root_group = self.__groups["live"]











#
