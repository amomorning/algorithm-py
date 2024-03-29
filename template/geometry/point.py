import collections, math, bisect, heapq, random, functools, itertools, copy, typing, operator
import platform;

LOCAL = (platform.uname().node == 'AMO')


def debug(*args):
    if LOCAL:
        print('\033[92m', end='')
        printf(*args)
        print('\033[0m', end='')


def printf(*args):
    if LOCAL:
        print('>>>: ', end='')
    for arg in args:
        if isinstance(arg, typing.Iterable) and \
                not isinstance(arg, str) and \
                not isinstance(arg, dict):
            print(' '.join(map(str, arg)), end=' ')
        else:
            print(arg, end=' ')
    print()


def check(op, lhs, rhs=None):
    if not op(lhs, rhs):
        debug('Error: ', lhs, 'not', op.__name__, rhs)
    else:
        printf(lhs, op.__name__, rhs)


EPS = 1e-6
INF = 1e100


def cmp(x): return -1 if x < -EPS else int(x > EPS)


def polar_cmp(a, b):
    if cmp(a.y) * cmp(b.y) <= 0:
        if cmp(a.y) > 0 or cmp(b.y) > 0: return cmp(a.y - b.y)
        if cmp(a.y) == 0 and cmp(b.y) == 0: return cmp(a.x - b.x)
    return -cmp(a.cross(b))


def find_points_in_aabb(xs, ys, aabb, boundary=True):
    """ pts: Sorted Points in [(x, y, id), ...]
        aabb: [[minx, miny], [maxx, maxy]]
        Returns: index list
    """
    if boundary:
        xl = bisect.bisect_right(xs, (aabb[0][0] - EPS, -1))
        xr = bisect.bisect_left(xs, (aabb[1][0] + EPS, -1))

        yl = bisect.bisect_right(ys, (aabb[0][1] - EPS, -1))
        yr = bisect.bisect_left(ys, (aabb[1][1] + EPS, -1))

    else:
        xl = bisect.bisect_left(xs, (aabb[0][0] + EPS, -1))
        xr = bisect.bisect_right(xs, (aabb[1][0] - EPS, -1))

        yl = bisect.bisect_left(ys, (aabb[0][1] + EPS, -1))
        yr = bisect.bisect_right(ys, (aabb[1][1] - EPS, -1))
    idx = set([x[1] for x in xs[xl:xr]])
    idy = set([y[1] for y in ys[yl:yr]])
    return idx & idy


class Point:
    def __init__(self, *args):
        if len(args) == 1:
            args = args[0]
        self.__v = list(args)

    def __len__(self):
        return len(self.__v)

    def __str__(self):
        return 'Point' + str(tuple(self.__v))

    def __repr__(self):
        return 'Point' + str(tuple(self.__v))

    def print(self):
        return ' '.join(map(str, self.__v))

    def __hash__(self):
        return hash(tuple(self.__v))

    def __getitem__(self, key):
        if type(key) is int or slice:
            return self.__v[key]

    def __getattr__(self, key):
        if key == 'x':
            return self.__v[0]
        if key == 'y':
            return self.__v[1]
        if key == 'z':
            return self.__v[2]
        if key == 'w':
            return self.__v[3]
        raise KeyError('Invalid key: %s' % key)

    def __setitem__(self, key, value):
        if type(key) is int and key < len(self.__v):
            self.__v[key] = value
        if key == 'x':
            self.__v[0] = value
        if key == 'y':
            self.__v[1] = value
        if key == 'z':
            self.__v[2] = value
        if key == 'w':
            self.__v[3] = value
        raise KeyError('Invalid key: %s' % key)

    def __neg__(self):
        ret = []
        for x in self:
            ret.append(-x)
        return Point(ret)

    def __eq__(self, rhs):
        if type(rhs) != Point: rhs = Point(rhs)
        assert len(rhs) == len(self)

        for i in range(len(self)):
            if cmp(self[i] - rhs[i]) != 0:
                return False
        return True

    def __le__(self, rhs):
        if type(rhs) != Point: rhs = Point(rhs)
        assert len(rhs) == len(self)

        for i in range(len(self)):
            if cmp(self[i] - rhs[i]) < 0:
                return True
            if cmp(self[i] - rhs[i]) > 0:
                return False
        return True

    def __lt__(self, rhs):
        if type(rhs) != Point: rhs = Point(rhs)
        assert len(rhs) == len(self)

        for i in range(len(self)):
            if cmp(self[i] - rhs[i]) < 0:
                return True
            if cmp(self[i] - rhs[i]) > 0:
                return False
        return False

    def __add__(self, rhs):
        if type(rhs) != Point: rhs = Point(rhs)
        ret = []
        for i in range(len(self)):
            ret.append(self[i] + rhs[i])
        return Point(ret)

    def __sub__(self, rhs):
        return self + (-rhs)

    def __mul__(self, scale):
        ret = []
        for x in self:
            ret.append(x * scale)
        return Point(ret)

    def __rmul__(self, scale):
        return self * scale

    def __truediv__(self, scale):
        return self * (1.0 / scale)

    def __floordiv__(self, scale):
        ret = []
        for x in self:
            ret.append(x // scale)
        return Point(ret)

    def __matmul__(self, rhs):
        if type(rhs) != Point: rhs = Point(rhs)
        ret = []
        for i in range(len(rhs)):
            ret.append(self[i] * rhs[i])
        return Point(ret)

    def __pow__(self, scale):
        tot = 0
        for x in self:
            tot += x ** scale
        return tot

    def __abs__(self):
        return (self ** 2) ** 0.5

    @property
    def polar(self):
        assert len(self) == 2
        return self.norm(),

    def norm(self, v=2, maxd=50):
        return (self ** v) ** (1.0 / v) if v <= maxd else max(self)

    def normalized(self):
        return self / self.norm()

    def dot(self, rhs):
        if type(rhs) != Point: rhs = Point(rhs)
        return sum(self @ rhs)

    def cross(self, rhs):
        if type(rhs) != Point: rhs = Point(rhs)
        if len(self.__v) == 3:
            a, b, c = self
            x, y, z = rhs
            return Point(-c * y + b * z, c * x - a * z, -b * x + a * y)
        elif len(self.__v) == 2:
            return self.x * rhs.y - self.y * rhs.x
        raise ValueError("Invalid coordinates")

    def proj(self, rhs):
        if type(rhs) != Point: rhs = Point(rhs)
        return rhs * self.dot(rhs) / rhs.dot(rhs)

    def select(self, dim):
        assert len(dim) > 1
        return Point([self[d] for d in dim])

    # Quaternion
    def conj(self):
        ret = [self[0]]
        for i in range(1, len(self)):
            ret.append(-self[i])
        return Point(ret)

    def inv(self):
        l2 = self.dot(self)
        return self.conj() / l2

    def mulq(self, rhs):
        assert len(self.__v) == 4
        if type(rhs) != Point: rhs = Point(rhs)

        q0, q1, q2, q3 = self
        p0, p1, p2, p3 = rhs

        return Point(q0 * p0 - q1 * p1 - q2 * p2 - q3 * p3, \
                     q0 * p1 + q1 * p0 + q2 * p3 - q3 * p2, \
                     q0 * p2 - q1 * p3 + q2 * p0 + q3 * p1, \
                     q0 * p3 + q1 * p2 - q2 * p1 + q3 * p0)

    # rotate
    def rotate(self, angle):
        assert len(self.__v) == 2
        c, s = math.cos(angle), math.sin(angle)
        return Point(self.x * c - self.y * s, self.x * s + self.y * c)

    def rotate_90(self):
        assert len(self.__v) == 2
        return Point(-self.y, self.x)

    def rotate_x(self, angle):
        assert len(self.__v) == 3
        c, s = math.cos(angle), math.sin(angle)
        x, y, z = self
        return Point(x, y * c - z * s, y * s + z * c)

    def rotate_y(self, angle):
        assert len(self.__v) == 3
        c, s = math.cos(angle), math.sin(angle)
        x, y, z = self
        return Point(x * c + z * s, y, -x * s + z * c)

    def rotate_z(self, angle):
        assert len(self.__v) == 3
        c, s = math.cos(angle), math.sin(angle)
        x, y, z = self
        return Point(x * c - y * s, x * s + y * c, z)

    def rotate_by(self, axis, angle):
        assert len(self.__v) == 3
        if type(axis) != Point: axis = Point(axis)

        c, s = math.cos(angle), math.sin(angle)
        x, y, z = self
        ux, uy, uz = axis.normalized()

        return Point((c + ux * ux * (1 - c)) * x + (ux * uy * (1 - c) - uz * s) * y + (ux * uz * (1 - c) + uy * s) * z, \
                     (uy * ux * (1 - c) + uz * s) * x + (c + uy * uy * (1 - c)) * y + (uy * uz * (1 - c) - ux * s) * z, \
                     (uz * ux * (1 - c) - uy * s) * x + (uz * uy * (1 - c) + ux * s) * y + (c + uz * uz * (1 - c)) * z)

    def rotate_by_quaternion(self, axis, angle):
        assert len(self.__v) == 3
        if type(axis) != Point: axis = Point(axis)
        axis = axis.normalized() * math.sin(angle * 0.5)
        q = Point(math.cos(angle * 0.5), axis.x, axis.y, axis.z)
        return self.apply_quaternion(q)

    def apply_quaternion(self, q):
        p = Point(1.0, self.x, self.y, self.z)
        return Point(q.mulq(p).mulq(q.inv())[1:])

    def apply_matrix(self, m):
        """ row major matrix 
        """
        n = len(self)

        ret = []
        for i in range(n):
            tot = 0
            for j in range(n):
                tot += self[j] * m[i][j]
            ret.append(tot)

        return Point(ret)


def test_points():
    check(operator.lt, Point(1, 2), Point(1, 2))
    check(operator.le, Point(1, 2), Point(1, 2))

    # 按 y 排序
    a = [Point(3, 4), Point(1, 2), Point(3, 5), Point(2, 7)]
    a = sorted(a, key=lambda p: p[1])
    debug('Sorted by Y:', a)

    a = sorted(a, key=functools.cmp_to_key(polar_cmp), reverse=True)
    debug('sorted by Polar:', a)

    check(operator.eq, sum(a, start=Point(0, 0)), Point(9, 18))

    a = Point(1, 2)
    b = Point(0, 4)

    check(operator.eq, a.proj(b), Point(0, 2))
    debug(a.rotate(0.1))

    a = Point(1, 2, 3)
    check(operator.eq, a.rotate_by_quaternion((1, 1, 1), 0.5), a.rotate_by((1, 1, 1), 0.5))

    a = Point(1, 2, 3, 1)
    check(operator.eq, Point(2, 3, 4, 1), a.apply_matrix([[1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 1], [0, 0, 0, 1]]))

    # a = Point(1)


def test_inside_aabb():
    n = 1000
    pts = [Point(random.randint(0, 100), random.randint(0, 100)) for _ in range(n)]
    print(' '.join(map(str, pts)))
    xs = sorted([(pts[i].x, i) for i in range(n)])
    ys = sorted([(pts[i].y, i) for i in range(n)])
    res = find_points_in_aabb(xs, ys, [[20, 20], [40, 60]], False)
    print(res)

    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1)
    inside = [[], []]
    outside = [[], []]
    for i in range(n):
        if i in res:
            inside[0].append(pts[i].x)
            inside[1].append(pts[i].y)
        else:
            outside[0].append(pts[i].x)
            outside[1].append(pts[i].y)
    ax.scatter(inside[0], inside[1], c='r')
    ax.scatter(outside[0], outside[1], c='k')
    plt.show()


if __name__ == '__main__':
    # test_inside_aabb()
    p0 = Point([1, 2, 3])
    p1 = Point([4, 5, 6])
    print(p0.proj(p1))
