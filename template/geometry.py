import collections, math, bisect, heapq, random, functools, itertools, copy, typing
import platform; LOCAL = (platform.uname().node == 'AMO')

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


import math, operator
EPS = 1e-6
def cmp(x): return -1 if x < -EPS else int(x > EPS)

class Point:
    def __init__(self, *args):
        if len(args) == 1:
            args = args[0]
        self.__v = list(args)
        
    def __len__(self):
        return len(self.__v)

    def __str__(self):
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
        return self * (1.0/scale)
    
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
    
    def norm(self, v = 2, maxd = 50):
        return (self ** v) ** (1.0/v) if v <= maxd else max(self)
    
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
            return Point(-c*y + b*z, c*x - a*z, -b*x + a*y)
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
        assert len(self.__v)  == 4
        if type(rhs) != Point: rhs = Point(rhs)

        q0, q1, q2, q3 = self
        p0, p1, p2, p3 = rhs

        return Point(q0*p0 - q1*p1 - q2*p2 - q3*p3, \
                     q0*p1 + q1*p0 + q2*p3 - q3*p2, \
                     q0*p2 - q1*p3 + q2*p0 + q3*p1, \
                     q0*p3 + q1*p2 - q2*p1 + q3*p0)

    # rotate
    def rotate(self, angle):
        assert len(self.__v) == 2
        c, s = math.cos(angle), math.sin(angle)
        return Point(self.x * c - self.y * s, self.x * s + self.y * c)
        
    def rotate_90(self):
        assert len(self.__v) == 2
        return Point(-self.y, self.x)
    
    def rotate_x(self, angle):
        assert len(self.__v)  == 3
        c, s = math.cos(angle), math.sin(angle)
        x, y, z = self
        return Point(x, y * c - z * s, y * s + z * c)
    
    def rotate_y(self, angle):
        assert len(self.__v)  == 3
        c, s = math.cos(angle), math.sin(angle)
        x, y, z = self
        return Point(x * c + z * s, y, -x * s + z * c)

    def rotate_z(self, angle):
        assert len(self.__v)  == 3
        c, s = math.cos(angle), math.sin(angle)
        x, y, z = self
        return Point(x * c - y * s, x * s + y * c, z)
    
    def rotate_by(self, axis, angle):
        assert len(self.__v)  == 3
        if type(axis) != Point: axis = Point(axis)
        
        c, s = math.cos(angle), math.sin(angle)
        x, y, z = self
        ux, uy, uz = axis.normalized()

        return Point((c+ux*ux*(1-c))*x + (ux*uy*(1-c)-uz*s)*y + (ux*uz*(1-c)+uy*s)*z, \
                     (uy*ux*(1-c)+uz*s)*x + (c+uy*uy*(1-c))*y + (uy*uz*(1-c)-ux*s)*z, \
                     (uz*ux*(1-c)-uy*s)*x + (uz*uy*(1-c)+ux*s)*y + (c+uz*uz*(1-c))*z)

    def rotate_by_quaternion(self, axis, angle): 
        assert len(self.__v) == 3
        if type(axis) != Point: axis = Point(axis)
        axis = axis.normalized() * math.sin(angle*0.5)
        q = Point(math.cos(angle*0.5), axis.x, axis.y, axis.z)
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


class Segment:
    def __init__(self, a, b):
        self.a = Point(a)
        self.b = Point(b)

    def __getitem__(self, item):
        if item == 0: return self.a
        if item == 1: return self.b
        raise KeyError('Invalid item: %s' % item)

    def __str__(self) -> str:
        return 'Line: [' + str(self.a) + ', ' + str(self.b) + ']'

    def length(self):
        return abs(self.a - self.b)

    def on_point(self, point):
        if type(point) != Point: point = Point(point)
        u, v = self.a-point, self.b-point
        return abs(u.cross(v)) == 0 and u.dot(v) <= 0
    
    def lerp(self, t):
        return (1 - t) * self.a + t * self.b

    def project_on(self, dim):        
        return Segment(self.a.select(dim), self.b.select(dim))

    def is_proper_intersect(self, line):
        assert len(self.a) == 2
        c1 = (self.b - self.a).cross(line.a - self.a)
        c2 = (self.b - self.a).cross(line.b - self.a)
        c3 = (line.b - line.a).cross(self.a - line.a)
        c4 = (line.b - line.a).cross(self.b - self.a)
        return c1 * c2  < 0 and c3 * c4 < 0

    def is_intersect(self, line):
        if self.is_proper_intersect(line):
            return True
        return self.on_point(line.a) or self.on_point(line.b) or\
            line.on_point(self.a) or line.on_point(self.b)
    
    def intersection(self, line):
        if len(line.a) == 3:
            return self.intersection_3d(line)

        if not self.is_intersect(line):
            return None
        u, v, w = line.a - self.a, self.b - self.a, line.b - line.a
        if cmp(v.cross(w)) == 0:
            if line.on_point(self.a):
                return self.a
            if line.on_point(self.b):
                return self.b
            return None
        t = w.cross(u) / w.cross(v)
        # debug(t)
        return self.lerp(t)
    
    def intersection_3d(self, line):
        assert len(self.a) == 3

        x_p = self.project_on((1, 2)).intersection(line.project_on((1, 2)))
        y_p = self.project_on((0, 2)).intersection(line.project_on((0, 2)))
        z_p = self.project_on((0, 1)).intersection(line.project_on((0, 1)))

        if x_p is None or y_p is None or z_p is None:
            return None

        for x in [y_p.x, z_p.x]:
            for y in [x_p.x, z_p.y]:
                for z in [x_p.y, y_p.y]:
                    pt = Point(x, y, z)
                    if self.on_point(pt) and line.on_point(pt):
                        return pt
        return None

    
    def project_point(self, point):
        u, v = point - self.a, self.b - self.a
        return self.a + u.proj(v)
    
    def distance(self, rhs):
        if type(rhs) == Point:
            u, v, w = self.b - self.a, rhs - self.a, rhs - self.b
            if cmp(u.dot(v)) < 0: return abs(v)
            elif cmp(u.dot(w)) > 0: return abs(w)
            else: return abs(u.cross(v)) / abs(u)
        
        if type(rhs) == Segment:
            if self.intersection(rhs) != None:
                return 0
            ret = min(self.distance(rhs.a), self.distance(rhs.b))
            ret = min(ret, min(rhs.distance(self.a), rhs.distance(self.b)))

            if len(self.a) == 3:
                """ Reference
                    for line line distance
                    [1] https://mathworld.wolfram.com/Line-LineDistance.html
                
                    # a, b, c = self.b - self.a, rhs.b - rhs.a, rhs.a - self.a
                    # return abs(a.cross(b).dot(c)) / abs(a.cross(b))

                    but here we should calculate the distance between two segments
                    [2] https://zalo.github.io/blog/closest-point-between-segments/
                """
                p = Plane(self.a, self.b-self.a)
                line = p.project_segment(rhs)
                closest = line.project_point(self.a)                
                if line.on_point(closest):
                    ret = min(ret, line.distance(self.a))

            return ret
            
        raise NotImplementedError("distance is not implemented for type %s" % type(rhs))

class Plane:
    def __init__(self, base, normal):
        self.base = base
        self.normal = normal
        self.normal.normalized()
    
    def project_point(self, point):
        vector = point - self.base
        return vector - vector.proj(self.normal)
    
    def project_segment(self, segment):
        a = self.project_point(segment.a)
        b = self.project_point(segment.b)
        return Segment(a, b)

if __name__ == '__main__':

    check(operator.lt, Point(1, 2), Point(1, 2))
    check(operator.le, Point(1, 2), Point(1, 2))
    
    # 按 y 排序
    a = [Point(3, 4), Point(1, 2), Point(3, 5), Point(2,7)]
    a = sorted(a, key=lambda p: p[1])
    debug('Sorted by Y:', a)

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

    # print(a.rotate(math.pi/3))
    l = Segment(Point(0, 0), Point(3, 3))
    check(operator.eq, l.lerp(0.3), Point(0.9, 0.9))
    check(operator.eq, l.intersection(Segment(Point(1, 0), Point(0, 1))), Point(0.5, 0.5))
    # (3, 8)

    debug((Point(1, 2, 3).dot(Point(-2, -4, -6))))

    # print(a.dot(b))
    check(operator.eq, Point(1, 2, 3).select((0, 2)), Point(1, 3))

    l = Segment(Point(0, 0, 0), Point(2, 4, 6))
    r = Segment(Point(5, 0, 0), Point(-3, 4, 6))
    r_ = Segment(Point(5, 0, 0), Point(2, 4, 6))
    check(operator.eq, l.intersection_3d(r), Point(1, 2, 3))
    # >>>: Point(1.0, 2.0, 3.0) eq Point(1, 2, 3)
    check(operator.eq, l.intersection_3d(r_), Point(2, 4, 6))
    # >>>: None eq None

    l = Segment(Point(0, 0, 0), Point(3, 3, 0))
    check(operator.eq, l.distance(Point(1, 0, 0)), math.sqrt(2) * 0.5)

    check(operator.eq, l.project_point(Point(-1, 0, 0)), Point(-0.5, -0.5, 0))

    p = Plane(Point(0, 0, 0), Point(0, 1, 0))
    debug(p.project_segment(Segment(Point(2, 1, 0), Point(4, 0, 5))))

    check(operator.eq, l.distance(r), 5.0/math.sqrt(6))
