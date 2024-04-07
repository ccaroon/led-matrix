import math
import random
import time

import displayio

import ulab.numpy as np
# https://github.com/scipy/scipy/blob/main/scipy/spatial/distance.py#L1864
# Not available in `ulab` -- grab from ^^^^^ and add locally here
# from scipy.spatial.distance import squareform, pdist
from ulab.numpy.linalg import norm


class Boids:
    MIN_DISTANCE = 1.0
    MAX_RULE_VELO = 0.03
    MAX_VELOCITY = .55

    def __init__(self, display, count, **kwargs):
        self.__display = display
        self.__count = count

        self.__iteration_count = kwargs.get("iterations", 100)
        self.__debug = kwargs.get("debug", False)

        self.__width = display.width
        self.__height = display.height

        self.__seed_center()

        angles = 2 * math.pi * np.random.rand(count)
        self.vel = np.array(list(zip(np.cos(angles), np.sin(angles))))

        self.__iteration = 1

    def __seed_center(self):
        # position of each boid
        # ...each being a random distance from the center up to 10 units away
        # ...represented a `count` pairs of (x,y) coordinates
        self.__boids = [self.__width / 2.0, self.__height / 2.0] + 5 * np.random.rand(2 * self.__count).reshape(self.__count, 2)

    def apply_boundary_wrap(self):
        delta_r = 0.99

        for coord in self.__boids:
            # Check Col
            if coord[0] > self.__width + delta_r:
                coord[0] = -delta_r

            if coord[0] < -delta_r:
                coord[0] = self.__width + delta_r

            # Check Row
            if coord[1] > self.__height + delta_r:
                coord[1] = -delta_r

            if coord[1] < -delta_r:
                coord[1] = self.__height + delta_r

    def apply_boundary_reflect(self):
        delta_r = 0.0
        # reverse_flock = False
        count = 0
        bad_boids = []
        for idx, coord in enumerate(self.__boids):
            boid_ok = True

            # Check Col
            if coord[0] > self.__width:
                coord[0] = self.__width - delta_r
                reverse_flock = True
                count += 1
                # self.vel[idx][1] *= -1
                boid_ok = False

            if coord[0] < 0:
                coord[0] = delta_r
                # reverse_flock = True
                count += 1
                # self.vel[idx][1] *= -1
                boid_ok = False

            # Check Row
            if coord[1] > self.__height:
                coord[1] = self.__height - delta_r
                # reverse_flock = True
                count += 1
                # self.vel[idx][0] *= -1
                boid_ok = False

            if coord[1] < 0:
                coord[1] = delta_r
                # reverse_flock = True
                count += 1
                # self.vel[idx][0] *= -1
                boid_ok = False

            if not boid_ok:
                bad_boids.append(idx)

        # If at least X hit boundary, reverse flock
        if count > (self.__count * .25):
            # for bidx in bad_boids:
                # self.vel[bidx][0] *= -1
                # self.vel[bidx][1] *= -1
            self.vel *= -1
            # self.vel[idx][0] *= -1
            # self.vel[idx][1] *= -1

    def apply_rules(self):
        # get pair-wise distances
        dist_matrix = squareform(pdist(self.__boids))

        # rule #1: separation
        D = dist_matrix < self.MIN_DISTANCE
        vel = self.__boids * D.sum(axis=1).reshape(self.__count, 1) - D.dot(self.__boids)
        self.limit(vel, self.MAX_RULE_VELO)

        D = dist_matrix < 50.0

        # rule #2 - alignment
        vel2 = D.dot(self.vel)
        self.limit(vel2, self.MAX_RULE_VELO)
        vel += vel2

        # rule #3 - cohesion
        vel3 = D.dot(self.__boids) - self.__boids
        self.limit(vel3, self.MAX_RULE_VELO)
        vel += vel3

        return vel

    def limit(self, vel, max_val):
        for vec in vel:
            self.limit_vec(vec, max_val)

    def limit_vec(self, vec, max_val):
        mag = norm(vec)
        if mag > max_val:
            vec[0], vec[1] = vec[0]*max_val/mag, vec[1]*max_val/mag

    def add(self, loc:tuple=None):
        # Add a new Boid
        row = loc[0] or (self.__height // 2)
        col = loc[1] or (self.__width // 2)
        self.__boids = np.concatenate(
            (self.__boids, np.array([[col,row]])),
            axis=0
        )
        angles = 2 * math.pi * np.random.rand(1)
        v = np.array(list(zip(np.sin(angles), np.cos(angles))))
        self.vel = np.concatenate((self.vel, v), axis=0)

        self.__count += 1

    def scatter(self, loc:tuple=None):
        row = loc[0] or random.randint(0, self.__height)
        col = loc[1] or random.randint(0, self.__width)
        self.vel += 0.1 * (self.__boids - np.array([[col, row]]))

    def tick(self):
        self.vel += self.apply_rules()
        self.limit(self.vel, self.MAX_VELOCITY)
        self.__boids += self.vel
        self.apply_boundary_reflect()

        self.__boids.reshape(2*self.__count)[::2],
        self.__boids.reshape(2*self.__count)[1::2]

        self.__iteration += 1

    # TODO: implement
    def display(self):
        for idx, boid in enumerate(self.__boids):
            col = int(boid[0])
            row = int(boid[1])
