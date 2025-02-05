from point import *


class Matrix:
    def __init__(self, size=4):
        self.size = 4
        self.m = [[0] * size for _ in range(size)]
        for i in range(size):
            self.m[i][i] = 1

    def from_translate(self, translate):
        translate = Point(translate)
        for i in range(self.size - 1):
            self.m[i][-1] = translate[i]

    def from_rotate_axis(self, axis, angle):
        pass
