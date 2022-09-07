import random
from point import *


class Triangle:
    def __init__(self, a, b, c):
        self.a = Point(a)
        self.b = Point(b)
        self.c = Point(c)

    def __getitem__(self, key):
        if key == 0:
            return self.a
        if key == 1:
            return self.b
        if key == 2:
            return self.c
        raise KeyError('Invalid item: %s' % key)

    def __str__(self) -> str:
        return 'Triangle: [' + str(self.a) + ', ' + str(self.b) + ', ' + str(self.c) + ']'

    @property
    def normal(self):
        assert len(self.a) == 3
        b, c = self.b - self.a, self.c - self.a
        return b.cross(c).normalized()

    @property
    def aabb(self):
        d = len(self.a)
        mn = [math.inf] * d
        mx = [-math.inf] * d
        for i in range(3):
            for j in range(d):
                mn[j] = min(mn[j], self[i][j])
                mx[j] = max(mx[j], self[i][j])
        return mn, mx

    @property
    def centroid(self):
        return (self.a + self.b + self.c) / 3.0

    def area(self, doubled=False):
        b, c = self.b - self.a, self.c - self.a
        self.A = b.cross(c)
        if not doubled: self.A /= 2
        return self.A

    def incircle(self):
        """ Reference
            [1] Heron's formula: https://en.wikipedia.org/wiki/Heron%27s_formula
        """
        a = abs(self.b - self.c)
        b = abs(self.a - self.c)
        c = abs(self.a - self.b)
        s = (a + b + c) / 2
        r = math.sqrt((s - a) * (s - b) * (s - c) / s)
        return (a * self.a + b * self.b + c * self.c) / (a + b + c), r

    def circumcircle(self):
        """ Reference
            [1] https://en.wikipedia.org/wiki/Circumscribed_circle#Cartesian_coordinates_from_cross-_and_dot-products
        """
        a = self.b - self.c  # p2-p3
        b = self.c - self.a  # p3-p1
        c = self.a - self.b  # p1-p2
        r = abs(a) * abs(b) * abs(c) / abs(b.cross(a) * 2)

        tmp = - c.cross(a) ** 2 * 2
        alpha = a ** 2 * c.dot(b)
        beta = b ** 2 * c.dot(a)
        gamma = c ** 2 * b.dot(a)
        return (alpha * self.a + beta * self.b + gamma * self.c) / tmp, r

    def inside_point(self, p):
        assert len(p) == len(self.a)
        if len(p) == 2:
            p, b, c = p - self.a, self.b - self.a, self.c - self.a
            if b.cross(c) < 0:
                b, c = c, b
            if b.cross(p) < 0 or p.cross(c) < 0 or (c - b).cross(p - b) < 0:
                return False
            return True
        if len(p) == 3:
            p, b, c = p - self.a, self.b - self.a, self.c - self.a

            def is_zero(v):
                if cmp(abs(v)) == 0: return True
                if cmp(abs(v.normalized() - self.normal)) == 0: return True
                return False

            if is_zero(b.cross(p)) and is_zero(p.cross(c)) and is_zero((c - b).cross(p - b)):
                return True
            return False
        raise NotImplementedError("Higher dimensions are not supported")

    def uniform_sample(self, num):
        """ Reference: 
            [1] https://math.stackexchange.com/questions/18686/uniform-random-point-in-triangle-in-3d
        """
        ret = []
        for i in range(num):
            r1 = random.uniform(0, 1)
            r2 = random.uniform(0, 1)
            p = self.a * (1 - math.sqrt(r1)) + self.b * math.sqrt(r1) * (1 - r2) \
                + self.c * math.sqrt(r1) * r2
            ret.append(p)

        return ret

    def uniform_sample_parallelogram(self, num):
        b, c = self.b - self.a, self.c - self.a
        ret = []
        for _ in range(num):
            p = b * random.uniform(0, 1) + c * random.uniform(0, 1)

            if not self.inside_point(p + self.a):
                p = b + c - p
            ret.append(p + self.a)
        return ret

    def uniform_sample_rectangle(self, num):
        mn, mx = self.aabb
        ret = []
        for _ in range(num):
            x = random.uniform(mn[0], mx[0])
            y = random.uniform(mn[1], mx[1])
            while not self.inside_point(Point(x, y)):
                x = random.uniform(mn[0], mx[0])
                y = random.uniform(mn[1], mx[1])
            ret.append(Point(x, y))
        return ret


def test_triangle():
    tri = Triangle((0, 0), (1, 1.5), (0, 1))

    import matplotlib.pyplot as plt
    import matplotlib.patches as pat
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111)

    for i in range(3):
        a, b = tri[i], tri[(i + 1) % 3]
        ax.plot([a.x, b.x], [a.y, b.y], c='k', zorder=-1)
        ax.scatter(a.x, a.y, c='r')

    c = tri.centroid
    ax.scatter(c.x, c.y, c='b')
    ax.text(c.x, c.y, 'centroid', c='b')

    c, r = tri.incircle()
    ax.scatter(c.x, c.y, c='g')
    ax.text(c.x, c.y, 'incenter', c='g')
    ax.add_patch(pat.Circle((c.x, c.y), r, facecolor='w', edgecolor='g', zorder=-9))

    c, r = tri.circumcircle()
    ax.scatter(c.x, c.y, c='y')
    ax.text(c.x, c.y, 'circumcenter', c='y')
    ax.add_patch(pat.Circle((c.x, c.y), r, facecolor='w', edgecolor='y', zorder=-10))
    # plt.show()
    plt.savefig('./imgs/triangle_circles.png')

def test_sample():
    tri = Triangle((0, 0), (1, 1.5), (0, 1))
    import matplotlib.pyplot as plt
    import matplotlib.patches as pat
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111)
    for i in range(3):
        a, b = tri[i], tri[(i + 1) % 3]
        ax.plot([a.x, b.x], [a.y, b.y], c='k', zorder=-1)
        ax.scatter(a.x, a.y, c='r')

    pts = tri.uniform_sample(100)
    ax.scatter([p.x for p in pts], [p.y for p in pts], color='r')
    plt.show()
 

if __name__ == '__main__':
    # test_triangle()
    test_sample()
