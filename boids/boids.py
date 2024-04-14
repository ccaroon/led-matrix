#
# Ported / Adapted from https://github.com/beneater/boids
#
import math
import random
import time

import displayio


class Boid:
    # This will also be the length of the trail if displaying trails is ON
    MAX_HISTORY = 5

    def __init__(self, x, y, dx=None, dy=None):
        self.x = x
        self.y = y
        self.dx = dx or random.random() * 10 - 5
        self.dy = dy or random.random() * 10 - 5
        self.perching = False
        # Set to a random # of iterations when the boid perches
        self.perch_time = None

        self.history = []
        self.update_history()

    def __repr__(self):
        return f"Boid({self.x},{self.y},{self.dx},{self.dy})"

    def __str__(self):
        return self.__repr__()

    # Speed will naturally vary in flocking behavior, but real animals can't go
    # arbitrarily fast.
    def adjust_speed(self, limit=15):
        speed = math.sqrt(self.dx ** 2 + self.dy ** 2)
        if speed > limit:
            self.dx = (self.dx / speed) * limit
            self.dy = (self.dy / speed) * limit

    def distance_to(self, other_boid):
        return math.sqrt(
            (self.x - other_boid.x) * (self.x - other_boid.x) +
            (self.y - other_boid.y) * (self.y - other_boid.y)
        )

    def update_history(self):
        self.history.append((self.x, self.y))
        # Only keep MAX_HISTORY records
        self.history = self.history[-self.MAX_HISTORY:]


class BoidSimulation:
    VISUAL_RANGE = 75
    MARGIN = 3

    COLOR_BLACK = 0
    COLOR_BOID = 1

    def __init__(self, display, **kwargs):
        self.__display = display

        self.__width = display.width
        self.__height = display.height
        self.__ground_level = self.__height - self.MARGIN

        self.__bitmap = displayio.Bitmap(self.__width, self.__height, 2)

        palette = displayio.Palette(2)
        palette[self.COLOR_BLACK] = 0x000000
        palette[self.COLOR_BOID] = self.__random_color()
        self.__palette = palette

        # TileGrid & Group1
        grid1 = displayio.TileGrid(self.__bitmap, pixel_shader=palette)
        self.__group1 = displayio.Group()
        self.__group1.append(grid1)
        self.__display.root_group = self.__group1

        self.init(**kwargs)

    def init(self, **kwargs):
        self.__palette[self.COLOR_BOID] = self.__random_color()

        self.__count = kwargs.get("count", random.randint(50, 101))
        self.__iteration_count = kwargs.get("iterations", 500)
        self.__delay = kwargs.get("delay", 0.075)
        self.__perch_chance = kwargs.get("perch_chance", random.randint(10, 50)) / 100.0
        self.__trails = kwargs.get("trails", random.choice((True, False)))
        # self.__debug = kwargs.get("debug", False)

        self.__boids = []
        self.__init_boids(pattern=random.choice(("random", "center")))

        self.__iteration = 1

    def __init_boids(self, pattern="random"):
        for _ in range(self.__count):
            if pattern == "random":
                x = random.random() * self.__width
                y = random.random() * self.__height
            elif pattern == "center":
                x = (self.__width / 2.0) + 10 * random.random()
                y = (self.__height / 2.0) + 10 * random.random()

            self.__boids.append(
                Boid(x, y)
            )

    # Constrain a boid to within the window. If it gets too close to an edge,
    # nudge it back in and reverse its direction.
    def __keep_within_bounds(self, boid):
        turn_factor = 1

        if boid.x < self.MARGIN:
            boid.dx += turn_factor

        if boid.x > self.__width - self.MARGIN:
            boid.dx -= turn_factor

        if boid.y < self.MARGIN:
            boid.dy += turn_factor

        if boid.y > self.__height - self.MARGIN:
            boid.dy -= turn_factor

        if boid.y >= self.__ground_level and random.random() < self.__perch_chance:
            boid.perching = True
            # number of iterations to perch
            boid.perch_time = random.randint(5, 25)

    # Find the center of mass of the other boids and adjust velocity slightly to
    # point towards the center of mass.
    def __fly_towards_center(self, boid):
        # adjust velocity by this %
        centering_factor = 0.005

        center_x = 0
        center_y = 0
        num_neighbors = 0

        for other_boid in self.__boids:
            if boid.distance_to(other_boid) < self.VISUAL_RANGE:
                center_x += other_boid.x
                center_y += other_boid.y
                num_neighbors += 1

        if num_neighbors:
            center_x = center_x / num_neighbors
            center_y = center_y / num_neighbors

            boid.dx += (center_x - boid.x) * centering_factor
            boid.dy += (center_y - boid.y) * centering_factor

    # Move away from other boids that are too close to avoid colliding
    def __avoid_others(self, boid):
        # The distance to stay away from other boids
        min_distance = 2

        # Adjust velocity by this %
        avoid_factor = 0.05

        move_x = 0
        move_y = 0

        for other_boid in self.__boids:
            if other_boid is not boid:
                if boid.distance_to(other_boid) < min_distance:
                    move_x += boid.x - other_boid.x
                    move_y += boid.y - other_boid.y

        boid.dx += move_x * avoid_factor
        boid.dy += move_y * avoid_factor

    # // Find the average velocity (speed and direction) of the other boids and
    # // adjust velocity slightly to match.
    def __match_velocity(self, boid):
        # Adjust by this % of average velocity
        matching_factor = 0.05

        avg_dx = 0
        avg_dy = 0
        num_neighbors = 0

        for other_boid in self.__boids:
            if boid.distance_to(other_boid) < self.VISUAL_RANGE:
                avg_dx += other_boid.dx
                avg_dy += other_boid.dy
                num_neighbors += 1

        if num_neighbors:
            avg_dx = avg_dx / num_neighbors
            avg_dy = avg_dy / num_neighbors

            boid.dx += (avg_dx - boid.dx) * matching_factor
            boid.dy += (avg_dy - boid.dy) * matching_factor

    # Random primary color
    def __random_color(self):
        color = (
            (0x0000ff if random.random() > .33 else 0) |
            (0x00ff00 if random.random() > .33 else 0) |
            (0xff0000 if random.random() > .33 else 0)
        ) or 0x00ff00

        return color

    def add(self, loc: tuple = None):
        # Add a new Boid
        row = loc[0] if loc is not None else self.__height // 2
        col = loc[1] if loc is not None else self.__width // 2

        self.__boids.append(Boid(col, row))
        self.__count += 1

    def __dump(self):
        for boid in self.__boids:
            if boid.x < 0 or boid.x > self.__width or boid.y < 0 or boid.y > self.__height:
                print(f"{boid}")

    def tick(self):
        for boid in self.__boids:
            if boid.perching:
                if boid.perch_time > 0:
                    boid.perch_time -= 1
                else:
                    boid.perching = False
            else:
                boid.update_history()

                # Update the velocities according to each rule
                self.__fly_towards_center(boid)
                self.__avoid_others(boid)
                self.__match_velocity(boid)
                boid.adjust_speed(limit=15)
                self.__keep_within_bounds(boid)

                # Update the position based on the current velocity
                boid.x += boid.dx
                # Keep in col/width bounds
                boid.x = self.MARGIN if boid.x < 0 else boid.x
                boid.x = self.__width - self.MARGIN if boid.x > self.__width else boid.x

                boid.y += boid.dy
                # keep in row/height bounds
                boid.y = self.MARGIN if boid.y < 0 else boid.y
                boid.y = self.__height - self.MARGIN if boid.y > self.__height else boid.y

        self.__iteration += 1

    def display(self):
        for boid in self.__boids:
            curr_x = int(boid.x)
            curr_y = int(boid.y)
            self.__bitmap[curr_x, curr_y] = self.COLOR_BOID

            # if trails off -> erase most recent history
            off_x = int(boid.history[-1][0])
            off_y = int(boid.history[-1][1])
            # if trails on -> erase oldest history
            if self.__trails:
                off_x = int(boid.history[0][0])
                off_y = int(boid.history[0][1])

            self.__bitmap[off_x, off_y] = self.COLOR_BLACK

    def clear(self):
        for i in range(self.__width * self.__height):
            self.__bitmap[i] = self.COLOR_BLACK

    def run(self):
        for _ in range(self.__iteration_count):
            self.display()
            self.tick()
            # time.sleep(self.__delay)
